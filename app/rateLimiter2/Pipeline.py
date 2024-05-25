from app.redisConnection import *
import string
import random

class Pipeline():
	def __init__(self):
		self.redisPipeline = redisConnection.pipeline()
		self.commands = []
		self.result = {}

	def strRandom(self, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(6))

	def addCommand(self, command, *args, subCommand=None):
		randomStr = self.strRandom()
		self.commands.append({'command': command, 'args': args, 'subCommand': subCommand, 'id': randomStr})
		if subCommand:
			tmp = getattr(self.redisPipeline, subCommand)()
			getattr(tmp, command)(*args)
			return randomStr

		getattr(self.redisPipeline, command)(*args)
		return randomStr

	def execute(self):
		res = self.redisPipeline.execute()
		for i, command in enumerate(self.commands):
			self.result[command['id']] = res[i]

	def getResult(self):
		return self.result