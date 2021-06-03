from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time


def get_date() -> str:
    """
    Возвращает текущую дату и время в формате Http хедера Date
    """
    now = datetime.now()
    stamp = mktime(now.timetuple())
    return format_date_time(stamp)
