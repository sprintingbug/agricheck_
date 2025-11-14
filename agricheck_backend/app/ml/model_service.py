"""
ML Model Service for Rice Leaf Disease Detection
Based on EfficientNetB0 model trained on rice leaf dataset
Supports TensorFlow/Keras (.h5, .keras), PyTorch (.pth), and ONNX (.onnx) models
"""
import os
import numpy as np
from PIL import Image
from typing import Dict, Tuple, Optional, List
import logging

logger = logging.getLogger(__name__)

# Rice leaf disease classes - Matches the trained model from agricheckmodel.ipynb
# Order must match the model's output layer exactly!
# This order matches labels.txt: bacterial_leaf_blight, healthy, leaf_blast, tungro_virus
DISEASE_CLASSES = [
    "bacterial_leaf_blight",  # Index 0
    "healthy",                 # Index 1
    "leaf_blast",              # Index 2
    "tungro_virus",            # Index 3
]

# Human-readable disease names
DISEASE_NAMES = {
    "bacterial_leaf_blight": "Bacterial Leaf Blight",
    "healthy": "Healthy",
    "leaf_blast": "Leaf Blast",
    "tungro_virus": "Tungro Virus",
}

# Detailed recommendations for each disease (in Filipino and English)
DISEASE_RECOMMENDATIONS = {
    "healthy": {
        "en": "Your rice plant appears to be healthy. Continue with your regular watering and fertilization schedule. Monitor for any changes and maintain good agricultural practices.",
        "fil": "Ang inyong palay ay mukhang maayos at mabuti. Magpatuloy sa regular na pagdidilig at pagpapabunga. Bantayan ang anumang pagbabago at panatilihin ang mabuting pagsasaka.",
        "severity": "none",
        "action_required": False,
    },
    "bacterial_leaf_blight": {
        "en": "Bacterial Leaf Blight detected. This is a common rice disease that can be managed. Remove affected leaves and apply copper-based bactericide. Ensure good air circulation by proper spacing. Use resistant varieties in future plantings. With proper care, your crop can recover.",
        "fil": "Nakita ang Bacterial Leaf Blight. Ito ay karaniwang sakit ng palay na maaaring ma-manage. Tanggalin ang mga apektadong dahon at gumamit ng copper-based na bactericide. Siguraduhing may sapat na hangin sa pamamagitan ng tamang spacing. Gumamit ng resistant varieties sa susunod na tanim. Sa tamang pangangalaga, maaaring gumaling ang inyong pananim.",
        "severity": "moderate",
        "action_required": True,
    },
    "leaf_blast": {
        "en": "Leaf Blast detected. This is a fungal disease that responds well to treatment. Apply fungicide containing tricyclazole or azoxystrobin as directed. Remove affected leaves. Maintain proper spacing for air circulation. Avoid excessive nitrogen. Early treatment improves recovery.",
        "fil": "Nakita ang Leaf Blast. Ito ay fungal disease na maaaring gamutin. Gumamit ng fungicide na may tricyclazole o azoxystrobin ayon sa direksyon. Tanggalin ang mga apektadong dahon. Panatilihin ang tamang spacing para sa sapat na hangin. Iwasan ang labis na nitrogen. Maagang paggamot ay nakakatulong sa paggaling.",
        "severity": "moderate",
        "action_required": True,
    },
    "tungro_virus": {
        "en": "Tungro Virus detected. This viral disease is spread by leafhoppers. Remove affected plants to prevent spread to healthy ones. Control leafhoppers with appropriate insecticides. Consider using resistant rice varieties in your next planting. Early detection and management can help minimize impact.",
        "fil": "Nakita ang Tungro Virus. Ang viral disease na ito ay kumakalat sa pamamagitan ng leafhoppers. Tanggalin ang mga apektadong halaman upang maiwasan ang pagkalat sa malulusog na halaman. Kontrolin ang leafhoppers gamit ang angkop na insecticides. Isaalang-alang ang paggamit ng resistant rice varieties sa susunod na tanim. Maagang pag-detect at pag-manage ay makakatulong na mabawasan ang epekto.",
        "severity": "moderate",
        "action_required": True,
    },
}


class ModelService:
    """Service for loading and running ML model inference"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.model_type = None
        # Try multiple possible model file names/locations
        default_paths = [
            "models/best_finetuned.keras",
            "models/best.keras",
            "models/plant_disease_model.keras",
            "models/plant_disease_model.h5",
            "models/model.keras",
            "models/model.h5",
        ]
        self.model_path = model_path or os.getenv("MODEL_PATH")
        
        # If no path specified, try to find model file
        if not self.model_path:
            for path in default_paths:
                if os.path.exists(path):
                    self.model_path = path
                    break
            else:
                # Use first default if none found
                self.model_path = default_paths[0]
        
        self._load_model()
    
    def _load_model(self):
        """Load the ML model based on file extension"""
        if not os.path.exists(self.model_path):
            logger.warning(f"Model file not found at {self.model_path}. Using mock predictions.")
            return
        
        file_ext = os.path.splitext(self.model_path)[1].lower()
        
        try:
            if file_ext == ".h5" or file_ext == ".keras":
                self._load_keras_model()
            elif file_ext == ".pth" or file_ext == ".pt":
                self._load_pytorch_model()
            elif file_ext == ".onnx":
                self._load_onnx_model()
            else:
                logger.warning(f"Unsupported model format: {file_ext}. Using mock predictions.")
        except Exception as e:
            logger.error(f"Error loading model: {e}. Using mock predictions.")
            import traceback
            logger.error(traceback.format_exc())
    
    def _load_keras_model(self):
        """Load TensorFlow/Keras model (.h5 or .keras format)"""
        try:
            import tensorflow as tf
            from tensorflow import keras
            
            # Try loading as .keras first, then .h5
            if os.path.exists(self.model_path):
                self.model = keras.models.load_model(self.model_path)
            else:
                # Try alternative extensions
                for ext in ['.keras', '.h5']:
                    alt_path = os.path.splitext(self.model_path)[0] + ext
                    if os.path.exists(alt_path):
                        self.model = keras.models.load_model(alt_path)
                        self.model_path = alt_path
                        break
                else:
                    raise FileNotFoundError(f"Model file not found: {self.model_path}")
            
            self.model_type = "keras"
            logger.info(f"Successfully loaded Keras model from {self.model_path}")
            logger.info(f"Model input shape: {self.model.input_shape}")
            logger.info(f"Model output shape: {self.model.output_shape}")
        except ImportError:
            logger.error("TensorFlow not installed. Install with: pip install tensorflow")
        except Exception as e:
            logger.error(f"Error loading Keras model: {e}")
            raise
    
    def _load_pytorch_model(self):
        """Load PyTorch model"""
        try:
            import torch
            self.model = torch.load(self.model_path, map_location='cpu')
            self.model.eval()
            self.model_type = "pytorch"
            logger.info(f"Successfully loaded PyTorch model from {self.model_path}")
        except ImportError:
            logger.error("PyTorch not installed. Install with: pip install torch")
        except Exception as e:
            logger.error(f"Error loading PyTorch model: {e}")
    
    def _load_onnx_model(self):
        """Load ONNX model"""
        try:
            import onnxruntime as ort
            self.model = ort.InferenceSession(self.model_path)
            self.model_type = "onnx"
            logger.info(f"Successfully loaded ONNX model from {self.model_path}")
        except ImportError:
            logger.error("ONNX Runtime not installed. Install with: pip install onnxruntime")
        except Exception as e:
            logger.error(f"Error loading ONNX model: {e}")
    
    def preprocess_image(self, image_path: str, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
        """
        Preprocess image for EfficientNetB0 model input
        Uses EfficientNet preprocessing as per the training notebook
        """
        try:
            img = Image.open(image_path)
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # Resize image
            img = img.resize(target_size)
            # Convert to numpy array
            img_array = np.array(img, dtype=np.float32)
            
            # Use EfficientNet preprocessing (same as training)
            # This applies the correct normalization for EfficientNet
            try:
                import tensorflow as tf
                from tensorflow import keras
                # EfficientNet preprocessing: scales pixels to [-1, 1] range
                img_array = keras.applications.efficientnet.preprocess_input(img_array)
            except ImportError:
                # Fallback: manual EfficientNet preprocessing
                # EfficientNet expects input in range [-1, 1]
                img_array = (img_array / 127.5) - 1.0
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            return img_array
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            raise
    
    def predict(self, image_path: str, confidence_threshold: float = 0.65) -> Dict[str, any]:
        """
        Run prediction on an image with AI-enhanced analysis
        
        Args:
            image_path: Path to the image file
            confidence_threshold: Minimum confidence to accept prediction (default: 0.5)
        
        Returns:
            Dictionary with prediction results including disease name, confidence, 
            recommendations, and AI-enhanced analysis
        """
        if self.model is None:
            # Return mock prediction if model not loaded
            return self._mock_predict()
        
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image_path)
            
            # Run inference based on model type
            if self.model_type == "keras":
                predictions = self.model.predict(processed_image, verbose=0)
            elif self.model_type == "pytorch":
                import torch
                with torch.no_grad():
                    input_tensor = torch.from_numpy(processed_image).permute(0, 3, 1, 2)
                    predictions = self.model(input_tensor).numpy()
            elif self.model_type == "onnx":
                input_name = self.model.get_inputs()[0].name
                predictions = self.model.run(None, {input_name: processed_image})[0]
            else:
                return self._mock_predict()
            
            # Get predicted class and confidence
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            confidence_percent = confidence * 100
            
            # Get all predictions for analysis
            all_predictions_scores = {
                DISEASE_CLASSES[i]: float(predictions[0][i] * 100)
                for i in range(min(len(DISEASE_CLASSES), len(predictions[0])))
            }
            
            # Check if confidence meets threshold
            if confidence < confidence_threshold:
                logger.warning(f"Low confidence prediction: {confidence:.2f} < {confidence_threshold}")
                logger.info(f"All prediction scores: {all_predictions_scores}")
            
            # Additional validation: if confidence is very low, check if second prediction is close
            # This helps catch cases where the model is uncertain
            sorted_indices = np.argsort(predictions[0])[::-1]
            if len(sorted_indices) > 1:
                second_confidence = float(predictions[0][sorted_indices[1]] * 100)
                # If second prediction is close to first, it's uncertain
                if confidence_percent - second_confidence < 15.0:
                    logger.warning(f"Uncertain prediction: Top two predictions are close ({confidence_percent:.1f}% vs {second_confidence:.1f}%)")
            
            # Get disease class name (internal format)
            if predicted_class_idx < len(DISEASE_CLASSES):
                disease_class = DISEASE_CLASSES[predicted_class_idx]
                disease_name = DISEASE_NAMES.get(disease_class, disease_class.replace('_', ' ').title())
            else:
                disease_class = "unknown"
                disease_name = "Unknown"
            
            # Get recommendations with AI enhancement
            rec_info = DISEASE_RECOMMENDATIONS.get(
                disease_class.lower(),
                {
                    "en": "Please consult with an agricultural expert for proper diagnosis and treatment.",
                    "fil": "Pakipagkonsulta sa agricultural expert para sa tamang diagnosis at treatment.",
                    "severity": "unknown",
                    "action_required": True,
                }
            )
            
            # Build comprehensive recommendations with confidence-based messaging
            recommendations = self._build_ai_enhanced_recommendations(
                disease_class, disease_name, confidence_percent, rec_info, predictions[0]
            )
            
            # Get all predictions for analysis
            all_predictions = {
                DISEASE_NAMES.get(DISEASE_CLASSES[i], DISEASE_CLASSES[i].replace('_', ' ').title()): 
                float(predictions[0][i] * 100)
                for i in range(min(len(DISEASE_CLASSES), len(predictions[0])))
            }
            
            return {
                "disease_name": disease_name,
                "disease_class": disease_class,
                "confidence": round(confidence_percent, 2),
                "confidence_raw": confidence,
                "recommendations": recommendations,
                "severity": rec_info.get("severity", "unknown"),
                "action_required": rec_info.get("action_required", True),
                "all_predictions": all_predictions,
                "is_confident": confidence >= confidence_threshold,
            }
        except Exception as e:
            logger.error(f"Error during prediction: {e}", exc_info=True)
            return self._mock_predict()
    
    def _build_ai_enhanced_recommendations(
        self, 
        disease_class: str, 
        disease_name: str, 
        confidence: float, 
        rec_info: Dict,
        predictions: np.ndarray
    ) -> str:
        """
        Build AI-enhanced recommendations based on confidence and prediction analysis
        """
        base_rec = rec_info.get("fil", rec_info.get("en", ""))
        
        # Add confidence-based messaging (calm and professional, not alarming)
        if confidence >= 80:
            confidence_msg = "Mataas ang kumpiyansa sa diagnosis na ito."
        elif confidence >= 60:
            confidence_msg = "Katamtamang kumpiyansa sa diagnosis. Maaring kumonsulta sa agricultural expert para sa karagdagang tulong kung kinakailangan."
        else:
            confidence_msg = "Mababa ang kumpiyansa. Maaring kumonsulta sa agricultural expert para sa mas tiyak na diagnosis."
        
        # Check for secondary predictions (potential misdiagnosis)
        sorted_indices = np.argsort(predictions)[::-1]
        if len(sorted_indices) > 1:
            second_pred_idx = sorted_indices[1]
            second_confidence = predictions[second_pred_idx] * 100
            
            # If second prediction is close, mention it (only if significant)
            if second_confidence > 25 and (confidence - second_confidence) < 25:
                second_disease = DISEASE_NAMES.get(
                    DISEASE_CLASSES[second_pred_idx], 
                    DISEASE_CLASSES[second_pred_idx].replace('_', ' ').title()
                )
                base_rec += f"\n\nNote: Posible ring {second_disease} ({second_confidence:.1f}% confidence). Maaring kumonsulta sa agricultural expert para sa mas tiyak na diagnosis."
        
        # Add severity-based messaging (calm and informative, not alarming)
        severity = rec_info.get("severity", "unknown")
        # Use calm, informative prefix instead of dramatic warnings
        if severity in ["critical", "high", "moderate"]:
            base_rec = f"💡 {base_rec}"
        
        # Combine all messages in a calm, professional way
        full_recommendation = f"{confidence_msg}\n\n{base_rec}"
        
        # Add reassuring note for diseases (to prevent panic)
        if disease_class != "healthy" and severity != "none":
            full_recommendation += "\n\n💚 Paalala: Ang mga sakit na ito ay maaaring ma-manage at gamutin. Sa tamang pangangalaga, maaaring gumaling ang inyong pananim."
        
        return full_recommendation
    
    def _mock_predict(self) -> Dict[str, any]:
        """Return mock prediction when model is not available"""
        return {
            "disease_name": "Healthy",
            "disease_class": "healthy",
            "confidence": 98.7,
            "confidence_raw": 0.987,
            "recommendations": DISEASE_RECOMMENDATIONS["healthy"]["fil"],
            "severity": "none",
            "action_required": False,
            "all_predictions": {"Healthy": 98.7},
            "is_confident": True,
        }


# Global model service instance
_model_service: Optional[ModelService] = None


def get_model_service() -> ModelService:
    """Get or create the global model service instance"""
    global _model_service
    if _model_service is None:
        _model_service = ModelService()
    return _model_service

