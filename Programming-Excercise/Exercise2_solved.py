from datetime import datetime
'''
This task is to fix this code to write out a simple monthly report. The report should look professional.
The aim of the exercise is to:
- Ensure that the code works as specified including date formats
- Make sure the code will work correctly for any month
- Make sure the code is efficient
- Ensure adherence to PEP-8 and good coding standards for readability
- No need to add comments unless you wish to
- No need to add features to improve the output, but it should be sensible given the constraints of the exercise.
Code should display a dummy sales report
'''
### Do not change anything in the section below, it is just setting up some sample data
# test_data is a dictionary keyed on day number containing the date and sales figures for that day
month = "02"
test_data = {f"{x}": {"date": datetime.strptime(f"2021{month}{x:02d}", "%Y%m%d"),
                      'sales': float(x ** 2 / 7)} for x in range(1, 29)}
### Do not change anything in the section above, it is just setting up some sample data

# Start at 1th of February
start = test_data['1']

# End in the last day of February
end = test_data.get('29', test_data['28'])

def DateToDisplayDate(date):
    # E.g. Monday 8th February, 2021
    return (f"""{date.strftime("%a")} {date.strftime("%d")}th \
            {date.strftime("%B")}, {date.strftime("%Y")}""")

start["date"] = DateToDisplayDate(start["date"])
end["date"] = DateToDisplayDate(end["date"])

# Print the header of the report
print("Sales Report\nReport start date: " + start["date"].replace('  ', '') + \
      " | Starting value: $" + str(round(start["sales"], 2)) + \
      "\nReport end date: "  + end["date"].replace('  ', '') + \
      " | Total sales: $"    + str(round(end["sales"], 2))   + "\n")

total = 0
for k, v in enumerate(test_data):
    
    # Print the header of each row
    print("%-32s%-15s%-0s" % ("Date", "Sales", "Month to Date"))

    if month == "02" and k == 28:
        print("Leap year") # Must be displayed if data is for a leap year

    # String formatting for print
    string_format = "%-32s$%-14s$%-0s"

    if isinstance(test_data[v]['date'], datetime):
        # Get the date
        date = DateToDisplayDate(test_data[v]['date'])
        # Remove extra spaces
        date = date.replace('  ', '')
    else:
        # Get the date and remove extra spaces
        date = test_data[v]['date'].replace('   ', '')
    # Print
    print(string_format % \
          (date, \
           round(test_data[v]['sales'], 2), \
           round(total, 2))
        )
    total += test_data[v]['sales']
    print(f"Total sales for the month: ${total:.2f}\n")