from datetime import datetime, timedelta


def parse_date(date_string: str) -> datetime:
    if 'Сегодня' in date_string:
        today = datetime.now()
        time_string = date_string.split(', ')[1]
        hour, minute = map(int, time_string.split(':'))
        return today.replace(hour=hour, minute=minute)

    if 'Вчера' in date_string:
        yesterday = datetime.now() - timedelta(days=1)
        time_string = date_string.split(', ')[1]
        hour, minute = map(int, time_string.split(':'))
        return yesterday.replace(hour=hour, minute=minute)

    month_dict = {
        'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6,
        'июля': 7, 'августа': 8, 'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
    }
    date, time = date_string.split(', ')
    if len(date.split()) > 2:
        day, month, year = date.split()
        month = month_dict[month]
        hour, minute = map(int, time.split(':'))
        return datetime(int(year), month, int(day), hour, minute)
    else:
        day, month = date.split()
        month = month_dict[month]
        hour, minute = map(int, time.split(':'))
        now = datetime.now()
        return datetime(now.year, month, int(day), hour, minute)
