from app.rateLimiter2.rateLimiterHandler import RateLimiterHandler
import app.rateLimiter2.helpers.datetime as datetimeHelper
import app.rateLimiter2.helpers.pipeline as pipelineHelper

from app.redisConnection import *
from app.env import *

class MinuteRateLimiter(RateLimiterHandler):

	def get_hash(self):
		return f'minute:{datetimeHelper.this_minute_str()}:{self.user_id()}'

	def add_commands(self):
		self.get()
		self.increment()

	def increment(self):
		self.pipeline.add_command('incr', self.get_hash())
		self.pipeline.add_command('expire', self.get_hash(), env('TTL_MINUTE'))

	def get(self):
		self.key_list['minute'] = self.pipeline.add_command('get', self.get_hash())

	def get_result_minute(self):
		return self.pipeline.get_result()[self.key_list['minute']]

	def is_limit(self):
		minute = self.get_result_minute()
		if minute is None:
			return False
		return int(minute) > self.quotas.get_minute()

	def status_code(self):
		return 429