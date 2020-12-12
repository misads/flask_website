# flask_website
<p>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-Apache-brightgreen.svg" alt="License">
    </a>
</p>

基于Flask和Mysql，使用Python语言快速搭建你的网站。支持后台管理，结构化功能模块，易于扩展。

## 在线demo

一个基于本项目部署网站的[[在线demo]](http://fundin.top/)

## 安装和部署

目前已完全支持Python3，不再推荐使用Python2的版本。

1. 安装Mysql-Server。运行：

   ```bash
   #!/bin/bash
   sudo apt-get install mysql-server
   ```

   安装时需要设置mysql的用户名和密码。

2. 安装系统依赖项。运行：

   ```bash
   sudo apt-get install libmysqlclient-dev
   sudo apt-get install build-essential libffi-dev
   ```

3. 安装Python和pip（如果系统已经有python和pip则可以跳过此步）

   ```bash
   sudo apt-get install python-dev python-pip
   ```


4. 安装Python依赖：

   ```
   sudo pip install -r requirements.py35.txt
   ```

5. 在`app/config.py`文件中将`SQLALCHEMY_DATABASE_URI`字符串更改为你的mysql密码。

   ```bash
   SQLALCHEMY_DATABASE_URI = 'mysql://root:<password>@localhost:3306/flask'
   ```

   将`<password>`替换为你的mysql root密码。

6. 运行：

   - 以**开发者**模式运行：

   ```bash
   # !-bash
   python serve.py
   ```

   `flask_website`默认运行在`8000`端口。你可以通过修改`serve.py`来改变端口。

   - 以生产环境运行：

   ```python
   # !-bash
   gunicorn --bind 0.0.0.0:8000 -w 4 "app:create_app()"
   ```

   这里的`0.0.0.0:8000`是监听的端口，`-w`表示启动的进程数。

## Anaconda

你可以使用Anaconda创建flask需要的虚拟环境，步骤如下：

1. 创建一个新环境：

   ```bash
   conda create -n flask python=3.6
   ```

2. 进入环境：

   ```bash
   conda activate flask
   ```

3. 安装所需要的包

   ```python
   pip install -r requirements.py35.txt
   ```

## Docker镜像

如果你更倾向于使用docker搭建环境，我们同样提供了一个[[Dockerfile]](https://github.com/misads/flask_demo/blob/master/Dockerfile) 。

```bash
docker build -t flask:py3 .  # 构建镜像

docker run -di -p 80:8000 -e MYSQL_ROOT_PASSWORD=123456 -v /Users/xhy/commits/flask_demo:/opt/flask flask:py3  # 启动容器 映射端口并挂载硬盘

# d558fef44828759e0dea9a097cd341c29a2df72b3644d20cb959b265d130cae5

docker exec -it d558fe /bin/bash  # 运行shell
```
