from app.rateLimiter.rateLimiterHandler import RateLimiterHandler
import app.rateLimiter.helpers.datetime as datetimeHelper
import app.rateLimiter.helpers.pipeline as pipelineHelper

from app.redisConnection import *
from app.env import *

class MinuteRateLimiter(RateLimiterHandler):

	def get_hash(self):
		return f'minute:{datetimeHelper.this_minute_str()}:{self.user_id()}'

	@pipelineHelper.pipeline_is_not_none
	def increment(self, pipeline=None):
		pipeline.incr(self.get_hash())
		pipeline.expire(self.get_hash(), env('TTL_MINUTE'))

	def get(self):
		minute_count = redisConnection.get(self.get_hash())
		if minute_count:
			return int(minute_count)
		return 0

	def is_limit(self):
		return self.get() > self.quotas.get_minute()