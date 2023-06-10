from database import Database
from database.models import User, Group

_session = Database().session

class UserMethods:
    @staticmethod
    def create(tg_id: int) -> User | None:
        user = UserMethods.get(tg_id)

        # return None if user doesn't exist
        if user is not None:
            return None

        user = User(tg_id=tg_id)
        _session.add(user)
        _session.commit()
        return user

    @staticmethod
    def get(tg_id: int) -> User | None:
        return _session.query(User).filter_by(tg_id=tg_id).first()

    @staticmethod
    def get_all_users() -> list[User]:
        return _session.query(User).all()

    @staticmethod
    def update_active_group(user: User, group: Group) -> User:
        user.active_group = group
        _session.add(user)
        _session.commit()
        return user

    @staticmethod
    def update_active_group_by_id(user: User, group_id: int) -> User:
        user.active_group_id = group_id
        _session.add(user)
        _session.commit()
        return user

    @staticmethod
    def add_user_to_group(user: User, group: Group) -> None:
        user.groups.append(group)
        _session.add(user)
        _session.commit()