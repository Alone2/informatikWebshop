FROM mysql:8

ENV MYSQL_ROOT_PASSWORD=1234

ADD setupDatabase.sql /docker-entrypoint-initdb.d
ADD my.cnf /etc/mysql/conf.d
EXPOSE 3306
