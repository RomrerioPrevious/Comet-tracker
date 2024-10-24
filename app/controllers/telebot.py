from app.services import bd_service

service = bd_service.BDService()


def search_name(comet: str) -> str:
    new_comet = service.search(comet)
    return new_comet.name
