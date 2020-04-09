# cs411-final-project

## Setting up

Dependencies:
* Docker

This project also requires 3 environment files: `env/mongo.env`, `env/mysql.env`, and `env/web.env`. These files are used to configure the various Docker containers.

Sample env files:

`env/mongo.env`:
```
MONGO_INITDB_ROOT_USERNAME=mymongouser
MONGO_INITDB_ROOT_PASSWORD=mymongopassword
```

`env/mysql.env`:
```
MYSQL_DATABASE=mydatabasename
MYSQL_USER=mysqluser
MYSQL_PASSWORD=mysqlpassword
MYSQL_ROOT_PASSWORD=this_doesnt_matter
MYSQL_RANDOM_ROOT_PASSWORD=yes
```

`env/web.env`:
```
SQLALCHEMY_DATABASE_URI=mysql+pymysql://mysqluser:mysqlpassword@mysql/mydatabasename
MONGODB_DATABASE_URI=mongodb://mymongouser:mymongopassword@mongodb
```

## Running the server

1) Run `./start.sh`
2) Go to `localhost:8000`

## Accessing the containers

To access any of the Docker containers, run `docker exec -it <container> /bin/sh`.

To access the MySQL database, connect to the MySQL container (sample id `cs411finalproject_mysql_1`) and run the following:
`mysql -u<username> -p<password>`.

Container names/ids can be found by running `docker ps`. For example:
```
$ docker ps
CONTAINER ID        IMAGE                   COMMAND                  CREATED             STATUS              PORTS                  NAMES
c182d9dbaf0b        nginx:1.17              "nginx -g 'daemon of…"   4 seconds ago       Up 3 seconds        0.0.0.0:8000->80/tcp   cs411finalproject_nginx_1
7f89986a304f        cs411finalproject_web   "sh ./docker-entrypo…"   5 seconds ago       Up 4 seconds                               cs411finalproject_web_1
e19302e12d55        mongo:4.2               "docker-entrypoint.s…"   7 seconds ago       Up 4 seconds        27017/tcp              cs411finalproject_mongodb_1
37a4d0c9ac89        mysql:8.0               "docker-entrypoint.s…"   7 seconds ago       Up 5 seconds        3306/tcp, 33060/tcp    cs411finalproject_mysql_1
$ docker exec -it cs411finalproject_mysql_1 /bin/sh
# mysql -umysqluser -pmysqlpassword
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 13
Server version: 8.0.19 MySQL Community Server - GPL

Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
```
