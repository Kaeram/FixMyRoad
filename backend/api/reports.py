from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import Optional
from supabase import Client
from backend.models.schemas import (
    PotholeReportCreate,
    PotholeReportResponse,
    ImageValidationResult,
)
from backend.services import PotholeService
from backend.utils import mock_ml_validation
from backend.config.database import get_supabase


router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.post("/validate-image", response_model=ImageValidationResult)
async def validate_image(
    image: UploadFile = File(..., description="Pothole image to validate")
):
    """Validate pothole image using ML model.
    
    This endpoint validates if the uploaded image is valid and contains a pothole.
    Uses a mock ML model for the MVP.
    
    Args:
        image: Image file to validate
        
    Returns:
        Validation result with confidence score
    """
    try:
        # Read image data
        image_data = await image.read()
        
        # Validate using mock ML model
        validation_result = mock_ml_validation(image_data)
        
        return validation_result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image validation failed: {str(e)}")


@router.post("/submit", response_model=PotholeReportResponse)
async def submit_report(
    latitude: float = Form(..., description="Latitude coordinate"),
    longitude: float = Form(..., description="Longitude coordinate"),
    description: Optional[str] = Form(None, description="Description of the pothole"),
    severity: Optional[str] = Form("medium", description="Severity level"),
    reporter_name: Optional[str] = Form(None, description="Reporter name"),
    reporter_email: Optional[str] = Form(None, description="Reporter email"),
    reporter_phone: Optional[str] = Form(None, description="Reporter phone"),
    image: Optional[UploadFile] = File(None, description="Pothole image"),
    supabase: Client = Depends(get_supabase),
):
    """Submit a pothole report.
    
    This endpoint:
    1. Validates the image (if provided) using ML
    2. Discards invalid images
    3. Creates a ticket with unique ID
    4. Stores in PostgreSQL via Supabase
    5. Calculates priority based on area complaint density
    
    Args:
        latitude: Location latitude
        longitude: Location longitude
        description: Optional description
        severity: Severity level
        reporter_name: Optional reporter name
        reporter_email: Optional reporter email
        reporter_phone: Optional reporter phone
        image: Optional pothole image
        supabase: Database client
        
    Returns:
        Created report with ticket ID
    """
    image_url = None
    
    # If image is provided, validate it
    if image:
        try:
            image_data = await image.read()
            validation_result = mock_ml_validation(image_data)
            
            if not validation_result.is_valid:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid image: {validation_result.reason}"
                )
            
            # In a real implementation, upload to storage and get URL
            # For MVP, we simulate this with a placeholder
            # TODO: Implement actual image upload to Supabase Storage or S3
            image_url = f"https://storage.example.com/potholes/{image.filename}"
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Image processing failed: {str(e)}")
    
    # Create report data
    report_data = PotholeReportCreate(
        latitude=latitude,
        longitude=longitude,
        description=description,
        severity=severity,
        reporter_name=reporter_name,
        reporter_email=reporter_email,
        reporter_phone=reporter_phone,
    )
    
    # Create report
    service = PotholeService(supabase)
    try:
        report = await service.create_report(report_data, image_url)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create report: {str(e)}")
