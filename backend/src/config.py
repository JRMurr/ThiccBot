import os

DB_USER = os.getenv("DB_USER", "thicc")
DB_PASS = os.getenv("DB_PASS", "thicc")
DB_NAME = os.getenv("DB_NAME", "thicc")


class Config:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@postgres:5432/{DB_NAME}"
    )


class TestConfig(Config):
    TESTING = True
    pass
