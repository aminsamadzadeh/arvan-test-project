from datetime import datetime, timedelta

def this_month_str():
	return datetime.now().strftime('%Y-%m')

def this_minute_str():
	return datetime.now().strftime('%H-%M')

def first_day_of_next_month():
	now = datetime.now()
	next_month = now.replace(day=28) + timedelta(days=4)
	return (next_month - timedelta(next_month.day-1)).replace(hour=0, minute=0, second=0, microsecond=0)

def diff_now_to_next_month():
	return int((first_day_of_next_month() - datetime.now()).total_seconds())+1
