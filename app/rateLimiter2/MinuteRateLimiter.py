from app.rateLimiter2.RateLimiterHandler import RateLimiterHandler
import app.rateLimiter2.helpers.datetime as datetimeHelper
import app.rateLimiter2.helpers.pipeline as pipelineHelper

from app.redisConnection import *
from app.rateLimiter2.Quotas import *
from app.env import *

class MinuteRateLimiter(RateLimiterHandler):

	def getHash(self):
		return f'minute:{datetimeHelper.thisMinuteStr()}:{self.userId()}'

	def addCommands(self):
		self.get()
		self.increment()

	def increment(self):
		self.pipeline.addCommand('incr', self.getHash())
		self.pipeline.addCommand('expire', self.getHash(), env('TTL_MINUTE'))

	def get(self):
		self.keyList['minute'] = self.pipeline.addCommand('get', self.getHash())

	def getResultMinute(self):
		return self.pipeline.getResult()[self.keyList['minute']]

	def isLimit(self):
		minute = self.getResultMinute()
		if minute is None:
			return False
		return int(minute) > self.quotas.getMinute()

	def statusCode(self):
		return 429