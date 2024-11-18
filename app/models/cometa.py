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

    def __str__(self) -> str:
        return f"{self.name}"


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


def fabric_comet_by_fields(fields: [str]) -> Comet:
    return Comet(
        id=0,
        name=fields[0],
        diameter=float(fields[1]),
        neo=True if fields[2] == "Y" else False,
        albedo=float(fields[3]),
        period=float(fields[4]),
        class_=fields[5]
    )