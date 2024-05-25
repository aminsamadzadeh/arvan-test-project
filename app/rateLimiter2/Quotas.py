from app.redisConnection import *
from app.env import *

class Quotas():
	def __init__(self, user_id):
		self.user_id = user_id
		self.quotas = self.get()

	def getQuotaHash(self):
		return f'quotas:{self.user_id}'

	def get(self):
		return redisConnection.hmget(self.getQuotaHash(), ['month', 'minute'])

	def getMonth(self):
		month = self.quotas[0]
		if not month:
			return int(env('QUOTAS_MONTH'))
		return int(month)

	def getMinute(self):
		minute = self.quotas[1]
		if not minute:
			return int(env('QUOTAS_MINUTE'))
		return int(minute)