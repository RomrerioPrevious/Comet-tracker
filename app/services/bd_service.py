from app.models.cometa import Comet, fabric_comet_by_row
from app.config import Config
from random import randint
import pandas as pd


class BDService:
    def __init__(self):
        path = f"{Config.find_global_path()}/resources/dataset.csv"
        with open(path) as file:
            self.bd = pd.read_csv(file, encoding="UTF-8")

    def get_comet_by_id(self, id: int) -> Comet:
        row = self.bd.query(f"id == '{id}'")
        if row.empty:
            raise IndexError(f"Don't find comet with id '{id}'")
        return fabric_comet_by_row(row)

    def get_comet_by_name(self, name: str) -> Comet:
        row = self.bd.query(f"name == '{name.capitalize()}'")
        if row.empty:
            raise IndexError(f"Don't find comet with name '{name}'")
        return fabric_comet_by_row(row)

    def get_random_comet(self) -> Comet:
        id = randint(0, 100000)
        return self.get_comet_by_id(id)

    def get_comet_by_diameter(self, diameter: str) -> Comet:
        row = self.bd.query(f"diameter == '{diameter.capitalize()}'")
        if row.empty:
            raise IndexError(f"Don't find comet with diameter '{diameter}'")
        return fabric_comet_by_row(row)

    def create_comet(self, comet: Comet) -> bool:
        ...

    def update_comet(self, comet: Comet) -> bool:
        ...

    def delete_comet(self, id: int) -> bool:
        ...
