# PORTFOLIO NOTE: PUT and COPY are intentionally commented out in this preserved development script.
#Connecting local machine to Snowflake using the Snowflake Connector for Python

import os
from dotenv import load_dotenv
import snowflake.connector

# 1. Open the lockbox
load_dotenv('.env')

# 2. Gather the credentials from the lockbox
USER = os.getenv('SNOWFLAKE_USER')
PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')

print("Dialing Snowflake...")

# 3. Dial the phone (Connect to the database)
conn = snowflake.connector.connect(
    user=USER,
    password=PASSWORD,
    account=ACCOUNT,           # Snowflake account locator; does not set schema
)


# 4. Ask the question using the cursor
#file_name = "wing_data_sample.csv"
#stage_name = "wing_data_stage"

COPY_INTO_query= """ COPY INTO RAW_WING
FROM @wing_data_stage
files=('wing_data_sample.csv')
FILE_FORMAT= (format_name = 'wing_data_file_format')
ON_ERROR = 'ABORT_STATEMENT'
FORCE = TRUE  
"""

staged_file_query = """ SELECT COUNT(*)
FROM @wing_data_stage/wing_data_sample.csv (FILE_FORMAT => 'wing_data_file_format')
"""

cs = conn.cursor()
try:
  cs.execute("USE DATABASE WING_DATA_PROJECT")
  cs.execute("USE SCHEMA PUBLIC")
  cs.execute("USE ROLE SYSADMIN")  

  #cs.execute(f"PUT file://{file_name} @{stage_name} OVERWRITE = TRUE auto_compress=false")  # Upload csv to the stage 

  #cs.execute(COPY_INTO_query) # Run the COPY INTO command
  #print('Data successfully loaded into RAW_WING!')


  with open('wing_data_sample.csv', 'r') as f:
    csv_file_count = sum(1 for line in f)-1 # Subtract 1 for the header row
    print(f'Number of rows in the CSV file in local machine: {csv_file_count}')

  cs.execute(staged_file_query) # Check the number of records in the staged file
  staged_file_rows=cs.fetchall()[0][0]
  print(f'Number of rows in the staged file in Snowflake: {staged_file_rows}')

  cs.execute("SELECT COUNT(*) FROM RAW_WING")  # Check the number of records in the table
  print(f"Number of rows loaded into RAW_WING table: {cs.fetchall()[0][0]}") 

except Exception as e:
  print(f"Error occurred: {e}")
finally:
  cs.close()
  conn.close()  # Clean up the main connection as well