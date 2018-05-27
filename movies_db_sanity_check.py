from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from movies_db_mapping import Base, Category, Movie, User

engine = create_engine('sqlite:///movies.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

print('=== Categories')
items = session.query(Category).all()
for item in items:
    print('id: %s; creator_id: %s; name: %s'
          % (item.id, item.creator_id, item.name))

print('\n=== Movies')
items = session.query(Movie).all()
for item in items:
    print('id: %s; category_id: %s; creator_id: %s; title: %s'
          % (item.id, item.category.id, item.creator_id, item.title))

print('\n=== Users')
items = session.query(User).all()
for item in items:
    print('id: %s; email: %s; name: %s'
          % (item.id, item.email, item.name))

print('\n')
