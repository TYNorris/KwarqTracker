from dataclasses import dataclass, field
from enum import Enum


class Status(str, Enum):
    neutral = "secondary",
    success = "success",
    fail = "danger",
    warn = "warning",
    info = "info"

@dataclass
class Message:

    title: str
    subtitle: str
    status: Status = field(default=Status.neutral)


    @classmethod
    def default(cls):
        return Message(
            title="Please scan in",
            subtitle="If you're new here, ask a student for help!",
            status=Status.neutral
        )
