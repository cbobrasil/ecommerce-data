#import library
from faker import Faker
import pandas as pd
import random
from random import randint 
import os
from datetime import datetime
import psycopg2
from sqlalchemy import create_engine

# Get the current date in the desired format
current_date = datetime.now().strftime("%Y-%m-%d")

#Generate Country and Language
fake=Faker(locale='id_ID')

#Geberate account table
def create_account(num_account):
    account=pd.DataFrame()
    for i in range(0,num_account):
        account.loc[i,'id']= str(randint(1245968, 9857483))
        account.loc[i,'first_name']=fake.first_name()
        account.loc[i,'last_name']=fake.last_name()
        account.loc[i,'email']=fake.ascii_free_email()
        account.loc[i,'phone_number']=fake.phone_number()
        account.loc[i,'is_verified']=fake.random_element(elements=("yes","no"))
        account.loc[i,'dt_user_creation']=fake.date_time_between(start_date='-2d', end_date='-1d', tzinfo=None)
    return account

#create 100 account
account=create_account(100)
#save data into csv
account.to_csv(f"account_{current_date}.csv",index=False)

#Generate Transaction Table
def transaction(num_trans):
    trans=pd.DataFrame()
    for i in range(0,num_trans):
        trans.loc[i,'transaction_id']= fake.bothify(text='FT#########')
        trans.loc[i,'created_at']=fake.date_time_between(start_date='-2y', end_date='now', tzinfo=None)
        trans.loc[i,'recipient_bank']=fake.random_element(elements=("Dana","Gopay","LinkAja","Ovo","Shopeepay","BRI","BNI","BSI","BCA",
                                                                    "Mandiri","JAGO","Maybank","Permata","Seabank","Muamalat","BJB"))
        trans.loc[i,'account_number']=fake.aba()
        trans.loc[i,'amount']=fake.random_int(min=10000, max=5000000, step=1000)
        trans.loc[i,'unique_code']=fake.random_int(min=50, max=999)
        trans.loc[i,'transaction_status']=fake.random_element(elements=("Need Confirmation","Checking","Processed","Success","Failed","Cancelled"))
    return trans
#generate 1000 transaction 
trans=transaction(10000)

#generate admin fee based on random 0 or 1500
trans['admin_fee']=random.choices([0,1500],k=len(trans))
#generate relational user id in account table and transaction table
trans['user_id']=random.choices(account["id"], k=len(trans))
#save data into csv
trans.to_csv(f"transaction_{current_date}.csv",index=False)

#Make Payment table
def payment(num_trans):
    payment=pd.DataFrame()
    for i in range(0,num_trans):
        payment.loc[i,'payment_id']= fake.bothify(text='FP#####')
        payment.loc[i,'send_at']=fake.date_time_between(start_date='-2y', end_date='now', tzinfo=None)
        payment.loc[i,'payment_method']=fake.random_element(elements=("BCA","BNI","BRI","BSI","CIMB","Danamon","Digibank","Mandiri","Muamalat","Permata","Jenius"))
        payment.loc[i,'account_number']=fake.aba()
        payment.loc[i,'payment_status']=fake.random_element(elements=("Success","Failed","Cancelled"))
    return payment

#generate 1000 payment process
pay=payment(10000)
#generate relational transaction id in trans table and payment table
pay['transaction_id']=random.choices(trans["transaction_id"], k=len(pay))
#save data into csv
pay.to_csv(f"payment_{current_date}.csv", index=False)


# Load data into PostgreSQL incrementally
engine = create_engine('postgresql://postgres:senha@localhost:5432/ecommerce')

# Function to load data into PostgreSQL incrementally
def load_to_postgres_incremental(table_name, data, engine):
    try:
        existing_data = pd.read_sql_table(table_name, engine)
        combined_data = pd.concat([existing_data, data]).drop_duplicates().reset_index(drop=True)
        combined_data.to_sql(table_name, engine, if_exists='replace', index=False)
    except Exception as e:
        print(f"Error loading data into PostgreSQL for {table_name}: {str(e)}")

# Load data incrementally into PostgreSQL
load_to_postgres_incremental('account', account, engine)
#load_to_postgres_incremental('transaction', trans, engine)
#load_to_postgres_incremental('payment', pay, engine)
        