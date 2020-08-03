DROP DATABASE swiftrail;
CREATE DATABASE swiftrail;

USE swiftrail;

CREATE TABLE users(
id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
email VARCHAR(255) NOT NULL,
username VARCHAR(255) NOT NULL,
password VARBINARY(255) NOT NULL,
first_name VARCHAR(40) NOT NULL,
last_name VARCHAR(40) DEFAULT '' NOT NULL,
gender ENUM('m','f', 'o') NOT NULL,
date_of_birth DATE NOT NULL,
country VARCHAR(40) NOT NULL,
phone_number VARCHAR(15) NOT NULL,
address VARCHAR(255) NOT NULL,
PRIMARY KEY (id),
UNIQUE (email),
UNIQUE (username));

CREATE TABLE station(
station_code VARCHAR(5) NOT NULL,
station_name VARCHAR(50) NOT NULL,
PRIMARY KEY (station_code),
UNIQUE (station_name));

CREATE TABLE train(
train_no CHAR(5) NOT NULL PRIMARY KEY,
train_name VARCHAR(50) NOT NULL,
UNIQUE (train_name));

CREATE TABLE train_details(
train_no CHAR(5) NOT NULL PRIMARY KEY,
source VARCHAR(5) NOT NULL,
destination VARCHAR(5) NOT NULL,
run_days VARCHAR(50) NOT NULL,
classes VARCHAR(50) NOT NULL,
FOREIGN KEY (train_no) REFERENCES train(train_no),
FOREIGN KEY (source) REFERENCES station(station_code),
FOREIGN KEY (destination) REFERENCES station(station_code));

CREATE TABLE seating(
train_no CHAR(5) NOT NULL,
max_seats SMALLINT UNSIGNED NOT NULL,
class ENUM('1A', '2A', '3A', 'SL', 'CC', '2S') NOT NULL,
FOREIGN KEY (train_no) REFERENCES train(train_no));

CREATE TABLE allotted_seats(
train_no CHAR(5) NOT NULL,
class ENUM('1A', '2A', '3A', 'SL', 'CC', '2S') NOT NULL,
seats SMALLINT UNSIGNED NOT NULL,
journey_date DATE NOT NULL,
FOREIGN KEY (train_no) REFERENCES train(train_no));

CREATE TABLE schedule(
train_no CHAR(5) NOT NULL,
station_code VARCHAR(5) NOT NULL,
arrival TIME NOT NULL,
departure TIME NOT NULL,
distance INT NOT NULL,
day INT NOT NULL,
FOREIGN KEY (train_no) REFERENCES train(train_no),
FOREIGN KEY (station_code) REFERENCES station(station_code));

CREATE TABLE ticket(
pnr CHAR(10) NOT NULL PRIMARY KEY,
transaction_id CHAR(20) NOT NULL UNIQUE,
source VARCHAR(5) NOT NULL,
boarding VARCHAR(5) NOT NULL,
destination VARCHAR(5) NOT NULL,
train_no CHAR(5) NOT NULL,
journey_date DATE NOT NULL,
class ENUM('1A', '2A', '3A', 'SL', 'CC', '2S') NOT NULL,
booked_by VARCHAR(255) NOT NULL,
FOREIGN KEY (source) REFERENCES station(station_code),
FOREIGN KEY (boarding) REFERENCES station(station_code),
FOREIGN KEY (destination) REFERENCES station(station_code),
FOREIGN KEY (train_no) REFERENCES train(train_no),
FOREIGN KEY (booked_by) REFERENCES users(username));

CREATE TABLE passenger(
pnr CHAR(10) NOT NULL,
name VARCHAR(20) NOT NULL,
age TINYINT UNSIGNED NOT NULL,
gender ENUM('m','f', 'o') NOT NULL,
seat_no SMALLINT UNSIGNED NOT NULL,
FOREIGN KEY (pnr) REFERENCES ticket(pnr));

CREATE TABLE transaction(
transaction_id CHAR(20) NOT NULL PRIMARY KEY,
transaction_date DATE NOT NULL,
amount DECIMAL(10,2),
booked_by VARCHAR(255) NOT NULL,
FOREIGN KEY (transaction_id) REFERENCES ticket(transaction_id),
FOREIGN KEY (booked_by) REFERENCES users(username));
