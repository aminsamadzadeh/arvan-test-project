from flask import request

import app.rateLimiter2.helpers.datetime as datetimeHelper
import app.rateLimiter2.helpers.pipeline as pipelineHelper
from app.rateLimiter2.duplicatedRateLimiter import DuplicatedRateLimiter
from app.rateLimiter2.minuteRateLimiter import MinuteRateLimiter
from app.rateLimiter2.monthRateLimiter import MonthRateLimiter
from app.rateLimiter2.pipeline import Pipeline

from app.redisConnection import *
from app.rateLimiter2.quotas import *

class RateLimiter():
	def __init__ (self):
		self.request_body = request.get_json()
		self.quotas = Quotas(self.user_id())
		self.pipeline = Pipeline()
		self.limiters = [
			DuplicatedRateLimiter(self.quotas, self.pipeline),
			MinuteRateLimiter(self.quotas, self.pipeline),
			MonthRateLimiter(self.quotas, self.pipeline)
		]

	def user_id(self):
		return self.request_body.get('user_id')

	def execute(self):
		for limiter in self.limiters:
			limiter.add_commands()
		self.pipeline.execute()

	def is_limit(self):
		for limiter in self.limiters:
			if limiter.is_limit():
				return True, limiter.status_code()
		return False, None

	
