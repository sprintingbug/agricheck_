from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone
from app.db.session import get_db
from app.db.models import Scan, User
from app.users.routes import get_current_user
from app.scans.schemas import ScanIn, ScanOut, ScanHistoryOut
from app.ml.model_service import get_model_service
from app.ml.image_validation import validate_image_for_scan
import os
import uuid
import shutil
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/scans", tags=["scans"])

# Directory to store uploaded images
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/scan", response_model=ScanOut, status_code=201)
async def scan_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload an image for disease detection.
    Uses ML model to detect plant diseases.
    """
    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ang file ay dapat na image. Pakipili ng image file."
        )
    
    # Generate unique filename
    file_ext = os.path.splitext(file.filename or 'image.jpg')[1]
    filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    try:
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Validate image before processing
        is_valid, error_message = validate_image_for_scan(file_path)
        if not is_valid:
            # Clean up file
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
        
        # Run ML model prediction with AI-enhanced analysis
        # Higher confidence threshold for better accuracy
        model_service = get_model_service()
        
        # Check if model is loaded
        if model_service.model is None:
            logger.warning("Model not loaded - using mock predictions")
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Ang ML model ay hindi pa na-load. Pakisubukang muli pagkatapos ng ilang segundo o i-restart ang backend server."
            )
        
        prediction_result = model_service.predict(file_path, confidence_threshold=0.65)
        
        # Validate prediction confidence (stricter for accuracy)
        confidence = prediction_result.get("confidence", 0.0)
        all_predictions = prediction_result.get("all_predictions", {})
        
        # Reject if confidence is too low (< 50%)
        if confidence < 50.0:
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mababa ang kumpiyansa sa diagnosis ({confidence:.1f}%). Ang image ay maaaring hindi malinaw o hindi dahon ng palay. Pakikumpara sa mas malinaw at nakatutok na litrato ng dahon ng palay."
            )
        
        # Check if prediction is uncertain (second prediction is close)
        sorted_predictions = sorted(all_predictions.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_predictions) > 1:
            top_conf = sorted_predictions[0][1]
            second_conf = sorted_predictions[1][1]
            if top_conf - second_conf < 15.0:  # Less than 15% difference
                logger.warning(f"Uncertain prediction: {top_conf:.1f}% vs {second_conf:.1f}%")
                if top_conf < 60.0:  # If top is also low confidence
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Hindi tiyak ang diagnosis ({top_conf:.1f}% vs {second_conf:.1f}%). Ang image ay maaaring hindi malinaw o hindi dahon ng palay. Pakikumpara sa mas malinaw na litrato ng dahon ng palay."
                    )
        
        # Extract prediction results
        disease_name = prediction_result.get("disease_name", "Unknown")
        confidence = prediction_result.get("confidence", 0.0)
        recommendations = prediction_result.get("recommendations", "Please consult with an agricultural expert.")
        
        # Log prediction details for debugging
        logger.info(f"Prediction: {disease_name} ({confidence}% confidence)")
        logger.info(f"All predictions: {prediction_result.get('all_predictions', {})}")
        
        # Warn if confidence is low but above rejection threshold
        if confidence < 60.0:
            logger.warning(f"Low confidence prediction: {confidence}% - may need expert consultation")
        if not prediction_result.get("is_confident", False):
            logger.warning(f"Confidence below threshold: {confidence}%")
        
        # Create scan record
        scan = Scan(
            user_id=current_user.id,
            image_path=file_path,
            disease_name=disease_name,
            confidence=confidence,
            recommendations=recommendations
        )
        db.add(scan)
        db.commit()
        db.refresh(scan)
        
        return ScanOut(
            id=scan.id,
            user_id=scan.user_id,
            image_path=scan.image_path,
            disease_name=scan.disease_name,
            confidence=scan.confidence,
            recommendations=scan.recommendations,
            created_at=scan.created_at
        )
    except HTTPException:
        # Re-raise HTTP exceptions (they already have proper error messages)
        raise
    except Exception as e:
        # Clean up file if error occurs
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Log the actual error for debugging
        logger.error(f"Error processing scan: {type(e).__name__}: {str(e)}", exc_info=True)
        
        # Provide more informative error message
        error_detail = f"May problema sa pag-process ng scan: {str(e)}"
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail
        )

@router.post("", response_model=ScanOut, status_code=201)
def save_scan(
    payload: ScanIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Save a scan result (for when scan is done separately and result is saved later).
    """
    scan = Scan(
        user_id=current_user.id,
        image_path="",  # Will be set if image is uploaded separately
        disease_name=payload.disease_name,
        confidence=payload.confidence,
        recommendations=payload.recommendations
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    
    return ScanOut(
        id=scan.id,
        user_id=scan.user_id,
        image_path=scan.image_path,
        disease_name=scan.disease_name,
        confidence=scan.confidence,
        recommendations=scan.recommendations,
        created_at=scan.created_at
    )

@router.get("/history", response_model=ScanHistoryOut, status_code=200)
def get_scan_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    disease_filter: Optional[str] = Query(None, alias="disease"),
    sort_by: str = Query("date", regex="^(date|confidence)$")
):
    """
    Get the authenticated user's scan history with filtering and sorting.
    - disease_filter: Filter by disease name (e.g., "Healthy", "Leaf Blight")
    - sort_by: Sort by "date" (desc) or "confidence" (desc)
    """
    query = db.query(Scan).filter(Scan.user_id == current_user.id)
    
    # Apply disease filter if provided
    if disease_filter:
        query = query.filter(Scan.disease_name.ilike(f"%{disease_filter}%"))
    
    # Apply sorting
    if sort_by == "confidence":
        query = query.order_by(Scan.confidence.desc())
    else:  # default to date
        query = query.order_by(Scan.created_at.desc())
    
    # Get total count (before limit/offset)
    total = query.count()
    
    # Apply pagination
    scans = query.limit(limit).offset(offset).all()
    
    return ScanHistoryOut(
        scans=[
            ScanOut(
                id=scan.id,
                user_id=scan.user_id,
                image_path=scan.image_path,
                disease_name=scan.disease_name,
                confidence=scan.confidence,
                recommendations=scan.recommendations,
                created_at=scan.created_at
            )
            for scan in scans
        ],
        total=total
    )

@router.get("/image/{scan_id}")
def get_scan_image(
    scan_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the image for a specific scan. Only accessible by the scan owner.
    """
    scan = db.query(Scan).filter(
        Scan.id == scan_id,
        Scan.user_id == current_user.id
    ).first()
    
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hindi nahanap ang scan. Pakisubukang muli."
        )
    
    if not scan.image_path or not os.path.exists(scan.image_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hindi nahanap ang image file. Pakisubukang muli."
        )
    
    # Determine media type from file extension
    ext = os.path.splitext(scan.image_path)[1].lower()
    media_type = "image/jpeg"
    if ext == ".png":
        media_type = "image/png"
    elif ext == ".gif":
        media_type = "image/gif"
    elif ext == ".webp":
        media_type = "image/webp"
    
    return FileResponse(
        scan.image_path,
        media_type=media_type,
        filename=os.path.basename(scan.image_path)
    )

@router.get("/diseases")
def get_unique_diseases(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of unique disease names for the authenticated user.
    """
    diseases = db.query(Scan.disease_name).filter(
        Scan.user_id == current_user.id
    ).distinct().all()
    
    return {
        "diseases": [disease[0] for disease in diseases]
    }

@router.delete("/{scan_id}", status_code=200)
def delete_scan(
    scan_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a scan by ID. Only the owner can delete their own scans.
    """
    # Find scan and verify ownership
    scan = db.query(Scan).filter(
        Scan.id == scan_id,
        Scan.user_id == current_user.id
    ).first()
    
    if not scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hindi nahanap ang scan o hindi ka may-ari ng scan na ito."
        )
    
    # Delete image file if it exists
    try:
        if scan.image_path and os.path.exists(scan.image_path):
            os.remove(scan.image_path)
            logger.info(f"Deleted image file: {scan.image_path}")
    except Exception as e:
        logger.warning(f"Could not delete image file {scan.image_path}: {e}")
        # Continue with database deletion even if file deletion fails
    
    # Delete from database
    db.delete(scan)
    db.commit()
    
    logger.info(f"Deleted scan {scan_id} for user {current_user.id}")
    
    return {
        "message": "Matagumpay na na-delete ang scan.",
        "deleted_scan_id": scan_id
    }

