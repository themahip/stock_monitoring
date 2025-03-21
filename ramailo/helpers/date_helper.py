import calendar
import math
import time
from calendar import monthrange
from datetime import date, datetime
from datetime import time as datetime_time
from datetime import timedelta

import pytz
from dateutil import parser
from dateutil.relativedelta import relativedelta
from django.utils import timezone as db_timezone
from django.utils.timezone import localtime
from pytz import timezone

ist_tz = timezone('Asia/Calcutta')
month_strings = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
    0: "Dec"}


def get_next_working_date(day=None):
    if not day:
        day = datetime.now().date()

    return get_next_weekday(day)


def get_time_n_days_from_today(days=0):
    return time.time() - timedelta(days).total_seconds()


def get_epoch_micro_seconds():
    return int(time.time() * 1000000)


def get_timezone_aware_datetime(date_object_in):
    return datetime.combine(date_object_in, datetime_time.min).replace(tzinfo=ist_tz)


def get_date_from_datetime(datetime_object):
    return datetime_object.date().isoformat()


def get_datetime_from_string(string_object):
    return datetime.strptime(string_object, '%Y-%m-%d').replace(tzinfo=ist_tz)


def get_next_weekday(day):
    weekday = day.weekday()
    days_ahead = 1
    if weekday == 4:
        days_ahead = 3
    if weekday == 5:
        days_ahead = 2

    return day + timedelta(days_ahead)


def is_a_weekday(day):
    weekday = day.weekday()
    if weekday == 5 or weekday == 6:
        return False

    return True


def add_months(a_date, months=1):
    month = a_date.month - 1 + months
    year = int(a_date.year + month / 12)
    month = month % 12 + 1
    day = min(a_date.day, calendar.monthrange(year, month)[1])

    return date(year, month, day)


def now_ist():
    return datetime.now(ist_tz)


def now_utc():
    return datetime.now(pytz.utc)


def get_time_from_string(string):
    return localtime(parser.parse(string))


def get_time_from_string_h_m_s(string):
    return datetime.strptime(string, '%H:%M:%S').time()


def get_date_object(string):
    return parser.parse(string).date()


def get_timestamp(string):
    return parser.parse(string)


def format_user_friendly(a_date):
    if not a_date:
        return ''

    return a_date.strftime('%d %b, %Y')


def format_user_friendly_month_and_year(a_date):
    if not a_date:
        return ''

    return a_date.strftime('%b %Y')


def format_datetime_user_friendly(a_date):
    if not a_date:
        return ''

    date_object = get_date_in_ist(a_date)
    return datetime.strftime(date_object, '%d %b,%Y %I:%S %p')


def get_date_from_d_b_y(date_string):
    return datetime.strptime(str(date_string.strip()), '%d-%b-%Y').date()


def get_date_from_y_b_d(date_string):
    return datetime.strptime(str(date_string.strip()), '%Y-%b-%d')


def get_date_from_slash_d_m_y(date_string):
    return datetime.strptime(str(date_string.strip()), '%d/%m/%Y').date()


def get_date_from_pipe_d_m_y(date_string):
    try:
        return datetime.strptime(str(date_string.strip()), '%d|%m|%Y').date()
    except ValueError:
        return None


def get_date_string_in_d_m_y(a_date):
    return a_date.strftime('%d/%m/%Y')


def get_date_string_in_d_m_y_without_separator(a_date):
    return a_date.strftime('%d%m%Y')


def get_timestamp_in_ist(date_time):
    return date_time.astimezone(ist_tz).strftime("%d, %b %Y, %H:%M")


def get_date_in_ist(date_time):
    return date_time.astimezone(ist_tz)


def get_date_string(date_time, date_format):
    return date_time.strftime(date_format)


def get_n_days_later_date(n, start_date=datetime.now(ist_tz)):
    return start_date + timedelta(days=n)


def get_n_days_past_date(n, start_date=datetime.now(ist_tz)):
    return start_date - timedelta(days=n)


def get_current_date():
    return db_timezone.now().date()


def get_current_month():
    return datetime.now().date().month


def get_current_timestamp():
    return db_timezone.now()


def get_current_year():
    return datetime.now().year


def get_month_string(month):
    return month_strings.get(month)


# 0 for current month, year
def get_month_year_from_now(months=0):
    current_month = datetime.now().month
    required_year = datetime.now().year

    required_month = current_month + months

    if required_month > 12:
        required_year += (required_month - 1) / 12
        required_month = required_month % 12

    if required_month == 0:
        required_month = 12

    return required_month, int(required_year)


def get_month_year_from_now_string(months=0):
    month, year = get_month_year_from_now(months)
    return "{}-{}".format(get_month_string(month), year)


def get_last_month_date(offset_month):
    month, year = get_month_year_from_now(offset_month)

    return datetime(day=monthrange(year, month)[1], month=month, year=year)


def get_date_from_day_month_year(day, month, year):
    return datetime(year=year, month=month, day=day)


def get_month_difference(from_date, to_date):
    return (to_date.month - from_date.month) + (to_date.year - from_date.year) * 12


def time_diff_in_hrs(from_date, to_date):
    if not from_date:
        from_date = to_date

    time_diff = to_date - from_date
    timedelta_hrs = divmod(time_diff.total_seconds(), 3600)
    return timedelta_hrs[0]


def unix_time_millis(dt):
    dt = dt.replace(tzinfo=None)
    epoch = datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds())


def get_timedelta_time_from_now(timedelta_time):
    return datetime.now() + timedelta_time


def get_first_of_current_month():
    today = get_current_date()
    return datetime(year=today.year, month=today.month, day=1)


def check_leap_year(year):
    return (year % 4) == 0 and ((year % 100) != 0 or (year % 400) == 0)


def get_weekday():
    return date.today().weekday()


def get_month_day():
    return date.today().day


def get_today():
    return date.today()


def get_now_date():
    return datetime.now(ist_tz).date()


def get_last_month_start_end_date() -> tuple:
    """
    Get start date and end date of last month.
    """
    today = get_current_date()
    start_date = today.replace(day=1) - relativedelta(months=1)
    end_date = today.replace(day=1) - timedelta(days=1)
    return start_date, end_date


def get_fiscal_year(date=None):
    import datetime

    if date is None:
        date = get_today()

    if date.month >= 4:
        fiscal_start_year = date.year
        fiscal_end_year = date.year + 1
    else:
        fiscal_start_year = date.year - 1
        fiscal_end_year = date.year

    fiscal_start_date = datetime.date(fiscal_start_year, 4, 1)
    fiscal_end_date = datetime.date(fiscal_end_year, 3, 31)

    return fiscal_start_date, fiscal_end_date
