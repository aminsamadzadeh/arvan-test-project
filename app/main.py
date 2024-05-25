from flask import Flask, jsonify, request
from app.env import *
from app.redisConnection import *
from app.rateLimiter.RateLimiter import *
from app.rateLimiter2.RateLimiter import RateLimiter as RateLimiter2

if not redisConnection.exists('requests'):
	redisConnection.bf().create('requests', 0.01, 1000)

app = Flask(__name__)

# @app.before_request
# def before():
# 	print('before_request')
# 	rt = RateLimiter()

# 	if rt.isDuplicated():
# 		return jsonify({'status': False}), 400

# 	rt.addToRequests()

# 	if rt.isLimit():
# 		return jsonify({'status': False}), 429

# 	rt.increment()

@app.before_request
def before2():
	print('before_request')
	rt = RateLimiter2()

	rt.execute()

	limit, statusCode = rt.isLimit()
	if limit:
		return jsonify({'status': False}), statusCode

@app.post('/sample')
def sample():
    print('send to the queue')
    return jsonify({'status': True}), 200

app.run(port=env('APIS_PORT'), host=env('APIS_HOST'))