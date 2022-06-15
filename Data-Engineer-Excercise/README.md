# Ortex Data Engineer Challenge
In this repository you will find my solutions to the coding challenges required for the [Data Engineer](https://public.ortex.com/data-engineer/) job position.

**Files descriptions**:
- ```table_creation.py``` is the script to create the table named *transactions* and insert the values from the CSV file. This table is used in ```part1.py```, so you must run it first.
- ```part1.py``` contains the solution to the Part 1 of the challenge.
- ```part2.py``` contains the solution to the Part 2 of the challenge.

**Additional remarks**: in order to connect to the DB to perform the queries in ```table_creation.py``` and ```part1.py```, you will need to create a file named *db_data.ini*, with the following structure:
```
[PostgreSQL]
user = <db_user>
pass = <db_pass>
host = <host>
port = <port>
db_name = <db_name>
```

Once finished, save it in the same folder of the scripts.

[Ortex](https://public.ortex.com/) is a fintech start-up that provides financial information and insights to institutions and private investors with data and analysis for the financial markets
