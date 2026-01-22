import pytest
from io import BytesIO
from PIL import Image
from backend.utils.image_validator import validate_image_format, mock_ml_validation
from backend.models.schemas import ImageValidationResult


def create_test_image(width=500, height=500, format="JPEG"):
    """Helper function to create test image."""
    img = Image.new('RGB', (width, height), color='red')
    buffer = BytesIO()
    img.save(buffer, format=format)
    return buffer.getvalue()


def test_validate_image_format_valid_jpeg():
    """Test validation of valid JPEG image."""
    image_data = create_test_image(500, 500, "JPEG")
    is_valid, error = validate_image_format(image_data)
    assert is_valid is True
    assert error == ""


def test_validate_image_format_valid_png():
    """Test validation of valid PNG image."""
    image_data = create_test_image(500, 500, "PNG")
    is_valid, error = validate_image_format(image_data)
    assert is_valid is True
    assert error == ""


def test_validate_image_format_too_small():
    """Test rejection of too small image."""
    image_data = create_test_image(50, 50, "JPEG")
    is_valid, error = validate_image_format(image_data)
    assert is_valid is False
    assert "too small" in error.lower()


def test_validate_image_format_too_large():
    """Test rejection of too large image."""
    image_data = create_test_image(6000, 6000, "JPEG")
    is_valid, error = validate_image_format(image_data)
    assert is_valid is False
    assert "too large" in error.lower()


def test_mock_ml_validation_valid_image():
    """Test ML validation accepts valid image."""
    image_data = create_test_image(1000, 1000, "JPEG")
    result = mock_ml_validation(image_data)
    
    assert isinstance(result, ImageValidationResult)
    assert result.is_valid is True
    assert result.confidence > 0.0
    assert result.reason is None


def test_mock_ml_validation_invalid_format():
    """Test ML validation rejects invalid format."""
    # Invalid image data
    invalid_data = b"not an image"
    result = mock_ml_validation(invalid_data)
    
    assert isinstance(result, ImageValidationResult)
    assert result.is_valid is False
    assert result.confidence == 0.0
    assert result.reason is not None


def test_mock_ml_validation_confidence_scoring():
    """Test that ML validation produces reasonable confidence scores."""
    # Larger image should have higher confidence
    small_image = create_test_image(200, 200, "JPEG")
    large_image = create_test_image(2000, 2000, "JPEG")
    
    small_result = mock_ml_validation(small_image)
    large_result = mock_ml_validation(large_image)
    
    # Both should be valid
    assert small_result.is_valid is True
    assert large_result.is_valid is True
    
    # Confidence should be between 0 and 1
    assert 0.0 <= small_result.confidence <= 1.0
    assert 0.0 <= large_result.confidence <= 1.0
