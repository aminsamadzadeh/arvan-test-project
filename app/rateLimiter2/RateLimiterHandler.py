from flask import request
from app.rateLimiter2.Quotas import *

class RateLimiterHandler():
	def __init__ (self, quotas, pipeline):
		self.request_body = request.get_json()
		self.quotas = quotas
		self.pipeline = pipeline
		self.keyList = {}

	def userId(self):
		return self.request_body.get('user_id')

	def requestId(self):
		return self.request_body.get('request_id')

	def statusCode(self):
		pass

	def addCommands(self):
		pass