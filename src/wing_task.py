# PORTFOLIO SAFETY PATCH: Task DDL/resume is opt-in; this modified script has NOT been rerun against Snowflake.
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


task_query= """ CREATE OR REPLACE TASK wing_data_task
                WAREHOUSE = 'COMPUTE_WH'
                SCHEDULE = '5 MINUTES' 
                WHEN SYSTEM$STREAM_HAS_DATA('wing_stream')
                
                AS 
                
                INSERT INTO CLEAN_WING
                ( PLAN_ID, PART_NUM, OP_SEQ, TORQUE_VALUE, QC_STATUS )
                SELECT PLAN_ID, PART_NUM, OP_SEQ, TORQUE_VALUE, QC_STATUS
                FROM wing_stream
                WHERE METADATA$ACTION = 'INSERT' 
            """

task_resume_query= """ ALTER TASK wing_data_task RESUME """

cs = conn.cursor()
try:
  cs.execute("USE DATABASE WING_DATA_PROJECT")
  cs.execute("USE SCHEMA PUBLIC")
  cs.execute("USE ROLE SYSADMIN")  # Ensure the role has the necessary privileges to create tasks
  

  if os.getenv("ENABLE_TASK_CHANGES", "false").lower() != "true":
    print("SAFETY: Task creation/resume disabled. Review code and set ENABLE_TASK_CHANGES=true only in a dedicated sandbox.")
    return_task_changes = False
  else:
    return_task_changes = True

  if return_task_changes:
    cs.execute(task_query)
    print('Task definition created; scheduled evaluation occurs every 5 minutes when enabled (not immediate event-triggering).')

    cs.execute('SHOW TASKS')
    print(f' Tasks: {cs.fetchall()}')

    cs.execute(task_resume_query)  # Only when ENABLE_TASK_CHANGES=true
    print('Task resumed. Remember to suspend it after testing to avoid ongoing costs.')

except Exception as e:
  print(f"Error occurred: {e}")
finally:
  cs.close()
  conn.close()  # Clean up the main connection as well