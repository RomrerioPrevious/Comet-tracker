from dataclasses import dataclass
from datetime import datetime


@dataclass
class Comet:
    id: int
    name: str
    period: float
    distance_earth: float
    distance_sun: float
    destroy_chance: float
    diameter: float

