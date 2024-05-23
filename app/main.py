from flask import Flask, jsonify, request
from app.env import *
from app.redisConnection import *

app = Flask(__name__)

@app.before_request
def before():
	print('before_request')


@app.post('/sample')
def sendOtp():
    jsonReq = valid.get_json()
    print('send to the queue')
    return jsonify({'status': True}), 200