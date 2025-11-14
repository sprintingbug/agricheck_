"""
Image validation utilities for leaf disease detection
Validates image quality, blur, and basic leaf detection
"""
import cv2
import numpy as np
from PIL import Image
import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

def calculate_blur_score(image_path: str) -> float:
    """
    Calculate blur score using Laplacian variance.
    Higher score = less blur (sharper image)
    Lower score = more blur (blurry image)
    
    Returns:
        Blur score (typically 0-1000+, higher is better)
    """
    try:
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            return 0.0
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Calculate Laplacian variance
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        return float(laplacian_var)
    except Exception as e:
        logger.error(f"Error calculating blur score: {e}")
        return 0.0

def is_image_blurry(image_path: str, threshold: float = 50.0) -> Tuple[bool, float]:
    """
    Check if image is blurry.
    Lower threshold = more lenient (accepts more images)
    
    Args:
        image_path: Path to image file
        threshold: Blur threshold (default: 50.0, lower = more lenient)
    
    Returns:
        (is_blurry, blur_score)
    """
    blur_score = calculate_blur_score(image_path)
    is_blurry = blur_score < threshold
    return is_blurry, blur_score

def detect_leaf_features(image_path: str) -> Dict[str, float]:
    """
    Basic leaf detection using color and edge analysis.
    Rice leaves are typically green and have clear edges.
    
    Returns:
        Dictionary with detection scores
    """
    try:
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            return {"green_ratio": 0.0, "edge_density": 0.0, "is_leaf": False}
        
        # Convert to HSV for better green detection
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Define green color range (for rice leaves)
        # Lower green: [40, 40, 40]
        # Upper green: [80, 255, 255]
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])
        
        # Create mask for green pixels
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        green_ratio = np.sum(green_mask > 0) / (img.shape[0] * img.shape[1])
        
        # Calculate edge density (leaves have many edges)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (img.shape[0] * img.shape[1])
        
        # Basic leaf detection: has green content and reasonable edges (more lenient)
        # Rice leaves typically have 15-80% green coverage and visible edges
        # Lower thresholds to accept more recognizable leaf images
        is_leaf = green_ratio > 0.15 and edge_density > 0.05
        
        return {
            "green_ratio": float(green_ratio),
            "edge_density": float(edge_density),
            "is_leaf": is_leaf
        }
    except Exception as e:
        logger.error(f"Error detecting leaf features: {e}")
        return {"green_ratio": 0.0, "edge_density": 0.0, "is_leaf": False}

def validate_image_for_scan(image_path: str) -> Tuple[bool, str]:
    """
    Validate image for leaf disease scanning.
    
    Checks:
    1. Image is not too blurry
    2. Image appears to be a leaf (has green and edges)
    
    Args:
        image_path: Path to image file
    
    Returns:
        (is_valid, error_message)
    """
    try:
        # Check if image can be opened
        try:
            img = Image.open(image_path)
            img.verify()
        except Exception as e:
            return False, "Hindi ma-open ang image. Pakisiguro na valid ang image file."
        
        # Check blur (more lenient threshold - focus on recognizable leaf with clear markings)
        # Lower threshold accepts images that are recognizable as leaves even if slightly blurry
        is_blurry, blur_score = is_image_blurry(image_path, threshold=50.0)
        if is_blurry:
            # Only reject if extremely blurry (very low score)
            if blur_score < 20.0:
                return False, f"Ang image ay masyadong malabo (blur score: {blur_score:.1f}). Pakikumpara sa mas malinaw na litrato ng dahon ng palay kung saan makikita ang markings."
            # If moderately blurry but still recognizable, warn but allow
            logger.info(f"Image has moderate blur (score: {blur_score:.1f}) but will be processed")
        
        # Check if it's a leaf (more lenient - focus on recognizable leaf)
        leaf_features = detect_leaf_features(image_path)
        if not leaf_features["is_leaf"]:
            return False, f"Ang image ay hindi mukhang dahon ng palay. Ang image ay dapat na dahon lamang ng palay na makikita ang markings. Pakikumpara sa dahon ng palay."
        
        return True, ""
    except Exception as e:
        logger.error(f"Error validating image: {e}")
        return False, "May problema sa pag-validate ng image. Pakisubukang muli."

