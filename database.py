from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import our models
from models.user import User
from models.mood import Mood
from models.notes import Notes
from models.visit import Visit

# Create a new engine and bind it to a session
engine = create_engine('sqlite:///store/database.db', connect_args={'check_same_thread': False})

DB_Session = sessionmaker(bind=engine)
db_session = DB_Session()

print ("database: Session created!")

def get_user_by_id(user_id):
	return db_session.query(User).filter_by(id=user_id).all()[0]

# Adds the model and commits the changes
def push_model(mdl):
	db_session.add(mdl)
	db_session.commit()

# Queries for a given model with a given filter
# e.g. query_for(User, User.name.in_(['ed', 'fakeuser']))
def get_session():
	return db_session


# FOR CREATING THE DATABASE
if __name__ == "__main__":
	User.__table__.create(engine)
	Mood.__table__.create(engine)
	Notes.__table__.create(engine)
	Visit.__table__.create(engine)
