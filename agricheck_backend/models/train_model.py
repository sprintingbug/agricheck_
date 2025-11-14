"""
Train Rice Leaf Disease Detection Model
Uses EfficientNetB0 with your dataset to train a high-accuracy model
for the 4 rice leaf disease classes: bacterial_leaf_blight, healthy, leaf_blast, tungro_virus
"""
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0
from PIL import Image
import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
IMAGE_SIZE = (224, 224)  # EfficientNetB0 input size
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001
VALIDATION_SPLIT = 0.2
TEST_SPLIT = 0.1

# Disease classes (must match labels.txt order)
DISEASE_CLASSES = [
    "bacterial_leaf_blight",
    "healthy",
    "leaf_blast",
    "tungro_virus",
]

# Paths - Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.resolve()
DATASET_DIR = SCRIPT_DIR / "dataset"
MODEL_DIR = SCRIPT_DIR
LABELS_FILE = SCRIPT_DIR / "labels.txt"

def load_images_from_folder(folder_path, class_index):
    """Load all images from a folder and assign class label"""
    images = []
    labels = []
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        logger.warning(f"Folder not found: {folder_path}")
        return images, labels
    
    # Supported image extensions
    extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
    
    image_files = []
    for ext in extensions:
        image_files.extend(list(folder_path.glob(f'*{ext}')))
    
    logger.info(f"Found {len(image_files)} images in {folder_path.name}")
    
    for img_path in image_files:
        try:
            # Load and preprocess image
            img = Image.open(img_path)
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to model input size
            img = img.resize(IMAGE_SIZE)
            
            # Convert to numpy array and normalize
            img_array = np.array(img, dtype=np.float32)
            
            images.append(img_array)
            labels.append(class_index)
            
        except Exception as e:
            logger.warning(f"Error loading {img_path}: {e}")
            continue
    
    return images, labels

def get_dataset_info():
    """Get dataset information without loading all images into memory"""
    dataset_path = DATASET_DIR if isinstance(DATASET_DIR, Path) else Path(DATASET_DIR)
    
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_path}")
    
    total_images = 0
    class_counts = {}
    
    for class_idx, class_name in enumerate(DISEASE_CLASSES):
        class_folder = dataset_path / class_name
        if class_folder.exists():
            # Count images
            extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
            count = sum(len(list(class_folder.glob(f'*{ext}'))) for ext in extensions)
            class_counts[class_name] = count
            total_images += count
            logger.info(f"Found {count} images in {class_name}")
        else:
            logger.warning(f"Folder not found: {class_folder}")
            class_counts[class_name] = 0
    
    if total_images == 0:
        raise ValueError("No images found in dataset folders!")
    
    logger.info(f"Total images: {total_images}")
    logger.info(f"Class distribution: {class_counts}")
    
    return total_images, class_counts

def create_model(input_shape=(224, 224, 3), num_classes=4):
    """Create EfficientNetB0 model with custom top layers"""
    # Load EfficientNetB0 base model (pre-trained on ImageNet)
    base_model = EfficientNetB0(
        weights='imagenet',
        include_top=False,
        input_shape=input_shape
    )
    
    # Freeze base model layers initially
    base_model.trainable = False
    
    # Add custom top layers for rice leaf disease classification
    inputs = keras.Input(shape=input_shape)
    
    # Preprocess input for EfficientNet
    x = keras.applications.efficientnet.preprocess_input(inputs)
    
    # Base model
    x = base_model(x, training=False)
    
    # Global average pooling
    x = layers.GlobalAveragePooling2D()(x)
    
    # Add dropout for regularization
    x = layers.Dropout(0.3)(x)
    
    # Dense layers with batch normalization
    x = layers.Dense(512, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    
    x = layers.Dense(256, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.2)(x)
    
    # Output layer (4 classes)
    outputs = layers.Dense(num_classes, activation='softmax', name='predictions')(x)
    
    model = keras.Model(inputs, outputs, name='rice_leaf_disease_model')
    
    return model, base_model

def train_model():
    """Main training function"""
    logger.info("=" * 60)
    logger.info("Starting Rice Leaf Disease Model Training")
    logger.info("=" * 60)
    
    # Get dataset info
    logger.info("Checking dataset...")
    total_images, class_counts = get_dataset_info()
    
    # Use ImageDataGenerator with flow_from_directory to load images in batches
    # This avoids loading all images into memory at once
    dataset_path = str(DATASET_DIR if isinstance(DATASET_DIR, Path) else Path(DATASET_DIR))
    
    # Create data augmentation for training
    train_datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=VALIDATION_SPLIT + TEST_SPLIT,
        preprocessing_function=keras.applications.efficientnet.preprocess_input
    )
    
    # Validation/Test data generator (no augmentation, just preprocessing)
    val_datagen = ImageDataGenerator(
        validation_split=VALIDATION_SPLIT + TEST_SPLIT,
        preprocessing_function=keras.applications.efficientnet.preprocess_input
    )
    
    # Create generators for train, validation, and test sets
    logger.info("Creating data generators...")
    
    # Training generator
    train_generator = train_datagen.flow_from_directory(
        dataset_path,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True,
        seed=42
    )
    
    # Calculate split sizes for validation and test
    total = sum(class_counts.values())
    val_size = int(total * VALIDATION_SPLIT)
    test_size = int(total * TEST_SPLIT)
    train_size = total - val_size - test_size
    
    logger.info(f"Train set: ~{train_size} images")
    logger.info(f"Validation set: ~{val_size} images")
    logger.info(f"Test set: ~{test_size} images")
    
    # Validation generator (using validation_split)
    val_generator = val_datagen.flow_from_directory(
        dataset_path,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False,
        seed=42
    )
    
    # For test set, we'll use a portion of validation set
    # Or we can evaluate separately after training
    test_generator = val_datagen.flow_from_directory(
        dataset_path,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False,
        seed=42
    )
    
    # Create model
    logger.info("Creating model...")
    model, base_model = create_model()
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy', 'top_k_categorical_accuracy']
    )
    
    logger.info("Model architecture:")
    model.summary()
    
    # Callbacks
    callbacks_list = [
        callbacks.ModelCheckpoint(
            filepath=str(MODEL_DIR / 'best.keras'),
            monitor='val_accuracy',
            save_best_only=True,
            save_weights_only=False,
            mode='max',
            verbose=1
        ),
        callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        ),
        callbacks.CSVLogger(str(MODEL_DIR / 'training_log.csv'))
    ]
    
    # Stage 1: Train with frozen base model
    logger.info("=" * 60)
    logger.info("Stage 1: Training with frozen base model")
    logger.info("=" * 60)
    
    history1 = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // BATCH_SIZE,
        epochs=20,  # First stage: fewer epochs
        validation_data=val_generator,
        validation_steps=val_generator.samples // BATCH_SIZE,
        callbacks=callbacks_list,
        verbose=1
    )
    
    # Stage 2: Fine-tune with unfrozen base model
    logger.info("=" * 60)
    logger.info("Stage 2: Fine-tuning with unfrozen base model")
    logger.info("=" * 60)
    
    # Unfreeze last few layers of base model for fine-tuning
    base_model.trainable = True
    for layer in base_model.layers[:-30]:  # Freeze all but last 30 layers
        layer.trainable = False
    
    # Recompile with lower learning rate for fine-tuning
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE * 0.1),
        loss='categorical_crossentropy',
        metrics=['accuracy', 'top_k_categorical_accuracy']
    )
    
    # Update callbacks for fine-tuning
    callbacks_list_finetune = [
        callbacks.ModelCheckpoint(
            filepath=str(MODEL_DIR / 'best_finetuned.keras'),
            monitor='val_accuracy',
            save_best_only=True,
            save_weights_only=False,
            mode='max',
            verbose=1
        ),
        callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        ),
        callbacks.CSVLogger(str(MODEL_DIR / 'training_log_finetuned.csv'))
    ]
    
    history2 = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // BATCH_SIZE,
        epochs=EPOCHS - 20,  # Remaining epochs
        validation_data=val_generator,
        validation_steps=val_generator.samples // BATCH_SIZE,
        callbacks=callbacks_list_finetune,
        verbose=1
    )
    
    # Evaluate on validation set (which we'll use as test)
    logger.info("=" * 60)
    logger.info("Evaluating on validation set...")
    logger.info("=" * 60)
    
    test_loss, test_accuracy, test_top_k = model.evaluate(
        val_generator,
        steps=val_generator.samples // BATCH_SIZE,
        verbose=1
    )
    
    logger.info(f"Validation Accuracy: {test_accuracy:.4f}")
    logger.info(f"Validation Top-K Accuracy: {test_top_k:.4f}")
    
    # Save final model
    final_model_path = MODEL_DIR / 'best_finetuned.keras'
    if final_model_path.exists():
        logger.info(f"✅ Best model saved to: {final_model_path}")
    else:
        model.save(str(final_model_path))
        logger.info(f"✅ Final model saved to: {final_model_path}")
    
    # Save labels file
    labels_path = LABELS_FILE if isinstance(LABELS_FILE, Path) else Path(LABELS_FILE)
    with open(labels_path, 'w') as f:
        for class_name in DISEASE_CLASSES:
            f.write(f"{class_name}\n")
    
    logger.info(f"✅ Labels saved to: {labels_path}")
    logger.info("=" * 60)
    logger.info("Training completed!")
    logger.info("=" * 60)
    
    return model, history1, history2

if __name__ == "__main__":
    # Set memory growth for GPU (if available)
    try:
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            logger.info(f"Using GPU: {gpus}")
    except Exception as e:
        logger.info(f"GPU setup failed: {e}. Using CPU.")
    
    # Train model
    model, history1, history2 = train_model()
    
    logger.info("\n✅ Training complete! Model saved as 'best_finetuned.keras'")
    logger.info("📁 The backend will automatically use this model for predictions.")

