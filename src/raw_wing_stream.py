# PORTFOLIO SAFETY PATCH: avoid replacing an existing stream and resetting state; NOT retested.
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


cs = conn.cursor()
try:
    cs.execute("USE DATABASE WING_DATA_PROJECT")
    cs.execute("USE SCHEMA PUBLIC")
    cs.execute("USE ROLE SYSADMIN")  

    cs.execute("CREATE STREAM IF NOT EXISTS wing_stream ON TABLE RAW_WING")
    print("Stream 'wing_stream' created successfully on table 'RAW_WING'")
    cs.execute("SELECT * FROM wing_stream")
    print(f"First row from wing_stream: {cs.fetchall()}")  

except Exception as e:
  print(f"Error occurred: {e}")
finally:
  cs.close()
  conn.close()  # Clean up the main connection as well