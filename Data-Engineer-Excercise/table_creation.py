# For DB connection and queries handling
from sqlalchemy import create_engine, text

# For credentials
from configparser import ConfigParser

# Manage of paths and errors
import os
import sys

# Save the current directory path
dirname = os.path.dirname(__file__)

# Define the CSV file path
csv_path = os.path.join(dirname, '2017.csv')

# Parse data from the .ini file
config = ConfigParser()

# Path to the .ini file
ini_path = os.path.join(dirname, 'db_data.ini')

# Read the configuration file
if os.path.isfile(ini_path):
    config.read(ini_path)
else:
    print('ERROR: Please, check the db_data.ini file.')
    sys.exit()

# Load the credentials
USER = config['PostgreSQL']['user']
PASS = config['PostgreSQL']['pass']
HOST = config['PostgreSQL']['host']
PORT = config['PostgreSQL']['port']
DB_NAME = config['PostgreSQL']['db_name']

try: 
    # Connect to the DB
    engine = create_engine(
        f"postgresql+psycopg2://{USER}:{PASS}@{HOST}:{PORT}/{DB_NAME}"
    )
except:
    print('Something went wrong with the DB connection')
    sys.exit()

# Context management
with engine.connect() as conn:
    
    # Define the query to create the table and 
    # copy the data from the CSV file into it.
    q = f"""
    BEGIN;

    CREATE TABLE IF NOT EXISTS transactions(
        transactionID INT NOT NULL, 
        gvkey INT NOT NULL, 
        companyName TEXT, 
        companyISIN TEXT, 
        companySEDOL TEXT,
        insiderID INT NOT NULL, 
        insiderName TEXT, 
        insiderRelation TEXT, 
        insiderLevel TEXT,
        connectionType TEXT, 
        connectedInsiderName TEXT, 
        connectedInsiderPosition TEXT,
        transactionType TEXT, 
        transactionLabel TEXT, 
        iid TEXT, 
        securityISIN TEXT,
        securitySEDOL TEXT,
        securityDisplay TEXT, 
        assetClass TEXT, 
        shares NUMERIC NOT NULL, 
        inputdate DATE NOT NULL,
        tradedate DATE NOT NULL, 
        maxTradedate DATE, 
        price NUMERIC, 
        maxPrice NUMERIC, 
        value NUMERIC, 
        currency TEXT,
        valueEUR NUMERIC, 
        unit TEXT, 
        correctedTransactionID NUMERIC, 
        source TEXT,
        tradeSignificance INT NOT NULL, 
        holdings NUMERIC, 
        filingURL TEXT, 
        exchange TEXT,
        PRIMARY KEY(transactionID)
    );

    COPY transactions
    FROM '{csv_path}'
    DELIMITER ','
    CSV HEADER;

    COMMIT;
    """

    # Execute the query
    conn.execute(text(q))