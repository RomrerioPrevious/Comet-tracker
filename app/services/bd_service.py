from app.models.cometa import Comet


class BDService:
    def __init__(self):
        ...

    def get_comet_by_id(id: int) -> Comet:
        ...

    def get_comet_by_name(name: str) -> Comet:
        ...

    def create_comet(comet: Comet) -> bool:
        ...

    def update_comet(comet: Comet) -> bool:
        ...

    def delete_comet(id: int) -> bool:
        ...

