# Basic authentication
This directory contains backend user data projects on Basic Authentication.

The following concepts will be considered at when managing the project:
- What authentication means
- What Base64 is
- How to encode a string in Base64
- What Basic authentication means
- How to send the Authorization header

## Requirements
The following requirements will be taken into account when managing these projects:

- All your files will be interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)
- Your code should use the pycodestyle style (version 2.5.)
- All your files must be executable
- The first line of all your files should be exactly #!/usr/bin/env python3

## Simple API

Simple HTTP API for playing with `User` model.


## Files

### `models/`
- `base.py`: base of all models of the API - handle serialization to file
- `user.py`: user model

### `api/v1`
- `app.py`: entry point of the API
- `views/index.py`: basic endpoints of the API: `/status` and `/stats`
- `views/users.py`: all users endpoints


## Setup
```
$ pip3 install -r requirements.txt
```


## Run
```
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```


## Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns an user based on the ID
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)
