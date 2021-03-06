from dataclasses import dataclass, field
from datetime import datetime, date

from typing import Set, List

from copy import deepcopy


@dataclass
class User:
    uid: int
    name: str
    dates_attended: Set[date] = field(default_factory=set)

    def __post_init__(self):
        if self.dates_attended is None:
            self.dates_attended = set()

        if isinstance(self.dates_attended, str):
            self.dates_attended = self._parse_dates_from_string(self.dates_attended)

        if isinstance(self.dates_attended, list):
            self.dates_attended = self.parse_dates_from_list(self.dates_attended)

    def attended(self, date: datetime):
        if date.date() not in self.dates_attended:
            self.dates_attended.add(date.date())

    def get_attendance_count(self):
        return len(self.dates_attended)

    def serialize(self):
        output = deepcopy(self.__dict__)
        output["dates_attended"] = self._format_dates_as_list()
        return output

    def _format_dates_as_list(self) -> List[str]:
        date_list = []

        for d in self.dates_attended:
            date_list.append(d.isoformat())

        return date_list

    def _parse_dates_from_string(self, string) -> set:
        splits = string.split(',')
        return self.parse_dates_from_list(splits)

    def parse_dates_from_list(self, l) -> set:
        output = set()
        for s in l:
            if len(s) == 0:
                continue
            output.add(date.fromisoformat(s))
        return output
