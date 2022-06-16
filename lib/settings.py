import flask
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# подключение flask + DB
application = flask.Flask('application')
# немного магии с кодировкой
application.config['JSON_AS_ASCII'] = False
PG_DSN = f"postgresql://castom:castom@127.0.0.1:5432/advertisement"
engine = create_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine)