from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    uid: int
    name: str
    dates_attended: set = field(default_factory=set)

    def __post_init__(self):
        if self.dates_attended is None:
            self.dates_attended = set()

    def attended(self, date: datetime):
        if date.date() not in self.dates_attended:
            self.dates_attended.add(date.date())

    def get_attendance_count(self):
        return len(self.dates_attended)
