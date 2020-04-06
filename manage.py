from flask import Flask
from flask_script import Manager, Server
from flask_migrate import MigrateCommand

from app import create_app
from app.models import db
import os

app = create_app()

manager = Manager(app)

ServerCommand = Server(host="0.0.0.0", port=8001, use_debugger=True, threaded=True)
manager.add_command("serve", ServerCommand)

manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
