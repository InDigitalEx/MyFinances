from database import Database
from database.models import Income, Group, User

_session = Database().session


class IncomeMethods:
    @staticmethod
    def add(user: User, group: Group, amount: int, text: str) -> Income:
        income = Income(user=user, amount=amount, text=text)
        group.incomes.append(income)
        _session.commit()
        return income

    @staticmethod
    def get_by_id(income_id: int) -> Income:
        return _session.query(Income).get(income_id)

    @staticmethod
    def delete_by_id(index: int) -> None:
        income = _session.query(Income).get(index)
        _session.delete(income)
        _session.commit()
