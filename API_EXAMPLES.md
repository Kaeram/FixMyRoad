# API Examples and Use Cases

This document provides practical examples of using the FixMyRoad API.

## Table of Contents
1. [Basic Examples](#basic-examples)
2. [Complete Workflows](#complete-workflows)
3. [Priority System](#priority-system)
4. [Response Examples](#response-examples)

## Basic Examples

### 1. Image Validation

**Request:**
```bash
curl -X POST "http://localhost:8000/api/reports/validate-image" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@pothole.jpg"
```

**Success Response (200):**
```json
{
  "is_valid": true,
  "confidence": 0.85,
  "reason": null
}
```

**Failure Response (200):**
```json
{
  "is_valid": false,
  "confidence": 0.45,
  "reason": "Confidence 0.45 below threshold 0.7"
}
```

### 2. Submit Report Without Image

**Request:**
```bash
curl -X POST "http://localhost:8000/api/reports/submit" \
  -H "Content-Type: multipart/form-data" \
  -F "latitude=40.7128" \
  -F "longitude=-74.0060" \
  -F "description=Large pothole causing vehicle damage" \
  -F "severity=high" \
  -F "reporter_name=Jane Smith" \
  -F "reporter_email=jane@example.com" \
  -F "reporter_phone=+1234567890"
```

**Response (200):**
```json
{
  "ticket_id": "FMR-20260122-A1B2C3D4",
  "status": "pending",
  "priority": "medium",
  "latitude": 40.7128,
  "longitude": -74.006,
  "description": "Large pothole causing vehicle damage",
  "severity": "high",
  "image_url": null,
  "reporter_name": "Jane Smith",
  "reporter_email": "jane@example.com",
  "reporter_phone": "+1234567890",
  "created_at": "2026-01-22T10:30:00Z",
  "updated_at": "2026-01-22T10:30:00Z"
}
```

### 3. Submit Report With Image

**Request:**
```bash
curl -X POST "http://localhost:8000/api/reports/submit" \
  -F "latitude=40.7128" \
  -F "longitude=-74.0060" \
  -F "description=Deep pothole on Main St" \
  -F "severity=high" \
  -F "image=@pothole.jpg"
```

**Success Response (200):**
```json
{
  "ticket_id": "FMR-20260122-B5C6D7E8",
  "status": "pending",
  "priority": "high",
  "latitude": 40.7128,
  "longitude": -74.006,
  "description": "Deep pothole on Main St",
  "severity": "high",
  "image_url": "https://storage.example.com/potholes/pothole.jpg",
  "reporter_name": null,
  "reporter_email": null,
  "reporter_phone": null,
  "created_at": "2026-01-22T10:35:00Z",
  "updated_at": "2026-01-22T10:35:00Z"
}
```

**Error Response (400 - Invalid Image):**
```json
{
  "detail": "Invalid image: Image is too small. Minimum size is 100x100 pixels."
}
```

### 4. Track Ticket (Public)

**Request:**
```bash
curl http://localhost:8000/api/public/track/FMR-20260122-A1B2C3D4
```

**Response (200):**
```json
{
  "ticket_id": "FMR-20260122-A1B2C3D4",
  "status": "in_progress",
  "priority": "high",
  "latitude": 40.7128,
  "longitude": -74.006,
  "description": "Large pothole causing vehicle damage",
  "severity": "high",
  "created_at": "2026-01-22T10:30:00Z",
  "updated_at": "2026-01-22T11:00:00Z"
}
```

**Error Response (404):**
```json
{
  "detail": "Ticket FMR-20260122-INVALID not found"
}
```

### 5. Get Map Data (Admin)

**Request:**
```bash
curl http://localhost:8000/api/admin/map
```

**Response (200):**
```json
[
  {
    "ticket_id": "FMR-20260122-A1B2C3D4",
    "latitude": 40.7128,
    "longitude": -74.006,
    "status": "pending",
    "priority": "high",
    "severity": "high",
    "created_at": "2026-01-22T10:30:00Z"
  },
  {
    "ticket_id": "FMR-20260122-B5C6D7E8",
    "latitude": 40.7130,
    "longitude": -74.0065,
    "status": "in_progress",
    "priority": "critical",
    "severity": "medium",
    "created_at": "2026-01-22T10:35:00Z"
  }
]
```

### 6. Get Heatmap Data (Admin)

**Request:**
```bash
curl http://localhost:8000/api/admin/heatmap
```

**Response (200):**
```json
[
  {
    "latitude": 40.7128,
    "longitude": -74.006,
    "weight": 5
  },
  {
    "latitude": 40.7200,
    "longitude": -74.0100,
    "weight": 3
  },
  {
    "latitude": 40.7050,
    "longitude": -74.0020,
    "weight": 8
  }
]
```

### 7. Update Ticket Status (Admin)

**Request:**
```bash
curl -X PUT "http://localhost:8000/api/admin/tickets/FMR-20260122-A1B2C3D4/status" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress",
    "admin_notes": "Repair crew dispatched. ETA 2 hours."
  }'
```

**Response (200):**
```json
{
  "ticket_id": "FMR-20260122-A1B2C3D4",
  "status": "in_progress",
  "priority": "high",
  "latitude": 40.7128,
  "longitude": -74.006,
  "description": "Large pothole causing vehicle damage",
  "severity": "high",
  "image_url": null,
  "reporter_name": "Jane Smith",
  "reporter_email": "jane@example.com",
  "reporter_phone": "+1234567890",
  "created_at": "2026-01-22T10:30:00Z",
  "updated_at": "2026-01-22T11:00:00Z"
}
```

### 8. Get Ticket Details (Admin)

**Request:**
```bash
curl http://localhost:8000/api/admin/tickets/FMR-20260122-A1B2C3D4
```

**Response (200):**
```json
{
  "ticket_id": "FMR-20260122-A1B2C3D4",
  "status": "resolved",
  "priority": "high",
  "latitude": 40.7128,
  "longitude": -74.006,
  "description": "Large pothole causing vehicle damage",
  "severity": "high",
  "image_url": "https://storage.example.com/potholes/pothole.jpg",
  "reporter_name": "Jane Smith",
  "reporter_email": "jane@example.com",
  "reporter_phone": "+1234567890",
  "created_at": "2026-01-22T10:30:00Z",
  "updated_at": "2026-01-22T14:00:00Z"
}
```

## Complete Workflows

### Workflow 1: Standard Report Submission

```bash
# Step 1: Validate image first (optional but recommended)
curl -X POST "http://localhost:8000/api/reports/validate-image" \
  -F "image=@my_pothole.jpg"

# Response: {"is_valid": true, "confidence": 0.87, "reason": null}

# Step 2: Submit the report with validated image
curl -X POST "http://localhost:8000/api/reports/submit" \
  -F "latitude=40.7128" \
  -F "longitude=-74.0060" \
  -F "description=Pothole near intersection" \
  -F "severity=medium" \
  -F "reporter_email=user@example.com" \
  -F "image=@my_pothole.jpg"

# Response: {"ticket_id": "FMR-20260122-ABC123", ...}

# Step 3: Save ticket ID and track status later
curl http://localhost:8000/api/public/track/FMR-20260122-ABC123
```

### Workflow 2: Admin Daily Routine

```bash
# Morning: Check all new reports
curl http://localhost:8000/api/admin/map | jq '.[] | select(.status == "pending")'

# Identify high-priority areas
curl http://localhost:8000/api/admin/heatmap | jq 'sort_by(.weight) | reverse | .[0:5]'

# Dispatch crew to high-priority ticket
curl -X PUT "http://localhost:8000/api/admin/tickets/FMR-20260122-ABC123/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress", "admin_notes": "Crew dispatched to Main St"}'

# End of day: Mark completed repairs
curl -X PUT "http://localhost:8000/api/admin/tickets/FMR-20260122-ABC123/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "resolved", "admin_notes": "Repair completed at 3pm"}'
```

## Priority System

The system automatically calculates priority based on the density of reports in a 1km radius:

| Reports in Area | Priority Level |
|----------------|---------------|
| < 2            | LOW           |
| 2-4            | MEDIUM        |
| 5-9            | HIGH          |
| 10+            | CRITICAL      |

### Example: Priority Calculation

**Scenario:** 5 reports in a small area

```bash
# Report 1 (First in area)
curl -X POST "http://localhost:8000/api/reports/submit" \
  -F "latitude=40.7128" -F "longitude=-74.0060" -F "description=Pothole 1"
# Priority: LOW

# Report 2 (Second in area)
curl -X POST "http://localhost:8000/api/reports/submit" \
  -F "latitude=40.7129" -F "longitude=-74.0061" -F "description=Pothole 2"
# Priority: MEDIUM

# Report 5 (Fifth in area)
curl -X POST "http://localhost:8000/api/reports/submit" \
  -F "latitude=40.7130" -F "longitude=-74.0062" -F "description=Pothole 5"
# Priority: HIGH (area now has 5 reports)
```

## Status Transitions

Valid status transitions:
```
pending → in_progress → resolved
pending → rejected
in_progress → pending (if work stopped)
```

### Example Status Updates

```bash
# Accept report
curl -X PUT "http://localhost:8000/api/admin/tickets/FMR-20260122-ABC123/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress", "admin_notes": "Work started"}'

# Complete repair
curl -X PUT "http://localhost:8000/api/admin/tickets/FMR-20260122-ABC123/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "resolved", "admin_notes": "Repair completed successfully"}'

# Reject invalid report
curl -X PUT "http://localhost:8000/api/admin/tickets/FMR-20260122-XYZ789/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "rejected", "admin_notes": "Not a pothole - speed bump"}'
```

## Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Submit a report
def submit_report(lat, lon, description, image_path=None):
    data = {
        'latitude': lat,
        'longitude': lon,
        'description': description,
        'severity': 'medium'
    }
    
    files = {}
    if image_path:
        files['image'] = open(image_path, 'rb')
    
    response = requests.post(f"{BASE_URL}/api/reports/submit", data=data, files=files)
    return response.json()

# Track a ticket
def track_ticket(ticket_id):
    response = requests.get(f"{BASE_URL}/api/public/track/{ticket_id}")
    return response.json()

# Usage
result = submit_report(40.7128, -74.0060, "Large pothole on Main St", "photo.jpg")
print(f"Ticket ID: {result['ticket_id']}")

status = track_ticket(result['ticket_id'])
print(f"Status: {status['status']}")
```

## Error Handling

### Common Error Responses

**400 Bad Request:**
```json
{
  "detail": "Invalid image: Image is too small. Minimum size is 100x100 pixels."
}
```

**404 Not Found:**
```json
{
  "detail": "Ticket FMR-20260122-INVALID not found"
}
```

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "latitude"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Failed to create report: Database connection failed"
}
```
