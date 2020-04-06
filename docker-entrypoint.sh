#!/bin/bash

set -e
uwsgi --http :8001 --module app.wsgi
