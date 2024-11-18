from app.models.comet import Comet, fabric_comet_by_row
from app.config import Config
import pandas as pd


class BDService:
    def __init__(self):
        self.path = f"{Config.find_global_path()}/resources/dataset.csv"
        with open(self.path) as file:
            self.bd = pd.read_csv(file, encoding="UTF-8")

    def get_comet_by_id(self, id: str) -> Comet:
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
        row = self.bd.sample(n=1)
        return fabric_comet_by_row(row)

    def get_comet_by_diameter(self, diameter: str) -> Comet:
        row = self.bd.query(f"diameter == '{diameter.capitalize()}'")
        if row.empty:
            raise IndexError(f"Don't find comet with diameter '{diameter}'")
        return fabric_comet_by_row(row)

    def create_comet(self, comet: Comet):
        self.bd = pd.concat([self.bd, comet.to_dataframe(self.bd)])
        self.bd.to_csv(self.path, index=False)

    def update_comet(self, comet: Comet):
        row = self.bd.query(f"id == '{comet.id}'")
        self.bd.loc[row.index] = comet.to_dataframe(self.bd)
        self.bd.to_csv(self.path, index=False)

    def delete_comet(self, id: str):
        row = self.bd.query(f"id == '{id}'")
        if row.empty:
            raise IndexError(f"Don't find comet with id '{id}'")
        self.bd.drop(row.index[0], inplace=True)
        self.bd.to_csv(self.path, index=False)
