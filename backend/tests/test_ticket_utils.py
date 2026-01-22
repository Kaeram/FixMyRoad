import pytest
from datetime import datetime
from backend.utils.ticket_utils import generate_ticket_id


def test_generate_ticket_id_format():
    """Test that ticket ID has correct format."""
    ticket_id = generate_ticket_id()
    
    # Check format: FMR-YYYYMMDD-XXXXX
    assert ticket_id.startswith("FMR-")
    parts = ticket_id.split("-")
    assert len(parts) == 3
    assert parts[0] == "FMR"
    assert len(parts[1]) == 8  # YYYYMMDD
    assert len(parts[2]) == 8  # 8 char unique ID


def test_generate_ticket_id_unique():
    """Test that generated ticket IDs are unique."""
    ids = set()
    for _ in range(100):
        ticket_id = generate_ticket_id()
        assert ticket_id not in ids
        ids.add(ticket_id)


def test_generate_ticket_id_date():
    """Test that ticket ID contains current date."""
    ticket_id = generate_ticket_id()
    date_part = ticket_id.split("-")[1]
    current_date = datetime.now().strftime("%Y%m%d")
    assert date_part == current_date
