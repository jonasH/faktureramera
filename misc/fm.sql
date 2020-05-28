CREATE TABLE bill (
       id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
       c_id int(11) REFERENCES customer(id) NOT NULL,
       reference varchar(30) NOT NULL,
       bill_date date NOT NULL,
       payed tinyint(1) NOT NULL DEFAULT '0',
       payed_date date DEFAULT NULL);
CREATE TABLE customer (
       id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
       name varchar(100) NOT NULL,
       address varchar(100) NOT NULL,
       zipcode varchar(100) NOT NULL);
CREATE TABLE jobs (
       id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
       b_id int(11) REFERENCES bill (id) NOT NULL,
       hours int(11) NOT NULL,
       price float NOT NULL,
       job varchar(50) NOT NULL);
