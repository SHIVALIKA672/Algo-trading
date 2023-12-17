import sqlite3

conn = sqlite3.connect('stocks.db')
conn.execute('''CREATE TABLE COMPANY
         (
         NAME           TEXT not null  PRIMARY KEY UNIQUE,
         Price           float     NOT NULL,
         change       float     NOT NULL,
         change_percentage         float     NOT NULL,
         volume int not null);''')

conn.execute('''CREATE TABLE transactions
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         Price           float     NOT NULL,
         quantity       int     NOT NULL,
         date         datetime default current_timestamp,
         type varchar(4)
         );''')

conn.execute('''CREATE TABLE networth
         (ID INT PRIMARY KEY     NOT NULL,
         date         datetime default current_timestamp,
         networth float,
         profits float,
         profits_inmarket float,
         invested_amount float
         );''')