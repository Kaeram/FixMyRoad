# FixMyRoad API - Quick Start Guide

## Setup Instructions

### 1. Prerequisites
- Python 3.8 or higher
- Supabase account (create at https://supabase.com)
- Git

### 2. Installation Steps

```bash
# Clone the repository
git clone https://github.com/Kaeram/FixMyRoad.git
cd FixMyRoad

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Supabase Setup

1. **Create a Supabase Project**
   - Go to https://supabase.com
   - Create a new project
   - Wait for the project to be ready

2. **Set up the Database**
   - Go to the SQL Editor in your Supabase dashboard
   - Copy and paste the contents of `database/schema.sql`
   - Run the SQL script to create the `pothole_reports` table

3. **Get Your Credentials**
   - Go to Project Settings → API
   - Copy your Project URL and anon/public key

4. **Configure Environment Variables**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env with your credentials
   nano .env
   ```
   
   Update the following in `.env`:
   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your_anon_key_here
   ```

### 4. Run the Application

```bash
# Start the server
python -m backend.main

# Or with uvicorn directly
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## Testing the API

### Using the Interactive Documentation

The easiest way to test the API is through the Swagger UI:

1. Open http://localhost:8000/docs in your browser
2. Expand any endpoint
3. Click "Try it out"
4. Fill in the required parameters
5. Click "Execute" to test

### Using curl Commands

#### 1. Check API Status
```bash
curl http://localhost:8000/
curl http://localhost:8000/health
```

#### 2. Validate an Image
```bash
# Create a test image first
convert -size 500x500 xc:blue test_pothole.jpg

# Validate it
curl -X POST "http://localhost:8000/api/reports/validate-image" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@test_pothole.jpg"
```

#### 3. Submit a Pothole Report
```bash
curl -X POST "http://localhost:8000/api/reports/submit" \
  -H "Content-Type: multipart/form-data" \
  -F "latitude=40.7128" \
  -F "longitude=-74.0060" \
  -F "description=Large pothole on Main Street" \
  -F "severity=high" \
  -F "reporter_name=John Doe" \
  -F "reporter_email=john@example.com" \
  -F "image=@test_pothole.jpg"
```

Response will include a ticket ID like:
```json
{
  "ticket_id": "FMR-20260122-A1B2C3D4",
  "status": "pending",
  "priority": "medium",
  ...
}
```

#### 4. Track a Ticket (Public)
```bash
curl http://localhost:8000/api/public/track/FMR-20260122-A1B2C3D4
```

#### 5. Get Map Data (Admin)
```bash
curl http://localhost:8000/api/admin/map
```

#### 6. Get Heatmap Data (Admin)
```bash
curl http://localhost:8000/api/admin/heatmap
```

#### 7. Update Ticket Status (Admin)
```bash
curl -X PUT "http://localhost:8000/api/admin/tickets/FMR-20260122-A1B2C3D4/status" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress",
    "admin_notes": "Repair crew dispatched to location"
  }'
```

### Using Python Script

Run the included test script:
```bash
python test_api.py
```

## API Workflow Example

### Complete User Journey

1. **User takes a photo of a pothole**

2. **User validates the image** (optional)
   ```bash
   curl -X POST "http://localhost:8000/api/reports/validate-image" \
     -F "image=@pothole_photo.jpg"
   ```

3. **User submits the report**
   ```bash
   curl -X POST "http://localhost:8000/api/reports/submit" \
     -F "latitude=40.7128" \
     -F "longitude=-74.0060" \
     -F "description=Deep pothole causing damage" \
     -F "severity=high" \
     -F "reporter_email=user@example.com" \
     -F "image=@pothole_photo.jpg"
   ```
   
   Receives ticket ID: `FMR-20260122-A1B2C3D4`

4. **User tracks their report**
   ```bash
   curl http://localhost:8000/api/public/track/FMR-20260122-A1B2C3D4
   ```

5. **Admin views all reports on map**
   ```bash
   curl http://localhost:8000/api/admin/map
   ```

6. **Admin checks high-priority areas (heatmap)**
   ```bash
   curl http://localhost:8000/api/admin/heatmap
   ```

7. **Admin updates ticket status**
   ```bash
   curl -X PUT "http://localhost:8000/api/admin/tickets/FMR-20260122-A1B2C3D4/status" \
     -H "Content-Type: application/json" \
     -d '{"status": "resolved", "admin_notes": "Pothole repaired"}'
   ```

## Troubleshooting

### Common Issues

**Problem**: `Connection refused` errors
- **Solution**: Make sure Supabase credentials are correct in `.env`
- Check that your Supabase project is running
- Verify the URL and API key

**Problem**: Image validation always fails
- **Solution**: Ensure image is JPEG or PNG format
- Check image size is between 100x100 and 5000x5000 pixels
- Verify file size is under 10MB

**Problem**: Server won't start
- **Solution**: Check if port 8000 is already in use
- Try a different port: `uvicorn backend.main:app --port 8001`
- Check Python version is 3.8+

**Problem**: Dependencies won't install
- **Solution**: Upgrade pip: `pip install --upgrade pip`
- Try installing dependencies one at a time
- Check Python version compatibility

## Architecture Overview

```
┌─────────────┐     ┌──────────────┐     ┌───────────┐
│   Client    │────▶│   FastAPI    │────▶│ Supabase  │
│ (Mobile/Web)│     │   Backend    │     │PostgreSQL │
└─────────────┘     └──────────────┘     └───────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  ML Model    │
                    │ (Mock/Real)  │
                    └──────────────┘
```

## Next Steps

1. **Production Deployment**
   - Deploy to a cloud service (Railway, Render, Heroku, etc.)
   - Set up proper authentication for admin endpoints
   - Configure CORS for your frontend domain

2. **Frontend Integration**
   - Build a web/mobile frontend
   - Use the OpenAPI spec for client generation
   - Implement map visualization (Google Maps, Leaflet, etc.)

3. **ML Model Integration**
   - Replace mock ML with a real trained model
   - Use TensorFlow, PyTorch, or cloud ML services
   - Train on actual pothole images

4. **Additional Features**
   - Email notifications
   - SMS updates
   - Image storage on Supabase Storage or S3
   - Analytics dashboard
   - Report filtering and search

## Support

For issues and questions:
- Open an issue on GitHub
- Check the README.md for detailed documentation
- Review the API docs at `/docs` endpoint
