from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime


class Event(BaseModel):
    event_id: str
    timestamp: datetime
    event_type: str
    service: str
    severity: str = "medium"
    metadata: Dict = {}
    parent_event: Optional[str] = None