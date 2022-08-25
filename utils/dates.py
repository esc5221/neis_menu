import datetime


def week_start_end_date(date):
    if date is None:
        date = today()
    if type(date) is str:
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

    week_start_date = date - datetime.timedelta(days=date.weekday())
    week_end_date = week_start_date + datetime.timedelta(days=6)

    return week_start_date, week_end_date


def today():
    return datetime.date.today()
