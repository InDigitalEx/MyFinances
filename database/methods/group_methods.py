from database import Database
from database.models import Group, User

_session = Database().session

class GroupMethods:
    @staticmethod
    def create(name: str, owner: User, private: bool = True) -> Group:
        group = Group(name=name, owner=owner, private=private)
        group.users.append(owner)

        _session.add(group)
        _session.commit()

        return group

    @staticmethod
    def get(group_id: int) -> Group:
        return _session.query(Group).get(group_id)

    @staticmethod
    def is_user_in_group(user: User, group_id: int) -> bool:
        group_ids: list[int] = [group.id for group in user.groups]
        return group_id in group_ids
