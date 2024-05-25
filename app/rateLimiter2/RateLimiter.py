from flask import request

import app.rateLimiter2.helpers.datetime as datetimeHelper
import app.rateLimiter2.helpers.pipeline as pipelineHelper
from app.rateLimiter2.DuplicatedRateLimiter import DuplicatedRateLimiter
from app.rateLimiter2.MinuteRateLimiter import MinuteRateLimiter
from app.rateLimiter2.MonthRateLimiter import MonthRateLimiter
from app.rateLimiter2.Pipeline import Pipeline

from app.redisConnection import *
from app.rateLimiter2.Quotas import *

class RateLimiter():
	def __init__ (self):
		self.request_body = request.get_json()
		self.quotas = Quotas(self.userId())
		self.pipeline = Pipeline()
		self.limiters = [
			DuplicatedRateLimiter(self.quotas, self.pipeline),
			MinuteRateLimiter(self.quotas, self.pipeline),
			MonthRateLimiter(self.quotas, self.pipeline)
		]

	def userId(self):
		return self.request_body.get('user_id')

	def execute(self):
		for limiter in self.limiters:
			limiter.addCommands()
		self.pipeline.execute()

	def isLimit(self):
		for limiter in self.limiters:
			if limiter.isLimit():
				return True, limiter.statusCode()
		return False, None

	
