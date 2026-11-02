import csv


# Generating the dirty payload
data = [
    # A standard, clean record
    {'PLAN_ID': 'PLAN-2010', 'PART_NUM': 'RIB-B2', 'OP_SEQ': 30, 'TORQUE_VALUE': 55.1, 'QC_STATUS': 'PASS'},
    
    # The Bad Data Injection: A string ('ERR') inside a numerical column
    {'PLAN_ID': 'PLAN-2020', 'PART_NUM': 'RIB-B3', 'OP_SEQ': 40, 'TORQUE_VALUE': 'ERR', 'QC_STATUS': 'FAIL'},
    
    # Another clean record
    {'PLAN_ID': 'PLAN-2030', 'PART_NUM': 'SKIN-C3', 'OP_SEQ': 20, 'TORQUE_VALUE': 50.0, 'QC_STATUS': 'PASS'}
]

file_path = 'wing_data_corrupted.csv'

with open(file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

print(f"Corrupted file '{file_path}' generated successfully.")


