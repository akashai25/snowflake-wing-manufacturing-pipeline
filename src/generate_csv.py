#generate synthetic wing data for testing
import csv
import random

   
data = []
for _ in range(100):

    TORQUE_VALUE = round(random.uniform(38, 72.0), 2)
    QC_STATUS= (
        'FAIL'
        if (TORQUE_VALUE< 42.5 or TORQUE_VALUE> 68.0)
        else
                 random.choice(['PASS', 'PASS', 'PASS', 'REWORK'])  # example distribution favors PASS; FAIL is assigned separately for out-of-range torque 
    )
    row = {
            'PLAN_ID': f'PLAN-{random.randint(1000, 1999)}', #Wrapping it in an f-string (f'PLAN-{...}')
            'PART_NUM': random.choice(['SPAR-A1', 'RIB-B2', 'SKIN-C3', 'STRINGER-D4']),
            'OP_SEQ': random.choice([10, 20, 30, 40]),
            'TORQUE_VALUE': TORQUE_VALUE,
            'QC_STATUS': QC_STATUS   
}
    data.append(row)



with open('wing_data_sample.csv', 'w', newline='') as csvfile:
    fieldnames = ['PLAN_ID', 'PART_NUM', 'OP_SEQ', 'TORQUE_VALUE', 'QC_STATUS']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)


    print("Synthetic wing data generated successfully!")