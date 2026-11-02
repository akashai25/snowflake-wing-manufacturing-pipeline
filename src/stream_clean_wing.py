
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
    account=ACCOUNT,           # Explicitly sets the active schema
)

query= """CREATE OR REPLACE TABLE CLEAN_WING (
        PLAN_ID VARCHAR,
        PART_NUM VARCHAR,
        OP_SEQ INT,
        TORQUE_VALUE FLOAT,
        QC_STATUS VARCHAR
        );"""

insert_query= """ INSERT INTO CLEAN_WING
                  SELECT PLAN_ID, PART_NUM, OP_SEQ, TORQUE_VALUE, QC_STATUS 
                  FROM wing_stream
                  WHERE METADATA$ACTION = 'INSERT' """

cs = conn.cursor()
try:
  cs.execute("USE DATABASE WING_DATA_PROJECT")
  cs.execute("USE SCHEMA PUBLIC")
  cs.execute("USE ROLE SYSADMIN")  

  #cs.execute(query)
  #print('CLEAN_WING table created successfully!')

  #cs.execute(insert_query)
  #print("Data inserted successfully into CLEAN_WING table from wing_stream.")
  cs.execute('SELECT * FROM CLEAN_WING')
  print('The rows in Clean Wing Table are:')
  for row in cs.fetchall():
    print(row)


  
except Exception as e:
  print(f"Error occurred: {e}")
finally:
  cs.close()
  conn.close()  # Clean up the main connection as well








