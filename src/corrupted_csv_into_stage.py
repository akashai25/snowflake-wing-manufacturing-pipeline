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


file_path = 'wing_data_corrupted.csv'
stage_name= 'wing_data_stage'


cs = conn.cursor()
try:
    cs.execute("USE DATABASE WING_DATA_PROJECT")
    cs.execute("USE SCHEMA PUBLIC")
    cs.execute("USE ROLE SYSADMIN") 
    
    cs.execute(f"PUT file://{file_path} @{stage_name} OVERWRITE = TRUE auto_compress=false")  # Upload csv to the stage 
    print(f"Corrupted file '{file_path}' uploaded to Snowflake stage '{stage_name}' successfully.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
  cs.close()
  conn.close()  # Clean up the main connection as well