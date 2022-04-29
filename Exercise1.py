# Import native CSV librarie
import csv

# Open the CSV file
with open(file = '2017.csv', mode = 'r', encoding = 'utf8') as csv_file:
    
    # Map each line in the CSV into a dictionary
    transactions = csv.DictReader(csv_file, delimiter = ',')
        
    # Create an empty dictionary to store the results
    db = {
            'exchange_most_trans' : {},
            'highest_value_EUR'   : {},
            'trans_per_month'     : {}
        }

    month = {
                '01':'Jan',
                '02':'Feb',
                '03':'Mar',
                '04':'Apr',
                '05':'May',
                '06':'Jun',
                '07':'Jul',
                '08':'Aug',
                '09':'Sep',
                '10':'Oct',
                '11':'Nov',
                '12':'Dec'		
            }

    # Iterate the data
    for transaction in transactions:

        # Count the number of transactions by exchange
        if transaction['exchange'] not in db['exchange_most_trans'].keys():
            db['exchange_most_trans'][transaction['exchange']] = 1
        else:
            db['exchange_most_trans'][transaction['exchange']] += 1

        # Accumulate 'valueEUR' for each 'companyName' transactions in August 2017
        if transaction['inputdate'][:-2] == '201708':
            if transaction['companyName'] not in db['highest_value_EUR'].keys():
                db['highest_value_EUR'][transaction['companyName']] = float(transaction['valueEUR'])
            else:
                db['highest_value_EUR'][transaction['companyName']] += float(transaction['valueEUR'])

        # Percentage of transactions per month
        if transaction['inputdate'][:4] == '2017' and transaction['tradeSignificance'] == '3':
            if month[transaction['inputdate'][4:-2]] not in db['trans_per_month'].keys():
                db['trans_per_month'][month[transaction['inputdate'][4:-2]]] = 1
            else:
                db['trans_per_month'][month[transaction['inputdate'][4:-2]]] += 1

# Question and answer 1
print('Question 1: What Exchange has had the most transactions in the file?')
most_trans = max(db['exchange_most_trans'], key = db['exchange_most_trans'].get)
print('Answer 1: {}' . format(most_trans))
print('\n')

# Question and answer 2
print('Question 2: In August 2017, which companyName had the highest combined valueEUR?')
highest_key = max(db['highest_value_EUR'], key = db['highest_value_EUR'].get)
print('Answer 2: {}' . format(highest_key))
print('\n')

# Question and answer 3
print('Question 3: For 2017, only considering transactions with tradeSignificance 3, what is the percentage of transactions per month?')
total = sum(db['trans_per_month'].values())
print('Answer 3: ')
for key in db['trans_per_month']:
    db['trans_per_month'][key] /= total
    db['trans_per_month'][key] *= 100
    print(key + ', {}%' . format(round(db['trans_per_month'][key])))