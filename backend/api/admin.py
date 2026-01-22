from fastapi import APIRouter, HTTPException, Depends
from typing import List
from supabase import Client
from backend.models.schemas import (
    PotholeReportResponse,
    TicketStatusUpdate,
    MapDataPoint,
    HeatmapDataPoint,
)
from backend.services import PotholeService
from backend.config.database import get_supabase


router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/map", response_model=List[MapDataPoint])
async def get_map_data(supabase: Client = Depends(get_supabase)):
    """Get all pothole reports for admin map view.
    
    Returns all reports with their coordinates, status, and priority
    for display on an admin map interface.
    
    Returns:
        List of map data points
    """
    service = PotholeService(supabase)
    try:
        return await service.get_all_reports_for_map()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch map data: {str(e)}")


@router.get("/heatmap", response_model=List[HeatmapDataPoint])
async def get_heatmap_data(supabase: Client = Depends(get_supabase)):
    """Get heatmap data showing complaint density.
    
    Returns aggregated data showing the density of reports in different areas.
    Used to create a heatmap visualization showing hotspots.
    
    Returns:
        List of heatmap data points with weights
    """
    service = PotholeService(supabase)
    try:
        return await service.get_heatmap_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch heatmap data: {str(e)}")


@router.put("/tickets/{ticket_id}/status", response_model=PotholeReportResponse)
async def update_ticket_status(
    ticket_id: str,
    status_update: TicketStatusUpdate,
    supabase: Client = Depends(get_supabase),
):
    """Update the status of a ticket (admin only).
    
    Allows admins to update ticket status and add notes.
    
    Args:
        ticket_id: Ticket ID to update
        status_update: New status and optional admin notes
        supabase: Database client
        
    Returns:
        Updated report
    """
    service = PotholeService(supabase)
    try:
        report = await service.update_status(ticket_id, status_update)
        if not report:
            raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
        return report
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update ticket: {str(e)}")


@router.get("/tickets/{ticket_id}", response_model=PotholeReportResponse)
async def get_ticket_details(
    ticket_id: str,
    supabase: Client = Depends(get_supabase),
):
    """Get detailed information about a ticket (admin view).
    
    Returns full ticket details including reporter information.
    
    Args:
        ticket_id: Ticket ID to retrieve
        supabase: Database client
        
    Returns:
        Full report details
    """
    service = PotholeService(supabase)
    try:
        report = await service.get_report_by_ticket_id(ticket_id)
        if not report:
            raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
        return report
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch ticket: {str(e)}")
