from datetime import date, timedelta

def get_current_month_min_max_dates():
    date_today = date.today()
    min_date = date_today.replace(day=1).strftime("%Y-%m-%d")
    max_date = (
        date_today.replace(
            month=date_today.month + 1
            ).replace(day=1) - timedelta(days=1)
        ).strftime("%Y-%m-%d")
    return min_date, max_date