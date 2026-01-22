from PIL import Image
import io
from typing import Tuple
from backend.models.schemas import ImageValidationResult
from backend.config import settings


def validate_image_format(image_data: bytes) -> Tuple[bool, str]:
    """Validate image format and basic properties.
    
    Args:
        image_data: Raw image bytes
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        image = Image.open(io.BytesIO(image_data))
        
        # Check if it's a valid image format
        if image.format not in ['JPEG', 'PNG']:
            return False, "Invalid image format. Only JPEG and PNG are supported."
        
        # Check image dimensions (should be reasonable)
        width, height = image.size
        if width < 100 or height < 100:
            return False, "Image is too small. Minimum size is 100x100 pixels."
        
        if width > 5000 or height > 5000:
            return False, "Image is too large. Maximum size is 5000x5000 pixels."
        
        # Check file size (max 10MB)
        if len(image_data) > 10 * 1024 * 1024:
            return False, "Image file size is too large. Maximum is 10MB."
        
        return True, ""
    except Exception as e:
        return False, f"Failed to process image: {str(e)}"


def mock_ml_validation(image_data: bytes) -> ImageValidationResult:
    """Mock ML model for pothole image validation.
    
    In a production system, this would use a trained ML model to detect
    if the image actually contains a pothole.
    
    For the MVP, we use a simple mock that:
    - Validates image format
    - Simulates ML confidence scoring
    - Returns validation result
    
    Args:
        image_data: Raw image bytes
        
    Returns:
        ImageValidationResult with validation status
    """
    # First validate basic image format
    is_valid_format, error_msg = validate_image_format(image_data)
    
    if not is_valid_format:
        return ImageValidationResult(
            is_valid=False,
            confidence=0.0,
            reason=error_msg
        )
    
    # Mock ML validation - in real implementation, this would be:
    # model.predict(preprocess_image(image_data))
    # For MVP, we accept all valid format images as containing potholes
    # with a simulated confidence score
    
    try:
        image = Image.open(io.BytesIO(image_data))
        
        # Simulate ML confidence based on image properties
        # In reality, this would be from the ML model's prediction
        width, height = image.size
        
        # Mock: larger, clearer images get higher confidence
        base_confidence = 0.75
        size_factor = min(1.0, (width * height) / (1000 * 1000))
        confidence = base_confidence + (size_factor * 0.2)
        confidence = min(0.95, confidence)  # Cap at 0.95
        
        # Check against threshold
        threshold = settings.ml_model_confidence_threshold
        is_valid = confidence >= threshold
        
        return ImageValidationResult(
            is_valid=is_valid,
            confidence=round(confidence, 2),
            reason=None if is_valid else f"Confidence {confidence:.2f} below threshold {threshold}"
        )
    except Exception as e:
        return ImageValidationResult(
            is_valid=False,
            confidence=0.0,
            reason=f"ML validation failed: {str(e)}"
        )
