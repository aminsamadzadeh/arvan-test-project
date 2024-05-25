from app.rateLimiter.RateLimiterHandler import RateLimiterHandler
import app.rateLimiter.helpers.datetime as datetimeHelper
import app.rateLimiter.helpers.pipeline as pipelineHelper

from app.redisConnection import *
from app.rateLimiter.Quotas import *

class MonthRateLimiter(RateLimiterHandler):

	def getHash(self):
		return f'month:{datetimeHelper.thisMonthStr()}:{self.userId()}'

	@pipelineHelper.pipelineIsNotNone
	def increment(self, pipeline=None):
		pipeline.incr(self.getHash())
		pipeline.expire(self.getHash(), datetimeHelper.diffNowToNextMonth())

	def get(self):
		monthCount = redisConnection.get(self.getHash())
		if monthCount:
			return int(monthCount)
		return 0

	def isLimit(self):
		return self.get() > self.quotas.getMonth()