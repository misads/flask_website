# flask_demo
一个flask框架使用sqlalchemy的完整demo

## Install
 1. Run `./prepare.sh` to install dependencies(using apt and pip).
 2. Set a MySql password.
 3. Modify [app/config.py](https://github.com/misads/flask_dempo/master/app/config.py) to your liking.(defalut root password is '123456'.)

## Run
Run in a debug mode with the following command:
  `python serve.py`

Or you can use 'gunicorn' command to start this demo:
  `gunicorn --bind 0.0.0.0:8000 -w 4 "app:create_app()"`
