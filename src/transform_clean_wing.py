# PORTFOLIO SAFETY PATCH: Destructive transformation is disabled by default; NOT retested against Snowflake.
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

query= """CREATE OR REPLACE TABLE CLEAN_WING_T (
        PLAN_ID VARCHAR,
        PART_NUM VARCHAR,
        OP_SEQ INT,
        TORQUE_VALUE FLOAT,
        QC_STATUS VARCHAR
        );"""


transform_query= """ INSERT INTO CLEAN_WING_T
                    SELECT TRIM(UPPER(PLAN_ID)),
                           TRIM(UPPER(PART_NUM)),
                           COALESCE(OP_SEQ, 0),
                           COALESCE(TORQUE_VALUE, 0.0),
                           TRIM(UPPER(QC_STATUS))
                    FROM CLEAN_WING
"""

cs = conn.cursor()
try:
  cs.execute("USE DATABASE WING_DATA_PROJECT")
  cs.execute("USE SCHEMA PUBLIC")
  cs.execute("USE ROLE SYSADMIN")  


  if os.getenv("ENABLE_DESTRUCTIVE_TRANSFORM", "false").lower() == "true":
    # WARNING: query contains CREATE OR REPLACE TABLE and can overwrite existing data.
    cs.execute(query)
    print('CLEAN_WING_T table replaced in the selected schema.')
    cs.execute(transform_query)
    cs.execute('SELECT * FROM CLEAN_WING_T')
    print(f' The data in transformed clean table is: {cs.fetchall()}')
  else:
    print('SAFETY: skipped CREATE OR REPLACE TABLE and INSERT. Review before enabling.')

except Exception as e:
  print(f"Error occurred: {e}")
finally:
  cs.close()
  conn.close()  # Clean up the main connection as well