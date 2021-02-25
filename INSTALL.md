# tuneeco Feed Server

## Requirements
- python3+
- pip3+
- mysql or compatible


## Installation

### Setup virtual environment
```sh
python3 -m venv venv
source venv/bin/activate
```

### install stuff into venv
```sh
pip install -r requirements.txt
```

### Config env vars
```sh
cp .env_sample .env
vi .env
```

### Run migrations
```sh
./manage.py migrate
./manage.py createsuperuser
```

### Restore data
```sh
./manage.py loaddata sample-data.json
```

## Start Server
```sh
./manage.py runserver
```


## Process Queue
```sh
./manage.py process_videos
```