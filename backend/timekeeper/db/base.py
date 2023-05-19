from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine.url import URL

url = URL.create("postgresql", "postgres", "", "localhost", 5342, "time_db")
engine = create_engine(url, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
