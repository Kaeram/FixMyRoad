from typing import List, Optional, Dict, Tuple
from datetime import datetime
from collections import defaultdict
import math
from supabase import Client
from backend.models.schemas import (
    PotholeReportCreate,
    PotholeReportResponse,
    TicketStatus,
    TicketPriority,
    TicketStatusUpdate,
    MapDataPoint,
    HeatmapDataPoint,
)
from backend.utils import generate_ticket_id


class PotholeService:
    """Service for pothole report management."""
    
    def __init__(self, supabase: Client):
        self.supabase = supabase
        self.table_name = "pothole_reports"
    
    async def create_report(
        self,
        report_data: PotholeReportCreate,
        image_url: Optional[str] = None
    ) -> PotholeReportResponse:
        """Create a new pothole report.
        
        Args:
            report_data: Report details
            image_url: URL of uploaded image (if any)
            
        Returns:
            Created report with ticket ID
        """
        ticket_id = generate_ticket_id()
        now = datetime.utcnow().isoformat()
        
        # Calculate initial priority based on existing reports in the area
        priority = await self._calculate_priority(report_data.latitude, report_data.longitude)
        
        # Prepare data for insertion
        data = {
            "ticket_id": ticket_id,
            "status": TicketStatus.PENDING.value,
            "priority": priority.value,
            "latitude": report_data.latitude,
            "longitude": report_data.longitude,
            "description": report_data.description,
            "severity": report_data.severity,
            "image_url": image_url,
            "reporter_name": report_data.reporter_name,
            "reporter_email": report_data.reporter_email,
            "reporter_phone": report_data.reporter_phone,
            "created_at": now,
            "updated_at": now,
        }
        
        # Insert into database
        result = self.supabase.table(self.table_name).insert(data).execute()
        
        if result.data and len(result.data) > 0:
            report = result.data[0]
            return PotholeReportResponse(
                ticket_id=report["ticket_id"],
                status=TicketStatus(report["status"]),
                priority=TicketPriority(report["priority"]),
                latitude=report["latitude"],
                longitude=report["longitude"],
                description=report.get("description"),
                severity=report.get("severity"),
                image_url=report.get("image_url"),
                reporter_name=report.get("reporter_name"),
                reporter_email=report.get("reporter_email"),
                reporter_phone=report.get("reporter_phone"),
                created_at=datetime.fromisoformat(report["created_at"]),
                updated_at=datetime.fromisoformat(report["updated_at"]),
            )
        else:
            raise Exception("Failed to create report")
    
    async def _calculate_priority(self, latitude: float, longitude: float) -> TicketPriority:
        """Calculate priority based on complaint density in the area.
        
        Priority is determined by the number of existing reports within
        a certain radius (approx 1km = 0.01 degrees).
        
        Args:
            latitude: Report latitude
            longitude: Report longitude
            
        Returns:
            Calculated priority level
        """
        radius = 0.01  # Approx 1km in degrees
        
        # Query reports in the area (within radius)
        result = self.supabase.table(self.table_name).select("*").execute()
        
        if not result.data:
            return TicketPriority.LOW
        
        # Count reports in the area
        nearby_count = 0
        for report in result.data:
            distance = self._calculate_distance(
                latitude, longitude,
                report["latitude"], report["longitude"]
            )
            if distance <= radius:
                nearby_count += 1
        
        # Determine priority based on density
        if nearby_count >= 10:
            return TicketPriority.CRITICAL
        elif nearby_count >= 5:
            return TicketPriority.HIGH
        elif nearby_count >= 2:
            return TicketPriority.MEDIUM
        else:
            return TicketPriority.LOW
    
    @staticmethod
    def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate approximate distance between two coordinates.
        
        Simple Euclidean distance for small distances.
        """
        return math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)
    
    async def get_report_by_ticket_id(self, ticket_id: str) -> Optional[PotholeReportResponse]:
        """Get a report by ticket ID.
        
        Args:
            ticket_id: Ticket ID to search for
            
        Returns:
            Report if found, None otherwise
        """
        result = self.supabase.table(self.table_name).select("*").eq("ticket_id", ticket_id).execute()
        
        if result.data and len(result.data) > 0:
            report = result.data[0]
            return PotholeReportResponse(
                ticket_id=report["ticket_id"],
                status=TicketStatus(report["status"]),
                priority=TicketPriority(report["priority"]),
                latitude=report["latitude"],
                longitude=report["longitude"],
                description=report.get("description"),
                severity=report.get("severity"),
                image_url=report.get("image_url"),
                reporter_name=report.get("reporter_name"),
                reporter_email=report.get("reporter_email"),
                reporter_phone=report.get("reporter_phone"),
                created_at=datetime.fromisoformat(report["created_at"]),
                updated_at=datetime.fromisoformat(report["updated_at"]),
            )
        return None
    
    async def update_status(
        self,
        ticket_id: str,
        status_update: TicketStatusUpdate
    ) -> Optional[PotholeReportResponse]:
        """Update ticket status (admin function).
        
        Args:
            ticket_id: Ticket ID to update
            status_update: New status and optional admin notes
            
        Returns:
            Updated report if successful, None otherwise
        """
        now = datetime.utcnow().isoformat()
        
        data = {
            "status": status_update.status.value,
            "updated_at": now,
        }
        
        if status_update.admin_notes:
            data["admin_notes"] = status_update.admin_notes
        
        result = self.supabase.table(self.table_name).update(data).eq("ticket_id", ticket_id).execute()
        
        if result.data and len(result.data) > 0:
            return await self.get_report_by_ticket_id(ticket_id)
        return None
    
    async def get_all_reports_for_map(self) -> List[MapDataPoint]:
        """Get all reports for admin map view.
        
        Returns:
            List of map data points
        """
        result = self.supabase.table(self.table_name).select("*").execute()
        
        if not result.data:
            return []
        
        return [
            MapDataPoint(
                ticket_id=report["ticket_id"],
                latitude=report["latitude"],
                longitude=report["longitude"],
                status=TicketStatus(report["status"]),
                priority=TicketPriority(report["priority"]),
                severity=report.get("severity"),
                created_at=datetime.fromisoformat(report["created_at"]),
            )
            for report in result.data
        ]
    
    async def get_heatmap_data(self) -> List[HeatmapDataPoint]:
        """Get heatmap data showing complaint density.
        
        Groups reports by approximate location and returns density information.
        
        Returns:
            List of heatmap data points with weights
        """
        result = self.supabase.table(self.table_name).select("latitude,longitude").execute()
        
        if not result.data:
            return []
        
        # Group reports by approximate grid (0.005 degree precision ~500m)
        grid_size = 0.005
        density_map: Dict[Tuple[float, float], int] = defaultdict(int)
        
        for report in result.data:
            lat = round(report["latitude"] / grid_size) * grid_size
            lon = round(report["longitude"] / grid_size) * grid_size
            density_map[(lat, lon)] += 1
        
        return [
            HeatmapDataPoint(
                latitude=lat,
                longitude=lon,
                weight=count
            )
            for (lat, lon), count in density_map.items()
        ]
