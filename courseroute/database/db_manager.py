# courseroute/database/db_manager.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from configparser import ConfigParser

from courseroute.database.models import Base

def get_config(filename='config.ini', section='database'):
    parser = ConfigParser()
    parser.read(filename)
    db_config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    return db_config

def create_session():
    db_config = get_config()
    engine_str = f"postgresql://{db_config['user']}:{db_config['password']}@" \
                 f"{db_config['host']}:{db_config['port']}/{db_config['database']}"
    engine = create_engine(engine_str)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
