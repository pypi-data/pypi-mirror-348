# cult_common/schemas/signal.py

from datetime import datetime
from pydantic import BaseModel

class Signal(BaseModel):
    original_event_id: str
    token_id: str
    timestamp: datetime
    score: float
    is_anomaly: bool
    anomaly_model_score: float
    model_type: str
    raw_event_snippet: str
    created_at: datetime

    # **NEW** make signal_type optional
    signal_type: str | None = None

    class Config:
        validate_assignment = True
        frozen = True
