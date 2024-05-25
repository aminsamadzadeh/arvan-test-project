import requests
import json
import random

total_time = 0
duplicated = 0
too_many = 0
ok = 0

def main():
	count = 1000
	for _ in range(count):
		send_req()
	print(':'*100)
	print('total_req:', count)
	print('total_time:', round(total_time, 1), 's')
	print('avg_time:', round((total_time/count)*1000, 1), 'ms')
	print('throughput:', round((count/total_time), 1), 'rps')
	print('ok:', ok)
	print('duplicated:', duplicated)
	print('too_many_request:', too_many)
	print(':'*100)

def get_payload():
	return json.dumps({
		"user_id": random.randint(1, 10),
		"request_id": random.randint(1, 1000)
	})

def send_req():
	global total_time, duplicated, too_many, ok
	url = "http://localhost:8080/sample"

	payload = get_payload()
	headers = {
	  'Accept': 'application/json',
	  'Content-Type': 'application/json'
	}

	response = requests.request("POST", url, headers=headers, data=payload)

	status_code = response.status_code

	if status_code == 400:
		duplicated += 1
		res = 'duplicated'

	if status_code == 429:
		too_many += 1
		res = 'too many request'

	if status_code == 200:
		ok += 1
		res = 'ok'

	total_time += response.elapsed.total_seconds()
	print('payload:', payload)
	print('status_code:', status_code)
	print('res:', res)
	print('time:', round(response.elapsed.total_seconds()*1000, 1), 'ms')
	print(':'*100)

if __name__ == '__main__':
	main()

