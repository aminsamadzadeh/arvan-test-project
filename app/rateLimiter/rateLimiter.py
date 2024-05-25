from flask import request

import app.rateLimiter.helpers.datetime as datetimeHelper
import app.rateLimiter.helpers.pipeline as pipelineHelper
from app.rateLimiter.minuteRateLimiter import MinuteRateLimiter
from app.rateLimiter.monthRateLimiter import MonthRateLimiter

from app.redisConnection import *
from app.rateLimiter.quotas import Quotas

class RateLimiter():
	def __init__ (self):
		self.request_body = request.get_json()
		self.quotas = Quotas(self.user_id())
		self.limiters = [
			MinuteRateLimiter(self.quotas),
			MonthRateLimiter(self.quotas)
		]

	def user_id(self):
		return self.request_body.get('user_id')

	def request_id(self):
		return self.request_body.get('request_id')

	def increment(self):
		p = redisConnection.pipeline()
		for limiter in self.limiters:
			limiter.increment(p)
		p.execute()

	def is_limit(self):
		for limiter in self.limiters:
			if limiter.is_limit():
				return True
		return False

	def get_req_hash(self):
		return f'requests:{self.request_id()}:{self.user_id()}'

	def add_to_requests(self):
		redisConnection.bf().add('requests', self.get_req_hash())

	def is_duplicated(self):
		return redisConnection.bf().exists('requests', self.get_req_hash())
