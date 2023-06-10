import logging
from typing import Optional

from database.methods import UserMethods, GroupMethods, ExpenseMethods, IncomeMethods
from database.models import User, Group, Expense, Income


class Methods:
    _user: User = None

    def __init__(self, telegram_id: int):
        self._telegram_id = telegram_id
        self.user = self.get_user()

    def get_user(self) -> User:
        """ Получение данных пользователя """

        # Если данные пользователя уже получены, то возвращем их
        if self.user is not None:
            return self.user

        # Получаем пользователя
        user = UserMethods.get(self.telegram_id)

        # Если пользователя не существует, то создаем его
        if user is None:
            logging.debug("Create a user because it is not in the database")
            user = self.activate_user()

        self.user = user
        return self.user

    def activate_user(self) -> User | None:
        """ Создание пользователя и личной группы"""

        # Создаем пользователя
        user = UserMethods.create(self.telegram_id)

        # Если пользователь уже создан, то возвращаем None
        if user is None:
            return None

        # Создаем личную группу, добавляем в нее пользователя
        group = GroupMethods.create('Личная', user, True)
        UserMethods.add_user_to_group(user, group)
        UserMethods.update_active_group(user, group)

        self.telegram_id = user.id
        return user

    def create_group(self, name: str, private: bool = True) -> Group:
        group = GroupMethods.create(name, self.user, private)
        UserMethods.add_user_to_group(self.user, group)
        return group

    def add_to_group(self, group_id: int) -> Group:
        group = GroupMethods.get(group_id)
        UserMethods.add_user_to_group(self.user, group)
        return group

    def create_expense(self, amount: int, text: str, group: Optional[Group] = None) -> Expense:
        if group is None:
            group = self.user.active_group
        return ExpenseMethods.add(self.user, group, amount, text)

    @staticmethod
    def get_expense(expense_id: int) -> Expense:
        return ExpenseMethods.get_by_id(expense_id)

    @staticmethod
    def delete_expense_by_id(expense_id: int) -> None:
        ExpenseMethods.delete_by_id(expense_id)

    def create_income(self, amount: int, text: str, group: Optional[Group] = None) -> Income:
        if group is None:
            group = self.user.active_group
        return IncomeMethods.add(self.user, group, amount, text)

    @staticmethod
    def get_income(income_id: int) -> Income:
        return IncomeMethods.get_by_id(income_id)

    @staticmethod
    def delete_income_by_id(income_id: int) -> None:
        IncomeMethods.delete_by_id(income_id)

    def update_user_group(self, group: Group) -> User:
        self.user = UserMethods.update_active_group(self.user, group)
        return self.user

    def update_user_group_by_id(self, group_id: int) -> User:
        self.user = UserMethods.update_active_group_by_id(self.user, group_id)
        return self.user

    @staticmethod
    def get_group_by_id(group_id: int) -> Group:
        return GroupMethods.get(group_id)

    def is_in_group(self, group_id: int) -> bool:
        return GroupMethods.is_user_in_group(self.user, group_id)

    @staticmethod
    def is_user_exists(tg_id: int) -> bool:
        return UserMethods.get(tg_id) is not None

    #region properties

    #region active group

    @property
    def active_group(self) -> Group:
        return self.user.active_group

    @active_group.setter
    def active_group(self, group: Group):
        self.update_user_group(group)

    @property
    def active_group_id(self) -> int:
        return self.user.active_group_id

    @active_group_id.setter
    def active_group_id(self, group_id: int):
        self.update_user_group_by_id(group_id)

    @property
    def group_name(self) -> str:
        return self.user.active_group.name

    #endregion

    @property
    def user_groups(self) -> list[Group]:
        return self.user.groups

    @property
    def user_owner_groups(self) -> list[Group]:
        return self.user.owner_groups

    @property
    def active_group_users(self) -> list[User]:
        return self.active_group.users

    @property
    def active_group_another_users(self) -> list[User]:
        return [user for user in self.active_group_users if self.user.tg_id != user.tg_id]

    # region id

    @property
    def id(self) -> int:
        return self.user.id

    #endregion

    # region telegram_id

    @property
    def telegram_id(self) -> int:
        return self._telegram_id
    @telegram_id.setter
    def telegram_id(self, value: int):
        self._telegram_id = value

    #endregion telegram_id

    # region user
    @property
    def user(self) -> User:
        return self._user

    @user.setter
    def user(self, value: User):
        self._user = value

    #endregion user

    #endregion properties
