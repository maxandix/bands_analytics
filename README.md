# API for rest.bandsintown.com analysis

2 Endpoints are available:
 - `/api/artist/<artist_name>/` - goes to https://rest.bandsintown.com/artists/{artist_name}/events?app_id=11&date=all with requested artist_name and return "the most favourite" artist's place to perform. Response is one string formated as 'City, Country'.
 - `/api/history/` - returns list of artist's names from your last 10 searches


## Run

To run you need Python 3.

Download code from GitHub. Install dependencies:

```sh
pip install -r requirements.txt
```

Create a database SQLite

```sh
python3 manage.py migrate
```

Run server:

```
python3 manage.py runserver
```

The service will be at [127.0.0.1:8000](http://127.0.0.1:8000)
