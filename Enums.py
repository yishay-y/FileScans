from enum import Enum


class State(Enum):
    Accepted = 1
    Running = 2
    Error = 3
    Complete = 4
