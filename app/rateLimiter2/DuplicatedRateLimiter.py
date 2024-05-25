from app.rateLimiter2.RateLimiterHandler import RateLimiterHandler
import app.rateLimiter2.helpers.datetime as datetimeHelper
import app.rateLimiter2.helpers.pipeline as pipelineHelper

from app.redisConnection import *
from app.rateLimiter2.Quotas import *

class DuplicatedRateLimiter(RateLimiterHandler):

	def getHash(self):
		return f'requests:{self.requestId()}:{self.userId()}'

	def addCommands(self):
		self.get()
		self.add()

	def add(self):
		self.pipeline.addCommand('add', 'requests', self.getHash(), subCommand='bf')

	def get(self):
		self.keyList['duplicated'] = self.pipeline.addCommand('exists', 'requests', self.getHash(), subCommand='bf')

	def getResultDuplicated(self):
		return self.pipeline.getResult()[self.keyList['duplicated']]

	def isLimit(self):
		return bool(self.getResultDuplicated())

	def statusCode(self):
		return 400