#!/bin/bash

set -e

# Wait for MySQL to set up
echo "Waiting for MySQL..."
host=`echo $SQLALCHEMY_DATABASE_URI | awk -F[@//] '{print $4}'`
while ! nc -z "${host}" 3306; do
    sleep 1
done
echo "MySQL is ready"

# Wait for MongoDB to set up
echo "Waiting for MongoDB..."
host=`echo $MONGODB_DATABASE_URI | awk -F[@//] '{print $4}'`
while ! nc -z "${host}" 27017; do
    sleep 1
done
echo "MongoDB is ready"

python3 manage.py db upgrade
python3 manage.py serve
