from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
# Define base model
Base = declarative_base()

# Define a sample table model (for example, a 'User' table)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    age= Column(Integer)

# Function to connect to the database
def connect_to_db(username, password, host, port, database):
    connection_str = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_str, echo=True)
    Base.metadata.create_all(engine)  # Create tables if they don't exist
    Session = sessionmaker(bind=engine)
    return Session()

# Function to add a new user
def add_user(session, name, email):
    new_user = User(name=name, age=email)
    session.add(new_user)
    session.commit()
    return new_user

# Function to edit an existing user
def edit_user(session, user_id, new_name=None, new_email=None):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        if new_name:
            user.name = new_name
        if new_email:
            user.email = new_email
        session.commit()
        return user
    return None

# Function to delete a user by ID
def delete_user(session, user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        return True
    return False

def show_data(session):
    users = session.query(User).all()
    if users:
        data = [{
            'ID': user.id,
            'Name': user.name,
            'Age': user.age
        } for user in users]
        return pd.DataFrame(data)
    else:
        return pd.DataFrame(columns=['ID', 'Name', 'Email'])
# ... existing code ...

# Function to update user data
def update_user(session, user_id, new_name, new_age):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        user.name = new_name
        user.age = new_age
        session.commit()
        return user
    return None

# ... existing code ...    

if __name__ == "__main__":
    session = connect_to_db('username', 'password', 'localhost', '3306', 'test_db')

    # Add a new user
    added_user = add_user(session, 'John Doe', 'john@example.com')
    print(f"Added user: {added_user.name}, {added_user.email}")

    # Edit the user
    updated_user = edit_user(session, added_user.id, new_name='Johnny Doe', new_email='johnny@example.com')
    if updated_user:
        print(f"Updated user: {updated_user.name}, {updated_user.email}")

    # Delete the user
    delete_success = delete_user(session, added_user.id)
    if delete_success:
        print("User deleted successfully.")
