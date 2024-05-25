## Installation
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10-full
git clone
cd arvan
python3.10 -m venv .
source bin/activate
pip install -r requirements.txt
pip install -e .
cp .env.example .env
```

## Run

### Run server
```
cd arvan
source bin/activate
cd app
gunicorn -w 6 -b 127.0.0.1:8080 'main:app' #run with 6 worker and on port 8080
```

### Run tester
```
pip install requests
cd arvan/tester
python main.py
```

## Test Result
```
total_req: 8000
concurrent: 8
worker: 6
total_time: 6.3 s
avg_time: 6.3 ms
throughput: 1269 rps
```