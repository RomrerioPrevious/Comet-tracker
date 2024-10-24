from app.models.cometa import Comet


class BDService:
    def search(self, comet: str) -> Comet:
        ...