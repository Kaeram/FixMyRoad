import uuid
from datetime import datetime


def generate_ticket_id() -> str:
    """Generate a unique ticket ID.
    
    Format: FMR-YYYYMMDD-XXXXX
    Where FMR = FixMyRoad, YYYYMMDD = date, XXXXX = unique identifier
    """
    date_str = datetime.now().strftime("%Y%m%d")
    unique_id = str(uuid.uuid4())[:8].upper()
    return f"FMR-{date_str}-{unique_id}"
