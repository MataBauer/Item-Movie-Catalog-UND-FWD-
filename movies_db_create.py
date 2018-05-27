from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from movies_db_mapping import Base, Category, Movie, User

engine = create_engine('sqlite:///movies.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create admin user / creator
admin = User(name="Mata", email="martina.cicel@gmail.com")

session.add(admin)
session.commit()


# Category - Animated movies
category1 = Category(name="Animated", creator=admin)

session.add(category1)
session.commit()

movie1 = Movie(title="Cloudy with a Chance of Meatballs",
               published=2009,
               storyline="A local scientist is often regarded as a failure \
until he invents a machine that can make food fall from the sky. But little \
does he know, that things are about to take a turn for the worst.",
               poster="/static/image/meatballs.jpg",
               category=category1, creator=admin)

session.add(movie1)
session.commit()

movie2 = Movie(title="Smurfs - The Lost Village",
               published=2017,
               storyline="In this fully animated, all-new take on the Smurfs, \
a mysterious map sets Smurfette and her friends Brainy, Clumsy, and Hefty on \
an exciting race through the Forbidden Forest, leading to the discovery of \
the biggest secret in Smurf history.",
               poster="/static/image/Smurfs_Lost_Village.jpg",
               category=category1, creator=admin)

session.add(movie2)
session.commit()

movie3 = Movie(title="Moana",
               published=2016,
               storyline="In Ancient Polynesia, when a terrible curse \
incurred by the Demigod Maui reaches Moana's island, she answers the Ocean's \
call to seek out the Demigod to set things right.",
               poster="/static/image/moana.jpg",
               category=category1, creator=admin)

session.add(movie3)
session.commit()

movie4 = Movie(title="The Boss Baby",
               published=2017,
               storyline="A suit-wearing, briefcase-carrying baby pairs up \
with his 7-year old brother to stop the dastardly plot of the CEO of Puppy \
Co.",
               poster="/static/image/boss.jpg",
               category=category1, creator=admin)

session.add(movie4)
session.commit()

movie5 = Movie(title="The Smurfs",
               published=2011,
               storyline="When the evil wizard Gargamel chases the tiny blue \
Smurfs out of their village, they tumble from their magical world into New \
York City.",
               poster="/static/image/smurfs.jpg",
               category=category1, creator=admin)

session.add(movie5)
session.commit()

# Category - Family movies
category2 = Category(name="Family", creator=admin)

session.add(category2)
session.commit()

movie1 = Movie(title="Because I Said So",
               published=2007,
               storyline="A meddling mother tries to set her daughter up with \
the right man so her kid won't follow in her footsteps.",
               poster="/static/image/Because.jpg",
               category=category2, creator=admin)

session.add(movie1)
session.commit()

movie2 = Movie(title="Gilmore Girls: A Year in the life",
               published=2016,
               storyline="Set nearly a decade after the finale of the \
original series, this revival follows Lorelai, Rory and Emily Gilmore through \
four seasons of change.",
               poster="/static/image/GG2016.jpg",
               category=category2, creator=admin)

session.add(movie2)
session.commit()

movie3 = Movie(title="Stardust",
               published=2007,
               storyline="In a countryside town bordering on a magical land, \
a young man makes a promise to his beloved that he'll retrieve a fallen star \
by venturing into the magical realm.",
               poster="/static/image/statdust.jpg",
               category=category2, creator=admin)

session.add(movie3)
session.commit()

movie4 = Movie(title="Grown Ups",
               published=2010,
               storyline="After their high school basketball coach passes \
away, five good friends and former teammates reunite for a Fourth of July \
holiday weekend.",
               poster="/static/image/Grownups.jpg",
               category=category2, creator=admin)

session.add(movie4)
session.commit()

# Category - Fun movies
category3 = Category(name="Fun", creator=admin)

session.add(category3)
session.commit()

movie1 = Movie(title="The Great Gatsby",
               published=2013,
               storyline="When his uptight CEO sister threatens to shut down \
his branch, the branch manager throws an epic Christmas party in order to \
land a big client and save the day, but the party gets way out of hand...",
               poster="/static/image/Gatsby.jpg",
               category=category3, creator=admin)

session.add(movie1)
session.commit()

movie2 = Movie(title="Office Christmas Party",
               published=2016,
               storyline="When his uptight CEO sister threatens to shut down \
his branch, the branch manager throws an epic Christmas party in order to \
land a big client and save the day, but the party gets way out of hand...",
               poster="/static/image/Office_Party.jpg",
               category=category3, creator=admin)

session.add(movie2)
session.commit()

movie3 = Movie(title="Bad Moms",
               published=2016,
               storyline="When three overworked and under-appreciated moms \
are pushed beyond their limits, they ditch their conventional \
responsibilities for a jolt of long overdue freedom, fun, and comedic \
self-indulgence.",
               poster="/static/image/Bad_Moms.jpg",
               category=category3, creator=admin)

session.add(movie3)
session.commit()

print ("Created database and filled it with data!")
