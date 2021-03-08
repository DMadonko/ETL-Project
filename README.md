#########################################################################
# ETL-Project
#########################################################################
### ETL Project Proposal

Team Members: 
1.	Raphael Serrano
2.	Swobabika Jena
3.	Thomas Maina
4.	Diana Madonko

### Project overview 

Our question of interest is to explore published books around the world and related information. This data will be able to assist people with book choices as it would provide more information on ratings, affordability and other areas that influence their choices.


### EXTRACT - Proposed data sources
•	Where is the data located?
1. Kaggle
2. Google books
•	What are the data set formats? 
1. csv
2. JSON
•	How will you get this data? (e.g. API, scraped data, download data)
1. API (downloading CSV files)
2. API
•	Our data will provide the following information:
~ ISBN
~ Book Name
~ Authors
~ Description
~ Language
~ Pages Number
~ Publisher
~ Publish Year
~ Rating
~ Country
~ Retail Price
~ Print Type


### TRANSFORM - Proposed clean-up and analysis
•	What are the transformations you will apply to the data? (e.g. filtering, aggregation, derived columns)
Filtering and derived columns
•	What steps will you take to clean the data and ensure its validity (e.g. messy data, duplicated data, incorrectly formatted data)
Deduplication, format revision and cleaning values.
•	How will you identify potential issues with your data sources? (e.g. exploratory data analysis, simple statistics etc)
Exploratory data analysis
•	How will the data be integrated? (e.g. joins, merges)
Merges
•	How will you apply these transformations (e.g. jupyter notebook, python script)
Jupyter Notebook
•	IMPORTANT → Why did you apply these transformations? How did this enrich your data?
We have chosen these transformations as they best suit the data we have selected.


### LOAD - Data storage
•	What type of database (relational, document) will you store the data?
Relational database
•	Why did you choose this database over another database?
We chose this database as it will allow us to easily apply analytical functions and derived data
•	What are your expected tables / documents and relationships between tables / documents in your database?
Our tables will be Book data, Review Ratings, Authors

Potential limitations
•	What are the potential limitations of your above proposed steps? 
~ The potential limitations we can run into is the dataset having limited data than expected 
~ There could be missing fields that we need

•	How can you control these potential issues?
~ We will explore different sources of data.

#########################################################################
# Navigating Folders
#########################################################################
### 01-Documentation
Contains the following files:
* **"ETL Project Proposal - Team 4.docx"** - Project proposal document
* **"ETL Project Report.docx"** - Document with details of the project and inferences gathered from the project

### 02-ETL_Scripts
Contains the following files:
* **"ETL_automation_Script.sh"** - The script acts as a wrapper script for both **sql_script.sql** file and **transform_and_load.py** file. It automates the ETL sequence: 
    - Setting up enfironment variables
    - Acquiring user credentials and setting API call limits
    - Creating necessary files and directories
    - Downloading CSV files from KAggle API call
    - Creating the database and tables
    - Loading and clensing data using DataFrames
    - Uploading data to the Database
* **sql_script.sql** - Contains the SQL code to create tables, called by **"ETL_automation_Script.sh"**
* **transform_and_load.py** - Contains the python script to load CSVs to dataframes, cleanse the data and load the data to the DB
* **bookData_analysis.ipynb** - Contains the python scripts and visualisation for analysing data

### 03-Prototype_Scripts
Contains files used for prototyping








