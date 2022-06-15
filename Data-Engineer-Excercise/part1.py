""" /*** LIBRARIES IMPORTATION ***/ """
# For DB connection and queries handling
from sqlalchemy import create_engine, text

# For credentials
from configparser import ConfigParser

# Manage of paths and errors
import os
import sys


""" /*** DB CONNECTION ***/ """

# Save the current directory path
dirname = os.path.dirname(__file__)

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


""" /*** QUERIES ***/ """

# Context management
with engine.connect() as conn:

    # /*** TASK 1 ***/
    task1 = """
    SELECT
        exchange, 
        COUNT(exchange) AS unique_exchanges
    FROM 
        transactions
    GROUP BY
        exchange
    ORDER BY 
        unique_exchanges DESC
    LIMIT 3;
    """
    result = conn.execute(text(task1))

    print("Task 1: Which are the top 3 exchange with " + \
          "the most transactions in the file?")
    for row in result.fetchall():
        print(row[0])

    
    # /*** TASK 2 ***/
    task2 = """
    SELECT
        DISTINCT companyName,
        SUM(valueEUR) OVER(PARTITION BY companyName) AS total_value
    FROM 
        transactions
    WHERE 
        TO_CHAR(inputdate, 'YYYY-MM') = '2017-08'
    ORDER BY
        total_value DESC
    LIMIT 2;
    """

    result = conn.execute(text(task2))

    print("\nTask 2: In August 2017, which 2 companyNames " + \
          "had the highest combined valueEUR?")
    for row in result.fetchall():
        print(row[0])


    # /*** TASK 3 ***/
    task3 = """
    SELECT
        COUNT(transactionID) AS trans,
        TO_CHAR(inputdate, 'Mon') AS month,
        TO_CHAR(inputdate, 'MM') AS num_month
    FROM 
        transactions
    WHERE 
        EXTRACT(YEAR FROM inputdate) = 2017
    AND
        tradeSignificance = 3
    GROUP BY
        num_month, month
    ORDER BY
        num_month ASC;
    """

    result = conn.execute(text(task3))

    print("\nTask 3: For 2017, only considering " + \
          "transactions with tradeSignificance 3, what " + \
          "is the percentage of transactions per month?")
    
    result = result.fetchall()
    total = sum([i[0] for i in result])
    
    for row in result:
        print(row[1], round(100*row[0]/total, 2), '%')