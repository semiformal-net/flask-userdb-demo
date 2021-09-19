# pull official base image
FROM python:3.9.5-slim-buster

# set work directory
WORKDIR /usr/bin/sqlproxy

RUN apt-get update
RUN apt-get install -y default-mysql-client # mariadb, available as mysql

ADD https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 /usr/bin/sqlproxy
RUN chmod +x /usr/bin/sqlproxy/cloud_sql_proxy.linux.amd64

# copy project
COPY . /usr/bin/sqlproxy

# run entrypoint.sh
ENTRYPOINT ["/usr/bin/sqlproxy/entrypoint.sh"]