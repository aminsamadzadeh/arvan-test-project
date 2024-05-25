from flask import request
from app.rateLimiter.Quotas import *

class RateLimiterHandler():
	def __init__ (self, quotas):
		self.request_body = request.get_json()
		self.quotas = quotas

	def userId(self):
		return self.request_body.get('user_id')

	def requestId(self):
		return self.request_body.get('request_id')

	def increment(self, pipeline=None):
		pass

	def isLimit(self):
		pass