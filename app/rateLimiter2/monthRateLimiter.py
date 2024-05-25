from app.rateLimiter2.rateLimiterHandler import RateLimiterHandler
import app.rateLimiter2.helpers.datetime as datetimeHelper
import app.rateLimiter2.helpers.pipeline as pipelineHelper

from app.redisConnection import *

class MonthRateLimiter(RateLimiterHandler):

	def get_hash(self):
		return f'month:{datetimeHelper.this_month_str()}:{self.user_id()}'

	def add_commands(self):
		self.get()
		self.increment()

	def increment(self):
		self.pipeline.add_command('incr', self.get_hash())
		self.pipeline.add_command('expire', self.get_hash(), datetimeHelper.diff_now_to_next_month())

	def get(self):
		self.key_list['month'] = self.pipeline.add_command('get', self.get_hash())

	def get_result_month(self):
		return self.pipeline.get_result()[self.key_list['month']]

	def is_limit(self):
		month = self.get_result_month()
		if month is None:
			return False
		return int(month) > self.quotas.get_month()

	def status_code(self):
		return 429