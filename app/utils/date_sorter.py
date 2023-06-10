from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

from data import Config

# Список названий месяцев
_MONTHS = [
    'Январь', 'Февраль', 'Март', 'Апрель',
    'Май', 'Июнь', 'Июль', 'Август',
    'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
]

_MONTHS_TO_DAYS = [
    'января', 'евраля', 'марта', 'апреля',
    'мая', 'июня', 'июля', 'августа',
    'сентября', 'октября', 'ноября', 'декабря'
]

class DateSorter:
    """
    The DateSorter class provides methods for filtering items based on dates.
    """

    def __init__(self, items: List) -> None:
        self.items = sorted(items, key=lambda x: x.created_at, reverse=True)

    def filter(self, start_date: Optional[datetime]=None, end_date: Optional[datetime]=None) -> List:
        filtered_items = []
        for item in self.items:
            if start_date is not None and item.created_at < start_date:
                continue
            if end_date is not None and item.created_at > end_date:
                continue
            filtered_items.append(item)
        return filtered_items

    def get_today(self) -> List:
        today = datetime.now()
        start_date = datetime(today.year, today.month, today.day)
        end_date = start_date + timedelta(days=1)
        return self.filter(start_date, end_date)

    def get_this_week(self) -> List:
        today = datetime.now()
        start_date = datetime(today.year, today.month, today.day) - timedelta(days=today.weekday())
        end_date = start_date + timedelta(weeks=1)
        return self.filter(start_date, end_date)

    def get_this_month(self) -> List:
        today = datetime.now()
        start_date = datetime(today.year, today.month, 1)
        if today.month == 12:
            end_date = datetime(today.year + 1, 1, 1)
        else:
            end_date = datetime(today.year, today.month + 1, 1)
        return self.filter(start_date, end_date)

    def get_this_year(self) -> List:
        today = datetime.now()
        start_date = datetime(today.year, 1, 1)
        end_date = datetime(today.year + 1, 1, 1)
        return self.filter(start_date, end_date)

    def get_last_days(self, delta: int) -> List:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=delta)
        return self.filter(start_date, end_date)

    def get_all_time(self) -> List:
        return self.filter()


class DateGroupsTrimmer(DateSorter):
    def __init__(self, items: List) -> None:
        super().__init__(items)

    def get_today(self, page: int) -> Tuple[List, bool]:
        return self._trim(super().get_today(), page)

    def get_this_week(self, page: int) -> Tuple[List, bool]:
        return self._trim(super().get_this_week(), page)

    def get_this_month(self, page: int) -> Tuple[List, bool]:
        return self._trim(super().get_this_month(), page)

    def get_this_year(self, page: int) -> Tuple[List, bool]:
        return self._trim(super().get_this_year(), page)

    def get_last_days(self, delta: int, page: int) -> Tuple[List, bool]:
        return self._trim(super().get_last_days(delta), page)

    def get_all_time(self, page: int) -> Tuple[List, bool]:
        return self._trim(super().get_all_time(), page)

    @staticmethod
    def _trim(items: List, page: int) -> Tuple[List, bool]:
        page_len = int(Config.PAGE_LENGHT)
        start = page * page_len
        end = start + page_len
        was_trimmed = False

        counter = 0
        trimmed_list = []
        for item in items:
            if counter >= end:
                was_trimmed = True
                break
            if counter >= start:
                trimmed_list.append(item)
            counter += 1
        return trimmed_list, was_trimmed


class DateGroupsSorter(DateGroupsTrimmer):
    def __init__(self, items: List) -> None:
        super().__init__(items)

    def get_today(self, page) -> Tuple[Dict, bool]:
        items, was_trimmed = super().get_today(page)
        return self._days_sort(items), was_trimmed

    def get_this_week(self, page: int) -> Tuple[Dict, bool]:
        items, was_trimmed = super().get_this_week(page)
        return self._days_sort(items), was_trimmed

    def get_this_month(self, page: int) -> Tuple[Dict, bool]:
        items, was_trimmed = super().get_this_month(page)
        return self._days_sort(items), was_trimmed

    def get_this_year(self, page: int) -> Tuple[Dict, bool]:
        items, was_trimmed = super().get_this_year(page)

        # Sort by months
        items = self._months_sort(items)

        # Sort months by months and days
        for month, item in items.items():
            items[month] = self._days_sort(item)

        return items, was_trimmed

    def get_last_days(self, delta: int, page: int) -> Tuple[Dict, bool]:
        items, was_trimmed = super().get_last_days(delta, page)
        return self._days_sort(items), was_trimmed

    def get_all_time(self, page: int) -> Tuple[Dict, bool]:
        items, was_trimmed = super().get_all_time(page)

        # Sort by years
        items = self._years_sort(items)

        # Sort years by years, months and days
        for year, year_item in items.items():
            items[year] = self._months_sort(year_item)
            for month, month_item in items[year].items():
                items[year][month] = self._days_sort(month_item)
        return items, was_trimmed

    def get_by_name(self, period: str, page: int = 0, delta: Optional[int] = 1) -> Tuple[Dict, bool]:
        if period == 'today':
            return self.get_today(page)
        elif period == 'week':
            return self.get_this_week(page)
        elif period == 'month':
            return self.get_this_month(page)
        elif period == 'year':
            return self.get_this_year(page)
        elif period == 'last':
            return self.get_last_days(delta, page)
        else:
            return self.get_all_time(page)

    # Private
    @staticmethod
    def _years_sort(items: List) -> Dict:
        groups = {}
        for item in items:
            year = f'{item.created_at.year} год'
            if year in groups:
                groups[year].append(item)
            else:
                groups[year] = [item]
        return groups

    @staticmethod
    def _months_sort(items: List) -> Dict:
        groups = {}
        for item in items:
            month = f'{_MONTHS[item.created_at.month-1]}'
            if month in groups:
                groups[month].append(item)
            else:
                groups[month] = [item]
        return groups

    @staticmethod
    def _days_sort(items: List) -> Dict:
        groups = {}
        for item in items:
            day = f'{item.created_at.day} {_MONTHS_TO_DAYS[item.created_at.month-1]}'
            if day in groups:
                groups[day].append(item)
            else:
                groups[day] = [item]
        return groups
