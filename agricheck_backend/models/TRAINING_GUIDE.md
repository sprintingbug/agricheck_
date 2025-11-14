# Training Guide: Rice Leaf Disease Detection Model

## Overview

This guide explains how to train a high-accuracy model for detecting 4 rice leaf disease states:
1. **bacterial_leaf_blight** - Bacterial Leaf Blight
2. **healthy** - Healthy leaves
3. **leaf_blast** - Leaf Blast
4. **tungro_virus** - Tungro Virus

## Dataset Structure

Your dataset should be organized as follows:

```
models/
└── dataset/
    ├── bacterial_leaf_blight/
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   └── ...
    ├── healthy/
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   └── ...
    ├── leaf_blast/
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   └── ...
    └── tungro_virus/
        ├── image1.jpg
        ├── image2.jpg
        └── ...
```

## Prerequisites

1. **Python 3.8+** installed
2. **TensorFlow 2.13+** installed
3. **Dataset** in the `models/dataset/` folder

## Training Steps

### 1. Activate Virtual Environment

```bash
cd C:\dev\agricheck_backend
.venv\Scripts\activate
```

### 2. Navigate to Models Directory

```bash
cd models
```

### 3. Run Training Script

```bash
python train_model.py
```

## Training Process

The training script performs:

1. **Data Loading**: Loads all images from dataset folders
2. **Data Splitting**: 
   - 70% Training
   - 20% Validation
   - 10% Test
3. **Data Augmentation**: Applies rotations, shifts, zooms, flips for better generalization
4. **Model Creation**: Creates EfficientNetB0 model with:
   - Pre-trained ImageNet weights
   - Custom top layers for 4-class classification
5. **Two-Stage Training**:
   - **Stage 1**: Train with frozen base model (20 epochs)
   - **Stage 2**: Fine-tune with unfrozen layers (remaining epochs)
6. **Model Saving**: Saves best model as `best_finetuned.keras`

## Training Configuration

You can modify these settings in `train_model.py`:

```python
IMAGE_SIZE = (224, 224)      # Input image size
BATCH_SIZE = 32              # Training batch size
EPOCHS = 50                  # Total training epochs
LEARNING_RATE = 0.001        # Initial learning rate
VALIDATION_SPLIT = 0.2       # Validation set percentage
TEST_SPLIT = 0.1             # Test set percentage
```

## Model Output

After training, you'll get:

- `best.keras` - Best model from Stage 1
- `best_finetuned.keras` ⭐ - Best model from Stage 2 (recommended)
- `training_log.csv` - Training metrics
- `training_log_finetuned.csv` - Fine-tuning metrics
- `labels.txt` - Class labels (auto-generated)

## Using the Trained Model

The backend will automatically detect and use `best_finetuned.keras`:

1. The model is saved in `models/best_finetuned.keras`
2. The backend's `ModelService` will automatically load it
3. No code changes needed - just restart the backend server

## Training Tips

### For Better Accuracy:

1. **More Images**: Aim for at least 100+ images per class
2. **Balanced Dataset**: Try to have similar number of images per class
3. **Quality Images**: Use clear, well-lit images of rice leaves
4. **Data Augmentation**: The script already includes augmentation, but you can add more
5. **More Epochs**: Increase `EPOCHS` if validation accuracy is still improving

### Monitoring Training:

- Watch the validation accuracy - it should increase over time
- If validation accuracy stops improving, training will stop early (EarlyStopping)
- Check `training_log_finetuned.csv` for detailed metrics

## Troubleshooting

### "No images found" error:
- Check that dataset folders match class names exactly
- Ensure images are in `.jpg`, `.jpeg`, or `.png` format
- Verify folder structure matches the expected layout

### Out of Memory error:
- Reduce `BATCH_SIZE` (try 16 or 8)
- Reduce `IMAGE_SIZE` (try 192x192 or 160x160)

### Training too slow:
- Use GPU if available (TensorFlow will auto-detect)
- Reduce number of epochs
- Reduce batch size

## Model Architecture

- **Base Model**: EfficientNetB0 (pre-trained on ImageNet)
- **Top Layers**: 
  - Global Average Pooling
  - Dense(512) + BatchNorm + Dropout(0.3)
  - Dense(256) + BatchNorm + Dropout(0.2)
  - Dense(4) with Softmax (4 classes)
- **Input**: 224x224 RGB images
- **Output**: 4-class probability distribution

## Expected Accuracy

With a good dataset:
- **Training Accuracy**: 90-98%
- **Validation Accuracy**: 85-95%
- **Test Accuracy**: 85-95%

## Next Steps

1. Train the model using `train_model.py`
2. Verify model works: `python test_model.py` (if available)
3. Restart backend server - it will auto-load the new model
4. Test with real rice leaf images through the scan page

---

**Note**: The trained model recognizes pixels and patterns in rice leaf images to detect diseases. The EfficientNetB0 architecture is excellent at extracting features from images, which helps with accurate disease classification.

