from app.redisConnection import *

def pipeline_is_not_none(func): 
	def wrap(*args, **kwargs): 
		has_pipeline = 'pipeline' in kwargs or len(args) > 1
		if has_pipeline:
			return func(*args, **kwargs) 
		
		pipeline = redisConnection.pipeline()
		kwargs['pipeline'] = pipeline
		func(*args, **kwargs) 
		pipeline.execute()
		return
	return wrap 