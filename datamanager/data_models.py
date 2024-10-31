from sqlalchemy import Column, String, INTEGER, ForeignKey, Float,Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(Text, nullable=False)

    #  Define relationships to the other table
    movies = relationship('Movie', back_populates='user')


class Movie(Base):
    __tablename__ = 'movies'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    director = Column(String, nullable=False)
    year = Column(String, nullable=False)
    user_id = Column(INTEGER, ForeignKey('users.id'))

    #  Define relationships to the other table
    user = relationship('User', back_populates='movies')
