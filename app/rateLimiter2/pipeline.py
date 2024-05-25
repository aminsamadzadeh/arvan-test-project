from app.redisConnection import *
import string
import random

class Pipeline():
	def __init__(self):
		self.redisPipeline = redisConnection.pipeline()
		self.commands = []
		self.result = {}

	def str_random(self, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(6))

	def add_command(self, command, *args, subCommand=None):
		random_str = self.str_random()
		self.commands.append({'command': command, 'args': args, 'subCommand': subCommand, 'id': random_str})
		if subCommand:
			tmp = getattr(self.redisPipeline, subCommand)()
			getattr(tmp, command)(*args)
			return random_str

		getattr(self.redisPipeline, command)(*args)
		return random_str

	def execute(self):
		res = self.redisPipeline.execute()
		for i, command in enumerate(self.commands):
			self.result[command['id']] = res[i]

	def get_result(self):
		return self.result