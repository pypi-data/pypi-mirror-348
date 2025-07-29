from datetime import datetime, timedelta

def get_current_time():
    return datetime.now()

def get_n_days_ago(n):
    return get_current_time() - timedelta(days=n)

def get_current_time_str():
    return get_current_time().strftime("%Y-%m-%d %H:%M:%S")

def get_current_date_str():
    return get_current_time().strftime("%Y-%m-%d")

def to_logger_time(time):
    return time.strftime("%d/%b/%Y")
