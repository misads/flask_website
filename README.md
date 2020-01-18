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

<img src="http://www.xyu.ink/wp-content/uploads/2020/01/flask2.png" style="zoom:80%;" alt="highlights" />

## Installation

 1. Run `./prepare.sh` to install dependencies (python2 for ubuntu).
 2. Set your MySql password.
 3. Modify [app/config.py](https://github.com/misads/flask_dempo/master/app/config.py) as you need. (defalut root password is '123456'.)

## Docker Image

We also provide a [Dockerfile](https://github.com/misads/flask_demo/blob/master/Dockerfile) for building an environment for running the code with **python3**.

```bash
docker build -t flask:py3 .  # 构建镜像

docker run -di -p 80:8000 -e MYSQL_ROOT_PASSWORD=123456 -v /Users/xhy/commits/flask_demo:/opt/flask flask:py3  # 启动容器 映射端口并挂载硬盘

# d558fef44828759e0dea9a097cd341c29a2df72b3644d20cb959b265d130cae5

docker exec -it d558fe /bin/bash  # 运行shell
```

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

