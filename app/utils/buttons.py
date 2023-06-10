from abc import ABC
from dataclasses import dataclass

@dataclass(frozen=True)
class Buttons(ABC):
    START = {
        'statistics': 'Статистика 📊',
        'groups': 'Сменить группу ✏️',
        'create_group': 'Создать группу 📝',
        'invite': 'Пригласить в группу 👨',
        'help': 'Команды 📚',
        'settings': 'Настройки ⚙️',
        'author': 'Автор 👨🏻‍💻'
    }
    SETTINGS = {
        'settings_profile': 'Профиль',
        'settings_groups': 'Группы',
        'settings_varia': 'Разное'
    }
    CREATE_GROUP_PRIVATE = {
        'private': 'Приватная 🔒',
        'public': 'Публичная 👥'
    }
    INVITE_TYPE = {
        'link': 'По ссылке 🔗',
        'personal': 'Личное 🤝'
    }
    INVITE = {
        'accept': 'Принять',
        'decline': 'Отклонить'
    }
    STAT_TYPE = {
        'expenses': 'Доходы',
        'incomes': 'Расходы'
    }
    STAT_PERIOD = {
        'today': 'За сегодня',
        'week': 'За неделю',
        'month': 'За месяц',
        'year': 'За год',
        'all': 'За всё время'
    }
