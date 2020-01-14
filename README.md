# flask_demo
<p>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-Apache-brightgreen.svg" alt="License">
    </a>
</p>

A Flask CMS demo based on SqlAlchemy framework.

## Highlights

- [x] Register & Login
- [x] Database initiation
- [x] Index template

<img src="http://www.xyu.ink/wp-content/uploads/2020/01/flask.png" style="zoom:80%;" alt="highlights" />

## Installation

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

