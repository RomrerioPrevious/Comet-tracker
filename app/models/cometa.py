from dataclasses import dataclass
from pandas import DataFrame


@dataclass
class Comet:
    id: int
    name: str
    diameter: float
    neo: bool
    albedo: float
    period: float
    class_: str


def fabric_comet_by_row(row: DataFrame) -> Comet:
    return Comet(
        id=row["id"][0],
        name=row["name"][0],
        diameter=float(row["diameter"][0]),
        neo=True if row["neo"][0] == "Y" else False,
        albedo=float(row["albedo"][0]),
        period=float(row["per"][0]),
        class_=row["class"][0]
    )
