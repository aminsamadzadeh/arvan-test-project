from app.rateLimiter2.rateLimiterHandler import RateLimiterHandler
import app.rateLimiter2.helpers.datetime as datetimeHelper
import app.rateLimiter2.helpers.pipeline as pipelineHelper

from app.redisConnection import *

class DuplicatedRateLimiter(RateLimiterHandler):

	def get_hash(self):
		return f'requests:{self.request_id()}:{self.user_id()}'

	def add_commands(self):
		self.get()
		self.add()

	def add(self):
		self.pipeline.add_command('add', 'requests', self.get_hash(), subCommand='bf')

	def get(self):
		self.key_list['duplicated'] = self.pipeline.add_command('exists', 'requests', self.get_hash(), subCommand='bf')

	def get_result_duplicated(self):
		return self.pipeline.get_result()[self.key_list['duplicated']]

	def is_limit(self):
		return bool(self.get_result_duplicated())

	def status_code(self):
		return 400