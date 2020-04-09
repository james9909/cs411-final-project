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
