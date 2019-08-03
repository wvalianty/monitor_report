#FROM tiangolo/uwsgi-nginx:python3.6
# We copy just the requirements.txt first to leverage Docker cache
#RUN apt-get update &&  apt-get install  mysql-client -y

#这个镜像有一个问题，容器中不输出
#FROM frolvlad/alpine-python3
FROM python:3.6-alpine 
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
RUN apk --no-cache add ca-certificates tzdata

WORKDIR /app
COPY . /app
RUN pip3 install -r requirement.txt

ENTRYPOINT ["python", "-u"]
CMD ["run.py"]
