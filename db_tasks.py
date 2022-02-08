from datetime import datetime
from dataclasses import dataclass, field

@dataclass
class Tasks():

    name: str
    creators: list
    description: str = field(default_factory=str)
    start_date: datetime = datetime.utcnow()
    completion_date: datetime = datetime.utcnow()
    due_date: datetime = datetime.utcnow()
    priority: int = 0
    assigned_to: list = field(default_factory=list)
    project_file:str  = "C:\\"
    status: str = "not started"  # TODO: only allow "not started", "in progress", and "complete"
