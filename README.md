# FixMyRoad - Smart Pothole Reporting System

A Python-based backend MVP for intelligent pothole reporting using FastAPI and Supabase.

## Features

- **Smart Image Validation**: ML-based validation (mock implementation for MVP) to ensure uploaded images are valid
- **Automatic Ticket Generation**: Unique ticket IDs for every valid report
- **Area-based Prioritization**: Intelligent priority calculation based on complaint density in the area
- **Admin Dashboard APIs**: Map view, heatmap, and status management
- **Public Tracking**: Allow users to track their reports using ticket ID
- **Clean Architecture**: Modular, maintainable code structure

## Architecture

```
backend/
├── api/                 # API endpoints
│   ├── reports.py      # Report submission and image validation
│   ├── admin.py        # Admin endpoints (map, heatmap, status updates)
│   └── public.py       # Public tracking endpoint
├── models/             # Pydantic models and schemas
│   └── schemas.py      # Data models for API validation
├── services/           # Business logic layer
│   └── pothole_service.py  # Core pothole report service
├── config/             # Configuration
│   ├── settings.py     # Application settings
│   └── database.py     # Supabase client
├── utils/              # Utility functions
│   ├── image_validator.py  # Image validation and mock ML
│   └── ticket_utils.py     # Ticket ID generation
└── main.py             # FastAPI application entry point
```

## Prerequisites

- Python 3.8+
- Supabase account (or PostgreSQL database)
- pip package manager

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/Kaeram/FixMyRoad.git
cd FixMyRoad
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

5. **Set up database**
   
   Run the SQL schema in your Supabase SQL editor:
```bash
# Connect to your Supabase project and run:
database/schema.sql
```

## Configuration

Edit `.env` file with your configuration:

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# Application Configuration
APP_NAME=FixMyRoad API
APP_VERSION=1.0.0
DEBUG=True

# ML Model Configuration
ML_MODEL_CONFIDENCE_THRESHOLD=0.7
```

## Running the Application

### Development Server

```bash
cd /path/to/FixMyRoad
python -m backend.main
```

Or with uvicorn directly:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## API Endpoints

### Public Endpoints

#### 1. Validate Image
```http
POST /api/reports/validate-image
Content-Type: multipart/form-data

Body:
- image: file (JPEG/PNG)

Response: {
  "is_valid": true,
  "confidence": 0.85,
  "reason": null
}
```

#### 2. Submit Report
```http
POST /api/reports/submit
Content-Type: multipart/form-data

Body:
- latitude: float (required)
- longitude: float (required)
- description: string (optional)
- severity: string (optional, default: "medium")
- reporter_name: string (optional)
- reporter_email: string (optional)
- reporter_phone: string (optional)
- image: file (optional, JPEG/PNG)

Response: {
  "ticket_id": "FMR-20260122-A1B2C3D4",
  "status": "pending",
  "priority": "medium",
  "latitude": 40.7128,
  "longitude": -74.0060,
  ...
}
```

#### 3. Track Ticket
```http
GET /api/public/track/{ticket_id}

Response: {
  "ticket_id": "FMR-20260122-A1B2C3D4",
  "status": "pending",
  "priority": "medium",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "description": "Large pothole on Main St",
  "created_at": "2026-01-22T10:30:00Z",
  "updated_at": "2026-01-22T10:30:00Z"
}
```

### Admin Endpoints

#### 4. Get Map Data
```http
GET /api/admin/map

Response: [
  {
    "ticket_id": "FMR-20260122-A1B2C3D4",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "status": "pending",
    "priority": "high",
    "severity": "medium",
    "created_at": "2026-01-22T10:30:00Z"
  },
  ...
]
```

#### 5. Get Heatmap Data
```http
GET /api/admin/heatmap

Response: [
  {
    "latitude": 40.7128,
    "longitude": -74.0060,
    "weight": 5  # Number of reports in this area
  },
  ...
]
```

#### 6. Update Ticket Status
```http
PUT /api/admin/tickets/{ticket_id}/status
Content-Type: application/json

Body: {
  "status": "in_progress",
  "admin_notes": "Repair crew dispatched"
}

Response: {
  "ticket_id": "FMR-20260122-A1B2C3D4",
  "status": "in_progress",
  ...
}
```

#### 7. Get Ticket Details
```http
GET /api/admin/tickets/{ticket_id}

Response: {
  "ticket_id": "FMR-20260122-A1B2C3D4",
  "status": "in_progress",
  "priority": "high",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "reporter_name": "John Doe",
  "reporter_email": "john@example.com",
  ...
}
```

## Data Models

### Ticket Status
- `pending`: Newly submitted, awaiting review
- `in_progress`: Being worked on
- `resolved`: Fixed/completed
- `rejected`: Invalid or duplicate report

### Priority Levels (Area-based)
Priority is automatically calculated based on complaint density:
- `low`: < 2 reports in 1km radius
- `medium`: 2-4 reports in 1km radius
- `high`: 5-9 reports in 1km radius
- `critical`: 10+ reports in 1km radius

## Image Validation

The MVP includes a mock ML validation system that:
1. Validates image format (JPEG/PNG)
2. Checks image dimensions (100x100 to 5000x5000 pixels)
3. Verifies file size (max 10MB)
4. Simulates ML confidence scoring
5. Rejects images below confidence threshold (0.7)

### Future: Real ML Implementation
For production, replace `mock_ml_validation` in `backend/utils/image_validator.py` with a real ML model (e.g., TensorFlow, PyTorch) trained to detect potholes.

## Testing

Run tests (when implemented):
```bash
pytest backend/tests/
```

## Database Schema

The application uses a single table `pothole_reports` with the following structure:

- `id`: Auto-incrementing primary key
- `ticket_id`: Unique ticket identifier
- `status`: Current status (pending/in_progress/resolved/rejected)
- `priority`: Area-based priority (low/medium/high/critical)
- `latitude`: GPS coordinate
- `longitude`: GPS coordinate
- `description`: User description
- `severity`: User-reported severity
- `image_url`: URL to uploaded image
- `reporter_name`: Reporter name (optional)
- `reporter_email`: Reporter email (optional)
- `reporter_phone`: Reporter phone (optional)
- `admin_notes`: Admin notes and updates
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

## Production Considerations

For production deployment, consider:

1. **Authentication & Authorization**: Implement JWT/OAuth for admin endpoints
2. **Image Storage**: Use Supabase Storage or S3 for actual image uploads
3. **Real ML Model**: Replace mock validation with trained model
4. **Rate Limiting**: Add rate limiting to prevent abuse
5. **Caching**: Implement caching for map/heatmap data
6. **Monitoring**: Add logging and monitoring (e.g., Sentry)
7. **CORS**: Configure proper CORS origins (not wildcard)
8. **Environment**: Use proper environment separation (dev/staging/prod)
9. **Database**: Add connection pooling and optimization
10. **API Keys**: Secure admin endpoints with API keys

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please open an issue on GitHub.