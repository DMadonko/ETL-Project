--Drop any tables if they exist
DROP TABLE IF EXISTS isbn_category CASCADE;
DROP TABLE IF EXISTS isbn_author CASCADE;
DROP TABLE IF EXISTS category CASCADE;
DROP TABLE IF EXISTS author CASCADE;
DROP TABLE IF EXISTS google_books CASCADE;
DROP TABLE IF EXISTS book_titles CASCADE;
DROP TABLE IF EXISTS print_type CASCADE;

--Create the book titles table
CREATE TABLE book_titles (
  "ISBN" VARCHAR(20) NOT NULL PRIMARY KEY,
  "Name" varchar NOT NULL,
  "Authors" varchar NOT NULL,
  "Description" varchar NOT NULL,
  "Language" varchar NOT NULL,
  "pagesNumber" int NOT NULL,
  "Publisher" varchar NOT NULL,
  "PublishYear" int NOT NULL,
  "Rating" int NOT NULL,
  "CountsOfReview" int NOT NULL
);

--Create the category table
CREATE TABLE category (
  category_id int NOT NULL PRIMARY KEY,
  category_name varchar NOT NULL 
);

--Create the ISBN_category table
CREATE TABLE isbn_category (
  isbn_no VARCHAR(20) NOT NULL,
  category_id int NOT NULL, 
  PRIMARY KEY(isbn_no,category_id),
  FOREIGN KEY (category_id) REFERENCES category (category_id)
);

--Create the author table
CREATE TABLE author (
  author_id int NOT NULL PRIMARY KEY,
  author_name varchar
);

--Create the ISBN_author table
CREATE TABLE isbn_author (
  isbn_no VARCHAR(20) NOT NULL,
  author_id int NOT NULL,
  PRIMARY KEY (isbn_no,author_id),
  FOREIGN KEY (author_id) REFERENCES author (author_id),
  FOREIGN KEY (isbn_no) REFERENCES book_titles ("ISBN")
);

--Create the print_type table
CREATE TABLE print_type (
  print_type_id int NOT NULL PRIMARY KEY,
  print_type varchar NOT NULL
);

--Create the google_books table
CREATE TABLE google_books (
  isbn_no VARCHAR(20) NOT NULL PRIMARY KEY,
  print_type_id int NOT NULL,
  retail_price money NOT NULL,
  FOREIGN KEY (print_type_id) REFERENCES print_type (print_type_id),
  FOREIGN KEY (isbn_no) REFERENCES book_titles ("ISBN")
);