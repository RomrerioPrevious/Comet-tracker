from dataclasses import dataclass
from datetime import datetime


@dataclass
class Comet:
    id: int
    name: str
    diameter: float
    neo: bool
    albedo: float
    period: float
    class_: str

