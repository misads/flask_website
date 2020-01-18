# python3.5
FROM mysql:5.7

RUN rm -f /etc/apt/sources.list
RUN echo "deb http://ftp.cn.debian.org/debian/ stretch main" > /etc/apt/sources.list
RUN echo "deb http://ftp.cn.debian.org/debian/ stretch-updates main" >> /etc/apt/sources.list
RUN echo "deb http://ftp.cn.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list


RUN apt-get update -qq && apt-get install -y \
    python3-pip \
    python3 \ 

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y tzdata

COPY requirements.txt /opt/
WORKDIR /opt/

RUN apt-get -y install libicu-dev

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

RUN apt-get install -y libmysqlclient-dev

RUN pip3 install mysqlclient

RUN apt-get install -y vim

EXPOSE 8000