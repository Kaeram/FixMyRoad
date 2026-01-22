#!/usr/bin/env python3
"""
Manual test script for FixMyRoad API.

This script tests all endpoints without requiring a real Supabase connection.
It uses mock/test data to validate the API structure and responses.
"""

import requests
import json
from io import BytesIO
from PIL import Image


BASE_URL = "http://localhost:8000"


def create_test_image():
    """Create a test image for validation."""
    img = Image.new('RGB', (500, 500), color='blue')
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    buffer.seek(0)
    return buffer


def test_root():
    """Test root endpoint."""
    print("\n=== Testing Root Endpoint ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200


def test_health():
    """Test health check endpoint."""
    print("\n=== Testing Health Endpoint ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200


def test_validate_image():
    """Test image validation endpoint."""
    print("\n=== Testing Image Validation ===")
    
    image_buffer = create_test_image()
    files = {'image': ('test.jpg', image_buffer, 'image/jpeg')}
    
    response = requests.post(f"{BASE_URL}/api/reports/validate-image", files=files)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    
    result = response.json()
    assert 'is_valid' in result
    assert 'confidence' in result


def test_submit_report_without_supabase():
    """Test report submission endpoint structure (will fail without Supabase)."""
    print("\n=== Testing Report Submission Structure ===")
    
    data = {
        'latitude': 40.7128,
        'longitude': -74.0060,
        'description': 'Large pothole on Main Street',
        'severity': 'high',
        'reporter_name': 'Test User',
        'reporter_email': 'test@example.com'
    }
    
    response = requests.post(f"{BASE_URL}/api/reports/submit", data=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}...")
    
    # Expected to fail without Supabase, but structure is correct
    print("Note: This endpoint requires Supabase connection to work fully")


def test_track_ticket_structure():
    """Test ticket tracking endpoint structure."""
    print("\n=== Testing Ticket Tracking Structure ===")
    
    response = requests.get(f"{BASE_URL}/api/public/track/FMR-20260122-TEST1234")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}...")
    
    # Expected to fail without Supabase
    print("Note: This endpoint requires Supabase connection to work fully")


def test_admin_endpoints_structure():
    """Test admin endpoints structure."""
    print("\n=== Testing Admin Endpoints Structure ===")
    
    # Test map endpoint
    print("\n-- Map Endpoint --")
    response = requests.get(f"{BASE_URL}/api/admin/map")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}...")
    
    # Test heatmap endpoint
    print("\n-- Heatmap Endpoint --")
    response = requests.get(f"{BASE_URL}/api/admin/heatmap")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}...")
    
    print("Note: These endpoints require Supabase connection to work fully")


def main():
    """Run all tests."""
    print("=" * 60)
    print("FixMyRoad API Manual Test Suite")
    print("=" * 60)
    
    try:
        test_root()
        test_health()
        test_validate_image()
        test_submit_report_without_supabase()
        test_track_ticket_structure()
        test_admin_endpoints_structure()
        
        print("\n" + "=" * 60)
        print("Tests completed!")
        print("=" * 60)
        print("\nNOTE: Some endpoints require a working Supabase connection.")
        print("To test fully, configure Supabase credentials in .env file")
        
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
