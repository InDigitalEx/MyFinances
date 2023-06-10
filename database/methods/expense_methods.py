from database import Database
from database.models import Expense, Group, User

_session = Database().session


class ExpenseMethods:
    @staticmethod
    def add(user: User, group: Group, amount: int, text: str) -> Expense:
        expense = Expense(user=user, amount=amount, text=text)
        group.expenses.append(expense)
        _session.commit()
        return expense

    @staticmethod
    def get_by_id(expense_id: int) -> Expense:
        return _session.query(Expense).get(expense_id)

    @staticmethod
    def delete_by_id(index: int) -> None:
        expense = _session.query(Expense).get(index)
        _session.delete(expense)
        _session.commit()
