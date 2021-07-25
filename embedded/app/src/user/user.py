from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    uid: int
    name: str
    attendance_count: int = field(default=0)

    def attended(self, date: datetime):
        self.attendance_count += 1
