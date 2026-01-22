from fastapi import APIRouter, HTTPException, Depends
from supabase import Client
from backend.models.schemas import TicketTrackingResponse
from backend.services import PotholeService
from backend.config.database import get_supabase


router = APIRouter(prefix="/api/public", tags=["Public"])


@router.get("/track/{ticket_id}", response_model=TicketTrackingResponse)
async def track_ticket(
    ticket_id: str,
    supabase: Client = Depends(get_supabase),
):
    """Track a pothole report by ticket ID (public endpoint).
    
    Allows anyone with a ticket ID to check the status of their report.
    Returns limited information (no reporter personal details).
    
    Args:
        ticket_id: Ticket ID to track
        supabase: Database client
        
    Returns:
        Ticket tracking information
    """
    service = PotholeService(supabase)
    try:
        report = await service.get_report_by_ticket_id(ticket_id)
        if not report:
            raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
        
        # Return tracking response (limited information)
        return TicketTrackingResponse(
            ticket_id=report.ticket_id,
            status=report.status,
            priority=report.priority,
            latitude=report.latitude,
            longitude=report.longitude,
            description=report.description,
            severity=report.severity,
            created_at=report.created_at,
            updated_at=report.updated_at,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to track ticket: {str(e)}")
