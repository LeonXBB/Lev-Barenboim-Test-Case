# some sql magic...

import databases
import sqlalchemy

from ..utils.env import get_env

secret_env = get_env("docker", True)
host_env = get_env("docker", False)

db = databases.Database(f"postgresql://admin:{secret_env('POSTGRES_PASSWORD')}@db:5432/default_database")
metadata = sqlalchemy.MetaData()

from .models.File import File
from .models.Log import Log

engine = sqlalchemy.create_engine(f"postgresql://admin:{secret_env('POSTGRES_PASSWORD')}@db:5432/default_database")
metadata.create_all(engine)
