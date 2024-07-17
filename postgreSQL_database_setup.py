##  Building a database for crime reports ##
### Objective: 
#   create a Postgres database of boston crime data
#   create a Postgres schema ('crimes') for the table
#   create seperate group privileges for analysts (read) & data scientist (read & write)
#   populate groups with users 

# Creating the Crime Database #
import csv
from pprint import pprint

import psycopg2

csv_filename = 'boston.csv'
conn = psycopg2.connect(dbname="postgres", user="postgres", password = '2611')
conn.autocommit = True # set autocommit to 'True' to create db
cursor = conn.cursor()

# Create Database #
cursor.execute("CREATE DATABASE crime_db;")

# Disconnect from postgres db and reconnect to crime_db
conn.close()
conn = psycopg2.connect(dbname="crime_db", user="postgres", password = '2611')
conn.autocommit = True # set autocommit to 'True' to create db
cursor = conn.cursor()

# Create 'crimes' schema witing crime_db #
cursor.execute("CREATE SCHEMA crimes;")

# Read in crime data (csv) #
with open(csv_filename) as file:
    reader = csv.reader(file)
    col_header = next(reader)
    first_row = next(reader) 
    print(len(col_header))

# Create function to retrieve proper data types #
def get_col_set(csv_file, col_index):
    # import csv (if not already)
    values = set()
    with open(csv_file, 'r') as f:
        next(f)
        file = csv.reader(f)
        for i in file:
            values.add(i[col_index])
        return values

# Loop through each column and retrieve the # of unique values contained in each #
for i in range(len(col_header)): 
    values = get_col_set(csv_filename,i)
    print(str(col_header[i]) + ":", f"{len(values):,}")

# Find Max Lenght of String fields #
print(col_header[3]) # index of OFFENSE_DESCRIPTION



description = list(get_col_set(csv_filename,0))

max_length = 0
for i in description:
    max_length = max(max_length,len(i))
print(max_length)

# identify longest description #
for i in description:
    if len(i) == max_length:
        print(i)

# First create an enumerated datatype for Day of Week (since only 7 should exist)
cursor.execute("""
               CREATE TYPE enum_days AS ENUM 
               ('Wednesday', 'Sunday', 'Monday', 'Saturday', 'Friday', 'Tuesday', 'Thursday')
               ;
               """)
# CREATE TABLE #
cursor.execute("""CREATE TABLE crimes.boston_crimes(
                 INCIDENT_NUMBER varchar(13) PRIMARY KEY
               , OFFENSE_CODE varchar(9)
               , OFFENSE_DESCRIPTION varchar(58)
               , DAY_OF_WEEK enum_days
               , Lat varchar(11)
               , Long varchar(12)
)
               ;""")

# LOAD DATA #
with open("boston.csv") as f:
    cursor.copy_expert("COPY crimes.boston_crimes FROM STDIN WITH CSV HEADER;", f)

# ESTABLISH PRIVILEGES #

# First check privileges #
cursor.execute("""
                SELECT DISTINCT grantor, grantee, privilege_type
                FROM information_schema.table_privileges;
               """)
cursor.fetchall()

cursor.execute("""
            REVOKE ALL ON SCHEMA public FROM public;
               """)

cursor.execute("""
            REVOKE ALL ON DATABASE crime_db FROM public;
               """)

# Create GROUPS - read and readwrite #
cursor.execute("""
            CREATE GROUP readonly NOLOGIN;
               """)
cursor.execute("""
            CREATE GROUP readwrite NOLOGIN;
               """)

# Grant Connect & Usage for both groups #
cursor.execute("""
            GRANT CONNECT ON DATABASE crime_db TO readonly;
               """)
cursor.execute("""
           GRANT USAGE ON SCHEMA crimes TO readonly;
               """)

cursor.execute("""
            GRANT CONNECT ON DATABASE crime_db TO readwrite;
               """)
cursor.execute("""
           GRANT USAGE ON SCHEMA crimes TO readwrite;
               """)

# Grant Select Privilege to READ group & SELECT, INSERT, DELETE, UPDATE to READWRITE #

# READONLY #
cursor.execute("""
               GRANT SELECT ON ALL TABLES IN SCHEMA crimes TO readonly;
                """)
# READWRITE #
cursor.execute("""
               GRANT SELECT, INSERT, DELETE, UPDATE ON ALL TABLES IN SCHEMA crimes
               TO readwrite;
                """)

# Populate Users #
# Data Analyst -> readonly #
cursor.execute("""
               CREATE USER data_analyst WITH PASSWORD 'secret1';
               GRANT readonly TO data_analyst;""")
# Data Scientist -> readwrite #
cursor.execute("""
               CREATE USER data_scientist WITH PASSWORD 'secret2';
               GRANT readwrite TO data_scientist;""")

# Check #
cursor.execute("""
SELECT grantee, privilege_type
    FROM information_schema.table_privileges
    WHERE grantee = 'readwrite';""")
cursor.fetchall()
cursor.execute("""               
SELECT grantee, privilege_type
    FROM information_schema.table_privileges
    WHERE grantee = 'readonly';
               """)
cursor.fetchall()
