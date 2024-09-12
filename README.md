Generate fake Relational Data


based on :
https://khofifah.medium.com/how-to-generate-fake-relational-data-in-python-and-getting-insight-using-sql-in-bigquery-985c5adc87d3



create table public.account(
id SERIAL PRIMARY KEY,
first_name varchar(300),
last_name varchar(300),
email varchar(300),
phone_number varchar(300),
is_verified varchar(3),
dt_user_creation date
);


create table public.transaction(
transaction_id SERIAL PRIMARY KEY,
created_at date,
recipient_bank varchar(300),
account_number int,
amount decimal(18,2),
unique_code int,
transaction_status varchar(300)
);


