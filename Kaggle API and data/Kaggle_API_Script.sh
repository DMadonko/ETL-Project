#!/bin/bash

# install kaggle Python package
pip install kaggle

# Create a directory to save the csv data
mkdir Kaggle_csvData

# List datasets matching the search term
kaggle datasets list -s goodreads

# List files for a the dataset
kaggle datasets files bahramjannesarr/goodreads-book-datasets-10m

# Download dataset files
kaggle datasets download bahramjannesarr/goodreads-book-datasets-10m -f book1-100k.csv --unzip -p Kaggle_csvData 
kaggle datasets download bahramjannesarr/goodreads-book-datasets-10m -f book100k-200k.csv --unzip -p Kaggle_csvData 