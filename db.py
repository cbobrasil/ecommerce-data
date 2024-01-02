#Import the packages 

from faker import Faker 
from pydbgen import pydbgen
import pandas as pd 
import random
import datetime

#Initiate the Faker and pydb objects 

fake = Faker()
ourDB= pydbgen.pydb()

#fucntion to create multiple simple profiles in Faker and pushes them into a Pandas dataframe 

def make_profile(x, y):
    Faker.seed_instance(x)
    profiles = pd.DataFrame([fake.profile() for _ in range(y)])
    profiles_created = datetime.datetime.now()
    return profiles 

profiles = make_profile(1989, 1000)
profiles.head()

Drivesrdf= ourDB.gen_dataframe(
1001,fields=('name','city','phone','license_plate','email'),
    real_email=True,phone_simple=True)
Driversdf

myDB.gen_table(1001,fields=['name','city','phone','company','job_title','email'],
               #Name your file 
               db_file='eDB022.db',
               #Name your table
               table_name='users',
primarykey='name',real_city=True)
