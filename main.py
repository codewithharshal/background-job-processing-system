from workers.tasks.csv_import import add_twoNum

for i in range(20):
    result = add_twoNum.delay(i,i+1)

print(result)