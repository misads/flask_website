# flask_demo
A operational Flask demo based on SqlAlchemy framework.

## Install
 1. Run `./prepare.sh` to install dependencies (for ubuntu).
 2. Set your MySql password.
 3. Modify [app/config.py](https://github.com/misads/flask_dempo/master/app/config.py) as you need. (defalut root password is '123456'.)

## Deploy
Run in debug mode:

```bash
# !-bash
python serve.py
```

Use gunicorn to start this demo in development mode:

```bash
gunicorn --bind 0.0.0.0:8000 -w 4 "app:create_app()"
```

