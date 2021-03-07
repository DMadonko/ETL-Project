#!/bin/bash

########################################################################
# initialise local and environment variables
########################################################################
#get root directory
echo "***************************************************************"
echo "** WELCOME TO ETL PROJECT!!!! INITIALISING..."
echo "***************************************************************"
directory=`pwd`
dataDirName="Kaggle_csvData"
kaggleConfigFile="${directory}/kaggle.json"
pythonConfigFile="${directory}/config.py"
booksTxtFile="${directory}/books.txt"
pgSchemaSqlFile="${directory}/sql_script.sql"
dataDir=${directory}/${dataDirName}
export KAGGLE_CONFIG_DIR=${directory}

echo "** Kaggle configuration file path set to \"${kaggleConfigFile}\""
echo "** Python configuration file path set to \"${pythonConfigFile}\""
echo "** Data directory path set to \"${dataDir}\""

########################################################################
# Create DIR's and config files
########################################################################
# install kaggle Python package
echo "***************************************************************"
echo "** Creating DIR's and config files..."
echo "***************************************************************"
echo "** Ensuring kaggle module is installed..."
pip install -q kaggle

echo "** Creating configuration files if not existing..."
# create kaggle.json config file
touch "${kaggleConfigFile}"

# create config.py config file
touch "${pythonConfigFile}"

# create books.txt file
touch "${booksTxtFile}"

# Create a directory to save the csv data
echo "** Creating data directory..."
if [ -d "${dataDir}" ] 
then
    echo "   ${dataDir} already exists, clearing data directory instead..."
    rm -f ${dataDir}/*.*
else
    mkdir ${dataDir}
fi

########################################################################
# Acquire required credentials and info from user
########################################################################
getCredentials(){
    # get kaggle username and api key
    echo "   Please enter you Kaggle UserID: "
    read kaggleId
    echo "   Please enter you Kaggle API KEY: "
    read kaggleAPIKey
    echo "   Your Kaggle user ID is \"${kaggleId}\" and your API key is \"${kaggleAPIKey}\""

    # get google api key from user
    echo "   Please enter you Google API Key: "
    read googleAPIkey

    # get pgadmin4 username and password
    echo "   Please enter you pgAdmin user name (default \"postgres\"): "
    read pgadminUser
    echo "   Please enter you pgAdmin password: "
    read pgadminPassword

    # get maximum googlebooks API calls
    echo "   Please enter the maximum number of google books API calls (must be an integer): "
    read maxCalls

    # save kaggle username and api key to config file
    echo "{\"username\":\"${kaggleId}\",\"key\":\"${kaggleAPIKey}\"}" > ${kaggleConfigFile}

    echo "** Populating config.py file with details"
    # save google api key to config file
    echo "# Google API Key" > ${pythonConfigFile}
    echo "g_key = \"${googleAPIkey}\"" >> ${pythonConfigFile}
    echo "# Max_data" >> ${pythonConfigFile}
    echo "maximum_data=${maxCalls}"  >> ${pythonConfigFile}

    # save pgAdmin user and password to config file
    echo "# PG Admin User" >> ${pythonConfigFile}
    echo "pg_user = \"${pgadminUser}\"" >> ${pythonConfigFile}
    echo "# PG Admin Password" >> ${pythonConfigFile}
    echo "pg_pass = \"${pgadminPassword}\"" >> ${pythonConfigFile}
} # end of getCredentials function

########################################################################
# Execute DB and Schema creation SQL file
########################################################################
getBooks(){
    echo ""
    echo "***************************************************************"
    echo "** Pulling books data from Kaggle API..."
    echo "***************************************************************"
    # List datasets matching the search term
    # kaggle datasets list -s goodreads

    # List files for the dataset
    echo ""
    echo "** Below are the list of CSVs from Kaggle: "
    kaggle datasets files bahramjannesarr/goodreads-book-datasets-10m > ${booksTxtFile}
    sed -i '1,2d' ${booksTxtFile}
    sort -o ${booksTxtFile} ${booksTxtFile}
    booksList=($(cat ${booksTxtFile} | awk '{print $1}'))
    printf '%s\n' "${booksList[@]}"
    numCSVs="${#booksList[@]}"
    echo ""

    # initialise CSV limit
    limit="5"

    # let user pick how many books to pull
    while :; do
    read -p "** Please enter the quantity of CSV files that you would like to download (1-${numCSVs}): " number
    [[ $number =~ ^[0-9]+$ ]] || { echo "Enter a valid number"; continue; }
    if ((number >= 1 && number <= ${numCSVs})); then
        limit=${number}
        echo "** You have chosen to download ${number} CSV files..."
        break;
    else
        echo "** number out of range, try again..."
    fi
    done

    # initialise counter
    ctr="1"

    # Download dataset files
    printf "\n** Downloading CSV files... \n"
    for i in "${!booksList[@]}"; do 
        kaggle datasets download bahramjannesarr/goodreads-book-datasets-10m -f "${booksList[$i]}"  -p ${dataDirName}
        if [ ${ctr} -eq ${limit} ]
        then
            break;
        else
            ctr=$[$ctr+1]
        fi
    done

    # Extract data
    unzip "${dataDir}/*.zip" -d "${dataDir}" 2> /dev/null
    # Delete Zip files
    rm -f ${dataDir}/*.zip  2> /dev/null

    printf "\n** Completed downloading books CSVs, below are the files downloaded..."
    ls -p -1 ./Kaggle_csvData
} # end of getBooks Function

########################################################################
# Execute DB and Schema creation SQL file
########################################################################
# set the PGUSER and PGPASSWORD environment variable
buildDB(){
    echo ""
    echo "***************************************************************"
    echo " ** Building the database and Schema..."
    echo "***************************************************************"
    # add postgre binaries path to $PATH
    export PATH="${PATH}:/C/Program Files/PostgreSQL/11/bin"
    export PGUSER=`grep "pg_user" ${pythonConfigFile} | cut -d '"' -f2` #pull from config if blank
    export PGPASSWORD=`grep "pg_pass" ${pythonConfigFile} | cut -d '"' -f2` #pull from config if blank
    # drop create DB
    dropdb --if-exists books_db
    createdb books_db
    # run SQL file
    psql -d books_db -f ${pgSchemaSqlFile}
} # End of buildDB function

########################################################################
# Execute python Cleanup script
########################################################################


# ask user if they want to configure credentials
echo ""
echo "***************************************************************"
echo "** Acquiring Credentials and configuration from user..."
echo "***************************************************************"
echo "** (Note: you can skip this if you have previously entered credentials)"
while true; do
    read -p "** Do you want to enter credentials and configuration parameters? [Y/N]:" yn
    case $yn in
        [Yy]* ) getCredentials;break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

# pull book data
getBooks
# build the database
buildDB

echo "helloWorld"
