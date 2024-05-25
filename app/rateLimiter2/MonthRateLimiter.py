from app.rateLimiter2.RateLimiterHandler import RateLimiterHandler
import app.rateLimiter2.helpers.datetime as datetimeHelper
import app.rateLimiter2.helpers.pipeline as pipelineHelper

from app.redisConnection import *
from app.rateLimiter2.Quotas import *

class MonthRateLimiter(RateLimiterHandler):

	def getHash(self):
		return f'month:{datetimeHelper.thisMonthStr()}:{self.userId()}'

	def addCommands(self):
		self.get()
		self.increment()

	def increment(self):
		self.pipeline.addCommand('incr', self.getHash())
		self.pipeline.addCommand('expire', self.getHash(), datetimeHelper.diffNowToNextMonth())

	def get(self):
		self.keyList['month'] = self.pipeline.addCommand('get', self.getHash())

	def getResultMonth(self):
		return self.pipeline.getResult()[self.keyList['month']]

	def isLimit(self):
		month = self.getResultMonth()
		if month is None:
			return False
		return int(month) > self.quotas.getMonth()

	def statusCode(self):
		return 429