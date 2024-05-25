from flask import request
from app.rateLimiter.quotas import Quotas

class RateLimiterHandler():
	def __init__ (self, quotas):
		self.request_body = request.get_json()
		self.quotas = quotas

	def user_id(self):
		return self.request_body.get('user_id')

	def request_id(self):
		return self.request_body.get('request_id')

	def increment(self, pipeline=None):
		pass

	def is_limit(self):
		pass