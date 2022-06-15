# Path handling
import os

# Data manipulation
import pandas as pd


# Save the current directory path
dirname = os.path.dirname(__file__)

# Define the CSV file path
csv_path = os.path.join(dirname, '2017.csv')

# Load it into a DataFrame
df = pd.read_csv(csv_path)



"""/*** TASK 1 ***/"""
# Task 1: Which are the top 3 source with the highest ratio of Buy to 
# Sell transactions weighted by the number of shares per transaction?

# Filter only buy/sell transactions
task1 = df.query("transactionType == 'Buy' | transactionType == 'Sell'")

# Filter only 3 useful columns
task1 = task1.filter(items=['source', 'transactionType', 'shares'])

# Group the DataFrame by source and transactionType
group = task1.groupby(by=['source', 'transactionType'])

# Count the number of transactions for each source
transactions_count = group.count().reset_index()
# Rename share column
transactions_count.rename(
    columns={'shares': 'num_transactions'}, 
    inplace=True
)

# Sum the amount of shares per transaction
shares_per_transaction = group.sum().reset_index()
# Rename share column
shares_per_transaction.rename(
    columns={'shares': 'weight'}, 
    inplace=True
)

# Concatenate both DF
concat = pd.concat(
    objs=[transactions_count, shares_per_transaction['weight']], 
    axis=1
)

# Add a column with the product
concat['dot'] = concat['num_transactions'] * concat['weight']

# Auxiliary dict
result = {}

for source in concat['source'].unique():
    buy = concat.query(
        f"source=='{source}' & transactionType=='Buy'"
    )
    
    sell = concat.query(
        f"source=='{source}' & transactionType=='Sell'"
    )

    result[source] = buy['dot'].values[0]/sell['dot'].values[0]

# Put the results into a DF
result = pd.DataFrame(
    data={
        'source': result.keys(),
        'ratio': result.values()
    }
)

# Print the results
print('Answer to Task 1: ')
print(result.sort_values(by='ratio', ascending=False).iloc[:3])
print('\n')



"""/*** TASK 2 ***/"""
# Task 2: Which are the top 3 currency by the total 
# numerical value of trades in that currency?

task2 = df.filter(items=['currency', 'transactionID'])
task2 = task2.groupby('currency').count().reset_index()
task2.rename(
    columns={'transactionID': 'trade_count'}, 
    inplace=True
)

# Print the results
print('Answer to Task 2: ')
print(task2.sort_values(by='trade_count', ascending=False).iloc[:3])
print('\n')



"""/*** TASK 3 ***/"""
# Task 3: What is the total number of transactions where 
# inputdate was more than 2 weeks after tradedate?

# Filter only useful columns
task3 = df.filter(items=['inputdate', 'tradedate'])

# Cast to datetime
task3['inputdate'] = pd.to_datetime(task3['inputdate'], format='%Y%m%d')
task3['tradedate'] = pd.to_datetime(task3['tradedate'], format='%Y%m%d')

# Add a flag when satisfies the condition
task3['flag'] = task3['inputdate'] > task3['tradedate'] + pd.DateOffset(weeks=2)

# Print the results
print('Answer to Task 3: ')
print(task3[task3['flag']==True].shape[0])