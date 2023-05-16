from database import Database


def register_models() -> None:
    Database().BASE.metadata.create_all(Database().engine)
