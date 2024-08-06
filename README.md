# hack-or-snooze-v4

# IMPORTANT CHANGES FROM PREVIOUS BACKEND!

- Token now must be sent in the _header_, not the body.
- `request.auth` stores the return value our ApiKey auth class (currently
  "user")

# Installation Guide:

Create and activate your venv:
```zsh
python3 -m venv venv
```

Install requirements:
```zsh
pip3 install -r requirements.txt
```

Create database (via PSQL):
```zsh
createdb hack_or_snooze
```

cd into directory containing `manage.py` and seed database:
```zsh
python manage.py migrate
```

Run server:
```zsh
python manage.py runserver
```

# How to Use This API

First, start by registering a new user using the **/api/users/signup** route
sending the following information:

    {
        "username": "string",
        "first_name": "string",
        "last_name": "string",
        "password": "string"
    }

Upon a successful request to that endpoint, you will receive a JSON payload
that includes your user details as well as a token. Like so:

    {
        "token": "your_username:token_data"
        "user": ...
    }

With your new token, you can now use all of the endpoints that require auth
(the endpoints marked with a lock). You will need to send this token in the
HEADERS of your request like so:

    HEADER: token: your_token

You can also supply this token to the **AUTHORIZE** button located at the top
of this documentation for usage in these interactive endpoints.