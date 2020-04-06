import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    with open('.key', 'a+b') as f:
        f.seek(0)
        key = f.read()
        if len(key) == 0:
            key = os.urandom(32)
            f.write(key)
            f.flush()

        SECRET_KEY = key
