from sqlalchemy import create_engine, Column, Integer, String, Index, Date, Float
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

class ColdStoreIn(Base):
    __tablename__ = 'cold_store_in'
    ID = Column(Integer, primary_key=True, index=True)
    Sr_No = Column(String(50), index=True)
    Fi_No = Column(String(50), index=True)
    Date = Column(Date, index=True)
    Company = Column(String(100), index=True)
    Item = Column(String(100), index=True)
    Type = Column(String(50), index=True)
    Size = Column(String(50), index=True)
    Conversion = Column(String(50), index=True)
    Total_Mc = Column(Float)
    Total_Kg = Column(Float)
    Freezing_Type = Column(String(50), index=True)
    __table_args__ = (
        Index('idx_cold_store_in_company_date', 'Company', 'Date'),
    )    

# Function to connect to the database
def connect_to_db(username, password, host, port, database):
    connection_str = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_str, echo=True)
    Base.metadata.create_all(engine)  # Create tables if they don't exist
    Session = sessionmaker(bind=engine)
    return Session()

def add_row(session, a, b, c, d, e, f, g, h, i, j, k):
    new_row = ColdStoreIn(Sr_No=a, Fi_No=b, Date=c, Company=d, Item=e, Type=f, Size=g, Conversion=h, Total_Mc=i, Total_Kg=j, Freezing_Type=k)
    session.add(new_row)
    session.commit()
    return new_row

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

def show_crin(session):
    crins = session.query(ColdStoreIn).all()
    if  crins:
        data = [{
            'ID': crin.ID,
            'Sr_No': crin.Sr_No,
            'Fi_No': crin.Fi_No,
            'Date': crin.Date,
            'Company': crin.Company,
            'Item': crin.Item,
            'Type': crin.Type,
            'Size': crin.Size,
            'Conversion':crin.Conversion,
            'Total_Mc':crin.Total_Mc,
            'Total_Kg':crin.Total_Kg,
            'Freezing_Type':crin.Freezing_Type
        } for crin in crins]
        return pd.DataFrame(data)
    else:
        pass


def update_crin(session, a, c, d, e, f, g, h, i, j, k, l, m):
    crin = session.query(ColdStoreIn).filter_by(ID=a).first()
    if crin:
        
        crin.Sr_No = c
        crin.Fi_No = d 
        crin.Date = e
        crin.Company = f
        crin.Item = g
        crin.Type = h
        crin.Size = i
        crin.Conversion = j
        crin.Total_Mc = k
        crin.Total_Kg = l
        crin.Freezing_Type = m
        session.commit()
        return crin
    return None

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

def insert_coldstorein(session, *args):
    """
    Insert data into ColdStoreIn table.
    """
    new_row = ColdStoreIn(
        Sr_No=args[0],
        Fi_No=args[1],
        Date=args[2],
        Company=args[3],
        Item=args[4],
        Type=args[5],
        Size=args[6],
        Conversion=args[7],
        Total_Mc=args[8],
        Total_Kg=args[9],
        Freezing_Type=args[10]
    )
    session.add(new_row)
    session.commit()
    return new_row

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

    # Insert a new ColdStoreIn record
    new_crin = insert_coldstorein(session, '001', 'FI001', '2023-10-01', 'Company A', 'Item A', 'Type A', 'Size A', 'Conv A', 100.0, 200.0, 'Freezing A')
    print(f"Inserted ColdStoreIn record: {new_crin.ID}, {new_crin.Sr_No}")

