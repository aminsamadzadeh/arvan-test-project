from app.rateLimiter.rateLimiterHandler import RateLimiterHandler
import app.rateLimiter.helpers.datetime as datetimeHelper
import app.rateLimiter.helpers.pipeline as pipelineHelper

from app.redisConnection import *

class MonthRateLimiter(RateLimiterHandler):

	def get_hash(self):
		return f'month:{datetimeHelper.this_month_str()}:{self.user_id()}'

	@pipelineHelper.pipeline_is_not_none
	def increment(self, pipeline=None):
		pipeline.incr(self.get_hash())
		pipeline.expire(self.get_hash(), datetimeHelper.diff_now_to_next_month())

	def get(self):
		month_count = redisConnection.get(self.get_hash())
		if month_count:
			return int(month_count)
		return 0

	def is_limit(self):
		return self.get() > self.quotas.get_month()