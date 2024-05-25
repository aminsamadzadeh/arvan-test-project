from app.rateLimiter.RateLimiterHandler import RateLimiterHandler
import app.rateLimiter.helpers.datetime as datetimeHelper
import app.rateLimiter.helpers.pipeline as pipelineHelper

from app.redisConnection import *
from app.rateLimiter.Quotas import *
from app.env import *

class MinuteRateLimiter(RateLimiterHandler):

	def getHash(self):
		return f'minute:{datetimeHelper.thisMinuteStr()}:{self.userId()}'

	@pipelineHelper.pipelineIsNotNone
	def increment(self, pipeline=None):
		pipeline.incr(self.getHash())
		pipeline.expire(self.getHash(), env('TTL_MINUTE'))

	def get(self):
		minuteCount = redisConnection.get(self.getHash())
		if minuteCount:
			return int(minuteCount)
		return 0

	def isLimit(self):
		return self.get() > self.quotas.getMinute()