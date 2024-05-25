from datetime import datetime, timedelta

def thisMonthStr():
	return datetime.now().strftime('%Y-%m')

def thisMinuteStr():
	return datetime.now().strftime('%H-%M')

def firstDayOfNextMonth():
	now = datetime.now()
	next_month = now.replace(day=28) + timedelta(days=4)
	return (next_month - timedelta(next_month.day-1)).replace(hour=0, minute=0, second=0, microsecond=0)

def diffNowToNextMonth():
	return int((firstDayOfNextMonth() - datetime.now()).total_seconds())+1
