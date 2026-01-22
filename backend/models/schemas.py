from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum


class TicketStatus(str, Enum):
    """Ticket status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    REJECTED = "rejected"


class TicketPriority(str, Enum):
    """Ticket priority based on area complaint density."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ImageValidationResult(BaseModel):
    """Image validation result from ML model."""
    is_valid: bool
    confidence: float
    reason: Optional[str] = None


class PotholeReportCreate(BaseModel):
    """Schema for creating a pothole report."""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    description: Optional[str] = Field(None, max_length=500, description="Description of the pothole")
    severity: Optional[str] = Field("medium", description="Reported severity (low/medium/high)")
    reporter_name: Optional[str] = Field(None, max_length=100)
    reporter_email: Optional[str] = Field(None, max_length=100)
    reporter_phone: Optional[str] = Field(None, max_length=20)


class PotholeReportResponse(BaseModel):
    """Schema for pothole report response."""
    ticket_id: str
    status: TicketStatus
    priority: TicketPriority
    latitude: float
    longitude: float
    description: Optional[str]
    severity: Optional[str]
    image_url: Optional[str]
    reporter_name: Optional[str]
    reporter_email: Optional[str]
    reporter_phone: Optional[str]
    created_at: datetime
    updated_at: datetime


class TicketStatusUpdate(BaseModel):
    """Schema for updating ticket status."""
    status: TicketStatus
    admin_notes: Optional[str] = Field(None, max_length=1000)


class TicketTrackingResponse(BaseModel):
    """Schema for public ticket tracking."""
    ticket_id: str
    status: TicketStatus
    priority: TicketPriority
    latitude: float
    longitude: float
    description: Optional[str]
    severity: Optional[str]
    created_at: datetime
    updated_at: datetime


class MapDataPoint(BaseModel):
    """Schema for map data point."""
    ticket_id: str
    latitude: float
    longitude: float
    status: TicketStatus
    priority: TicketPriority
    severity: Optional[str]
    created_at: datetime


class HeatmapDataPoint(BaseModel):
    """Schema for heatmap data point."""
    latitude: float
    longitude: float
    weight: int  # Number of reports in this area
