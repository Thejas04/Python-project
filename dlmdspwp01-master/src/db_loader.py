from numpy import genfromtxt
from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
import os
from db import connection_manager
from sqlalchemy.orm import sessionmaker

print(os.getcwd())


def Load_Data(file_name):
    data = genfromtxt(file_name, delimiter=',', skip_header=1, converters={0: lambda s: str(s)})
    return data.tolist()

def define_session():

    #Create the database
    engine = connection_manager.get_connection()

    #Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()
    
    return s