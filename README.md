# DRF img board API

REST API for an image board website using Django.
Built and tested on Ubuntu 22.04.

## Building

```
$ mkdir djangorf_imgboard && cd djangorf_imgboard
$ git clone https://github.com/moustafa-m/djangorf_imgboard.git
```

Create virtual environment:
```
$ python3 -m venv <env-name>
$ source <env-name>/bin/activate
```

Install dependencies:
```
$ cd djangorf_imgboard
$ pip install -r requirements.txt
```

Migrations:
```
$ python manage.py migrate
```

Run:
```
$ python manage.py runserver
```

To use any of the URLs in the [imgboard_app](imgboard_app/api/urls.py) you first need to register a user and use the auth token returned.

To register, send a request to ```/api/users/register/``` with the following data:
```
{
    "username": "",
    "email": "",
    "password": "",
    "password2": ""
}
```