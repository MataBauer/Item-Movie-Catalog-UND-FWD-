import sys
import os

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(180), nullable=False)

    @property
    def serialize(self):
        # serilaized function will be send JSON ojbects in serializable format
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email
            }


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    creator_id = Column(Integer, ForeignKey('user.id'))
    creator = relationship(User)

    @property
    def serialize(self):
        # serilaized function will be send JSON ojbects in serializable format
        return{
            'id': self.id,
            'name': self.name,
            'creator_id': self.creator_id
            }


class Movie(Base):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False)
    published = Column(Integer)
    storyline = Column(String(600))
    poster = Column(String)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    creator_id = Column(Integer, ForeignKey('user.id'))
    creator = relationship(User)

    @property
    def serialize(self):
        # serilaized function will be send JSON ojbects in serializable format
        return {
            'id': self.id,
            'title': self.title,
            'published': self.published,
            'storyline': self.storyline,
            'category_id': self.category_id,
            'creator_id': self.creator_id
            }

# insert at end of file #
engine = create_engine('sqlite:///movies.db')
Base.metadata.create_all(engine)
