from flask import request

import app.rateLimiter.helpers.datetime as datetimeHelper
import app.rateLimiter.helpers.pipeline as pipelineHelper
from app.rateLimiter.MinuteRateLimiter import MinuteRateLimiter
from app.rateLimiter.MonthRateLimiter import MonthRateLimiter

from app.redisConnection import *
from app.rateLimiter.Quotas import *

class RateLimiter():
	def __init__ (self):
		self.request_body = request.get_json()
		self.quotas = Quotas(self.userId())
		self.limiters = [
			MinuteRateLimiter(self.quotas),
			MonthRateLimiter(self.quotas)
		]

	def userId(self):
		return self.request_body.get('user_id')

	def requestId(self):
		return self.request_body.get('request_id')

	def increment(self):
		p = redisConnection.pipeline()
		for limiter in self.limiters:
			limiter.increment(p)
		p.execute()

	def isLimit(self):
		for limiter in self.limiters:
			if limiter.isLimit():
				return True
		return False

	def getReqHash(self):
		return f'requests:{self.requestId()}:{self.userId()}'

	def addToRequests(self):
		redisConnection.bf().add('requests', self.getReqHash())

	def isDuplicated(self):
		return redisConnection.bf().exists('requests', self.getReqHash())
