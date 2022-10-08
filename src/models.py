from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects import postgresql

from .database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    password = Column(String(100))
    name = Column(String, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    gender = Column(String(1), unique=True, nullable=False)
    birthdate = Column(Integer)
    is_active = Column(Boolean, default=1)
    privateKey = Column(String, unique=True)
    publicKey = Column(String, unique=True)

    def __repr__(self):
        return f'{self.__class__.__name__} (id={self.id}, name={self.username})'

'''
	"id"	INTEGER,
	"username"	TEXT UNIQUE,
	"password"  TEXT,
	"name"	TEXT,
	"mail" TEXT UNIQUE,
	"gender"	TEXT,
	"birthdate"  INTEGER,
	"is_active"  INTEGER DEFAULT 1,

'''




