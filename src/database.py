from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Database connection
# db_host = 'host'
# db_name = 'db'
# db_user = 'user'
# db_pass = 'pass'

SQLALCHEMY_DATABASE_URL = "sqlite:///../mt_web_8.db"
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://db:1qazxsw2@10.254.159.5/scrubing"
# SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # echo=True,
    # connect_args={"check_same_thread": False}
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
