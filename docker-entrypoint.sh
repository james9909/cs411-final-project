#!/bin/bash

set -e

# Wait for MySQL to set up
echo "Waiting for MySQL..."
host=`echo $SQLALCHEMY_DATABASE_URI | awk -F[@//] '{print $4}'`
while ! nc -z "${host}" 3306; do
    sleep 1
done
echo "MySQL is ready"

python3 manage.py db upgrade
python3 manage.py serve
