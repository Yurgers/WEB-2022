from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



SQLALCHEMY_DATABASE_URL = "sqlite:///../mt_web_8.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # echo=True,
    connect_args={"check_same_thread": False}
)
Session = sessionmaker(bind=engine,
                       autocommit=False,
                       autoflush=False,
                       )

Base = declarative_base()


# Dependency
def get_session():
    db = Session()
    try:
        yield db
    finally:
        db.close()
