from dataclasses import dataclass, asdict
from pandas import DataFrame, Series


@dataclass
class Comet:
    id: int
    name: str
    diameter: float
    neo: bool
    albedo: float
    period: float
    class_: str

    def to_dict(self):
        return {k: str(v) for k, v in asdict(self).items()}

    def to_dataframe(self, original: DataFrame) -> DataFrame:
        columns = original.columns.tolist()
        comet_dict = self.to_dict()
        comet_dict["name"] = self.name
        df = DataFrame([comet_dict])
        return df.reindex(columns=columns, fill_value=None)

    def __str__(self) -> str:
        return f"{self.name}.\n" \
               f"Это астероид с диаметром равным {self.diameter}м. " \
               f"\n\n Нажмите /start для продолжения."


def fabric_comet_by_row(row: DataFrame | Series) -> Comet:
    if isinstance(row, DataFrame):
        row = row.iloc[0]
    return Comet(
        id=row["id"],
        name=row["full_name"],
        diameter=float(row["diameter"]),
        neo=True if row["neo"] == "Y" else False,
        albedo=float(row["albedo"]),
        period=float(row["per"]),
        class_=row["class"]
    )


def fabric_comet_by_fields(fields: [str]) -> Comet:
    if len(fields) == 5:
        comet = Comet(
            id=0,
            name=fields[0],
            diameter=float(fields[1]),
            neo=True if fields[2] == "Y" else False,
            albedo=float(fields[3]),
            period=float(fields[4]),
            class_=fields[5]
        )
    else:
        comet = Comet(
            id=fields[0],
            name=fields[1],
            diameter=float(fields[2]),
            neo=True if fields[3] == "Y" else False,
            albedo=float(fields[4]),
            period=float(fields[5]),
            class_=fields[6]
        )
    return comet
