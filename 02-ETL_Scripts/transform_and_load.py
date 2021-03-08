#!/usr/bin/env python
# coding: utf-8

from sqlalchemy import create_engine
import pandas as pd
import os
import requests
import json
import config
import datetime
import time

dataDir='Kaggle_csvData'

column_names=['ISBN',
             'Name',
             'Authors',
             'Description',
             'Language',
             'pagesNumber',
             'Publisher',
             'PublishYear',
             'Rating',
             'CountsOfReview']

mainData=pd.DataFrame(columns = column_names)

# Loop through each file in the data directory and load the files in a dataframe for ETL
print ("\n***************************************************************")
print ("** START OF PYTHON AUTOMATED TRANSFORM AND LOAD TO -BOOKS_DB-")
print ("** Loading CSV Data to Data Frame...")
print ("***************************************************************")
for file in os.listdir(dataDir):
    filePath = '' + dataDir + '/' + os.fsdecode(file)
    print(f"Loading \"{filePath}\"")
    df = pd.read_csv(filePath)
    # workaround for files without 'description' column
    if 'Description' not in df.columns:
        df['Description']="None"
    # initial stage of ETL - filter required columns
    df = df[['ISBN',
             'Name',
             'Authors',
             'Description',
             'Language',
             'pagesNumber',
             'Publisher',
             'PublishYear',
             'Rating',
             'CountsOfReview']]
    # remove non-english characters from Name and Author
    df['Name']=df['Name'].str.replace('[^a-zA-Z0-9!@#$%^&*()-+?/`~"\':; ]', '')
    #df['Authors']=df['Authors'].str.replace('[^a-zA-Z0-9!@#$%^&*()-+?/`~"\':; ]', '')
    # drop rows with missing values
    df.dropna(how='any',inplace=True)
    # append CSV data to main dataframe
    mainData = mainData.append(df,ignore_index=True)

print("** Completed loading data to dataframe")

print("\n** Applying language filters and drop duplicates... ")
# filter languages & drop duplicates
enLanguages=['en-US','eng','en-GB','en-CA']
goodReadsData=mainData[mainData.Language.isin(enLanguages)].copy()
# sorting will keep the records with most reviews when duplicates are dropped
goodReadsData.sort_values(by='CountsOfReview',ascending=0,inplace=True)
goodReadsData = mainData[mainData.Language.isin(enLanguages)].drop_duplicates()
goodReadsData.drop_duplicates(subset='ISBN',inplace=True)
goodReadsData.drop_duplicates(subset='Name',inplace=True)
# Convert certain columns to INT
goodReadsData['CountsOfReview']=goodReadsData['CountsOfReview'].astype(int)
goodReadsData['pagesNumber']=goodReadsData['pagesNumber'].astype(int)
goodReadsData['PublishYear']=goodReadsData['PublishYear'].astype(int)

print("\n** Sorting Values... ")
goodReadsData.sort_values(by='Name',inplace=True)

# initialise DF's
print("\n** Initialising Google Books API data frames... ")
categoryDF = {"category_id":[],
             "category_name":[]}

isbn_categoryDF = {"isbn_no":[],
                   "category_id":[]}

authorDF = {"author_id":[],
            "author_name":[]}

isbn_authorDF = {"isbn_no":[],
                 "author_id":[]}

print_typeDF = {"print_type_id":[],
                "print_type":[]}

book_titlesDF= {"isbn_no":[],
                     "print_type_id":[],
                     "retail_price":[]}

# configure maximum Google books API call
print("\n** Limiting maximum API calls... ")
maxData = config.maximum_data
# get a list of ISBNs
isbn = goodReadsData['ISBN'].head(maxData)

# initialise ID's
category_id = 0
author_id = 0
print_type_id = 0

# initialise counters
timeoutMax=3
timeoutCtr=0
prc_cntr=0

# create URL
url=f'https://www.googleapis.com/books/v1/volumes?key={config.g_key}&q=isbn:'

# record runtime
startTime = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')

# loop through ISBNs and do a googlebooks API call

print ("\n***************************************************************")
print ("** Acquiring Google Books API data...")
print ("***************************************************************")
for i in isbn:

    # GET the API data
    response = requests.get(f"{url}{i}").json()
    prc_cntr += 1
    prcnt=round((prc_cntr/maxData)*100,0)

    # if response returns data then process the data
    try:
        if response['totalItems'] != 0:
            # reset timeout counter
            timeoutCtr=0

            # initialise authors list
            authors=[]

            print(f"RECORD {prc_cntr}: {prcnt}% - Processing ISBN No. {i}")

            # get author data
            try:
                authors=response['items'][0]['volumeInfo']['authors']
            except (KeyError, IndexError):
                authors.append(goodReadsData.loc[goodReadsData['ISBN'] == i]["Authors"].iloc[0])

            # get print_type data
            print_type=response['items'][0]['volumeInfo']['printType']

            # get categories data
            try:
                categories=response['items'][0]['volumeInfo']['categories']
            except (KeyError, IndexError):
                categories=[]

            # get list price data
            try:
                listPrice=response['items'][0]['saleInfo']['listPrice']['amount']
            except (KeyError, IndexError):
                listPrice=0.00   

            # load categories data in objects
            if len(categories) > 0:
                for c in categories:
                    cCaps = c.upper()
                    if cCaps not in categoryDF['category_name']: 
                        category_id += 1
                        categoryDF['category_id'].append(category_id)
                        categoryDF['category_name'].append(cCaps)
                        finalCatId = category_id
                    else: 
                        finalCatId = categoryDF['category_id'][categoryDF['category_name'].index(cCaps)]

                    isbn_categoryDF['isbn_no'].append(i)
                    isbn_categoryDF['category_id'].append(finalCatId)

            # load authors data in objects
            for a in authors:
                aCaps = a.upper()
                if aCaps not in authorDF['author_name']: 
                    author_id += 1
                    authorDF['author_id'].append(author_id)
                    authorDF['author_name'].append(aCaps)
                    finalAuthId = author_id
                else: 
                    finalAuthId = authorDF['author_id'][authorDF['author_name'].index(aCaps)]

                isbn_authorDF['isbn_no'].append(i)
                isbn_authorDF['author_id'].append(finalAuthId)

            # load print type data
            if print_type not in print_typeDF['print_type']:
                ptCaps = print_type.upper()
                print_type_id += 1
                print_typeDF['print_type_id'].append(print_type_id)
                print_typeDF['print_type'].append(ptCaps)
                finalPrintId = print_type_id
            else:
                finalPrintId = print_typeDF['print_type_id'][print_typeDF['print_type'].index(ptCaps)]

            # load google books data
            book_titlesDF['isbn_no'].append(i)
            book_titlesDF['print_type_id'].append(finalPrintId)
            book_titlesDF['retail_price'].append(listPrice)

        else:
            # skip if ISBN is not found
            print(f"RECORD {prc_cntr}: {prcnt}% - ISBN {i} not found. Skipping...")
    except (KeyError, IndexError):
        if timeoutCtr < timeoutMax:
            print(f"API Call timeout, resting for 20 seconds...")
            # increment timeout counter
            timeoutCtr += 1
            # sleep
            time.sleep(20)      
        else:
            print(f"ERROR: Maximum daily API call might have been reached, check API key...")
            break

endTime = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')

# record start and completion time
print(f"START TIME:     {startTime} \nCOMPLETION TIME: {endTime}\n")

# Convert directory of lists to DataFrames
book_titlesDF2=pd.DataFrame(goodReadsData)
google_booksDF=pd.DataFrame(book_titlesDF)
authorDF2=pd.DataFrame(authorDF)#.set_index('author_id')
categoryDF2=pd.DataFrame(categoryDF)#.set_index('category_id')
print_typeDF2=pd.DataFrame(print_typeDF)#.set_index('print_type_id')
isbn_categoryDF2=pd.DataFrame(isbn_categoryDF)#.set_index('isbn_no')
isbn_authorDF2=pd.DataFrame(isbn_authorDF)#.set_index('isbn_no')

#align Column names to database
book_titlesDF2.columns
book_titlesDF2

print ("\n***************************************************************")
print ("** Loading data to DB...")
print ("***************************************************************")

# create database connection
engine = create_engine(f'postgresql://{config.pg_user}:{config.pg_pass}@127.0.0.1/books_db')
connection = engine.connect()

# Ensure that destination tables are empty
engine.execute("DELETE FROM isbn_category")
engine.execute("DELETE FROM category")
engine.execute("DELETE FROM isbn_author")
engine.execute("DELETE FROM author")
engine.execute("DELETE FROM book_titles")
engine.execute("DELETE FROM print_type")

# Populate destination tables
book_titlesDF2.to_sql('book_titles', con=engine, if_exists='append', index=False)
print("Completed loading data for \"book_titles\" table...")
authorDF2.to_sql('author', con=engine, if_exists='append', index=False)
print("Completed loading data for \"author\" table...")
categoryDF2.to_sql('category', con=engine, if_exists='append', index=False)
print("Completed loading data for \"category\" table...")
print_typeDF2.to_sql('print_type', con=engine, if_exists='append', index=False)
print("Completed loading data for \"print_type\" table...")
isbn_categoryDF2.to_sql('isbn_category', con=engine, if_exists='append', index=False)
print("Completed loading data for \"isbn_category\" table...")
isbn_authorDF2.to_sql('isbn_author', con=engine, if_exists='append', index=False)
print("Completed loading data for \"isbn_author\" table...")
google_booksDF.to_sql('google_books', con=engine, if_exists='append', index=False)
print("Completed loading data for \"google_books\" table...")

# validate table count
book_titles_count=(engine.execute("SELECT COUNT(*) FROM book_titles").fetchall())[0][0]
author_count=(engine.execute("SELECT COUNT(*) FROM author").fetchall())[0][0]
category_count=(engine.execute("SELECT COUNT(*) FROM category").fetchall())[0][0]
print_type_count=(engine.execute("SELECT COUNT(*) FROM print_type").fetchall())[0][0]
isbn_category_count=(engine.execute("SELECT COUNT(*) FROM isbn_category").fetchall())[0][0]
isbn_author_count=(engine.execute("SELECT COUNT(*) FROM isbn_author").fetchall())[0][0]
print("\n\n***************************************************************")
print("** Please make sure all table data are populated as expected")
print("***************************************************************")
print(f"\"BOOK TITLES\" table count: {book_titles_count}")
print(f"\"AUTHOR\" table count: {author_count}")
print(f"\"CATEGORY\" table count: {category_count}")
print(f"\"PRINT_TYPE\" table count: {print_type_count}")
print(f"\"ISBN_CATEGORY\" table count: {isbn_category_count}")
print(f"\"ISBN_AUTHOR\" table count: {isbn_author_count}")
