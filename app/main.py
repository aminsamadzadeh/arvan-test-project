from flask import Flask, jsonify, request
from app.env import *
from app.redisConnection import *
from app.rateLimiter.rateLimiter import RateLimiter
from app.rateLimiter2.rateLimiter import RateLimiter as RateLimiter2

if not redisConnection.exists('requests'):
	redisConnection.bf().create('requests', 0.01, 1000)

app = Flask(__name__)

@app.before_request
def before():
	print('before_request')
	rt = RateLimiter()

	if rt.is_duplicated():
		return jsonify({'status': False}), 400

	rt.add_to_requests()

	if rt.is_limit():
		return jsonify({'status': False}), 429

	rt.increment()

# @app.before_request
# def before2():
# 	print('before_request')
# 	rt = RateLimiter2()

# 	rt.execute()

# 	limit, status_code = rt.is_limit()
# 	if limit:
# 		return jsonify({'status': False}), status_code

@app.post('/sample')
def sample():
    print('send to the queue')
    return jsonify({'status': True}), 200

if __name__ == '__main__':
	app.run(port=env('APIS_PORT'), host=env('APIS_HOST'))