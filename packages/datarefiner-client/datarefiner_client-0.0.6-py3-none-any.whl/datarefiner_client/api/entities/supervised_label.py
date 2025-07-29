from dataclasses import dataclass
from enum import Enum
from typing import Optional


class SupervisedLabelStatus(Enum):
    CHECKING = "checking"
    QUEUE = "queue"
    PROCESSING = "processing"
    COMPLETE = "complete"
    ERROR = "error"


@dataclass
class SupervisedLabel:
    id: int
    status: SupervisedLabelStatus
    started: int
    has_groups: int
    upload_id: int
    title: str
    archive_file: Optional[str]
    error: Optional[str] = None
    ended: Optional[int] = None
    size: Optional[int] = None

    def __post_init__(self):
        self.status = SupervisedLabelStatus(self.status)
