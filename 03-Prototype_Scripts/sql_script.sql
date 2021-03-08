--Create the books_db
DROP DATABASE IF EXISTS books_db;
CREATE DATABASE books_db;

--Drop any tables if they exist
DROP TABLE IF EXISTS book_titles CASCADE;
DROP TABLE IF EXISTS authors CASCADE;

--Create the book titles table
CREATE TABLE book_titles (
	ISBN int NOT NULL PRIMARY KEY,
	Name varchar NOT NULL,
	Authors varchar NOT NULL,
    Description varchar NOT NULL,
	Language varchar NOT NULL,
	PagesNumber int NOT NULL,
	Publisher varchar NOT NULL,
	PublishYear int NOT NULL,
    Rating int NOT NULL,
	