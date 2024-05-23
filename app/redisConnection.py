import redis
from app.env import *

redisConnection = redis.Redis(host=env('REDIS_HOST'), port=env('REDIS_PORT'), db=0)