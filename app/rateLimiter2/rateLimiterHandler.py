from flask import request
from app.rateLimiter2.quotas import *

class RateLimiterHandler():
	def __init__ (self, quotas, pipeline):
		self.request_body = request.get_json()
		self.quotas = quotas
		self.pipeline = pipeline
		self.key_list = {}

	def user_id(self):
		return self.request_body.get('user_id')

	def request_id(self):
		return self.request_body.get('request_id')

	def status_code(self):
		pass

	def add_commands(self):
		pass