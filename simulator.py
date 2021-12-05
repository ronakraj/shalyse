###############################################################
# Stock Price Data Modeller
# By Ronakraj Gosalia
###############################################################

import csv
import statistics

# Key files
data_file = open("asx.csv")

# Read data file and construct a dictionary of values
data_reader = csv.reader(data_file)
data_dict = {}
headers = []
heading = True
for row in data_reader:
    if heading:
        for item in row:
            data_dict[item] = []
            headers.append(item)
        heading = False
    else:
        for index, item in enumerate(row):
            data_dict[headers[index]].append(item)

# Test simulation
scenario = {
    'initial': 10000,       # Initial invested amount, $ AUD
    'topup': 0,             # Regular contributions, $ AUD
    'freq': 0,              # Frequency of contribution, months
    'period': 5             # Total investment horizon, years
}

growth = []
for i in range(0, len(data_dict[headers[0]])):
    next_period = scenario['period'] * 365 + i

    if next_period < len(data_dict[headers[0]]):
        # 0: Date, 1: Open, 2: High, 3: Low, 4: Close, 5: Adj Close 
        # and 6: Volume
        growth.append((float(data_dict[headers[5]][next_period]) - \
            float(data_dict[headers[5]][i])) / float(data_dict[headers[5]][i]))
    else:
        break

print("*************************************************")
print("SCENARIO")
print("Initial: \t $" + str(scenario['initial']))
print("Top-up: \t $" + str(scenario['topup']))
print("Frequency: \t " + str(scenario['freq']) + " per month")
print("Horizon: \t" + str(scenario['period']) + " years")
print("*************************************************")
print("RESULT")

result = {
    'min': {'perc': round(min(growth) * 100, 2), 
            'amount': round((min(growth) + 1) * scenario['initial'], 2)
            },
    'median': {'perc': round(statistics.median(growth) * 100, 2),
               'amount': round((statistics.median(growth) + 1) * \
                   scenario['initial'], 2)
              },
    'mean': {'perc': round(statistics.mean(growth) * 100, 2),
               'amount': round((statistics.mean(growth) + 1) * \
                   scenario['initial'], 2)
              },
    'max': {'perc': round(max(growth) * 100, 2), 
            'amount': round((max(growth) + 1) * scenario['initial'], 2)
            }
}

print("Min: \t" + str(result['min']['perc']) + " %" + \
    " \t $" + str(round(result['min']['amount'] - scenario['initial'], 2)))
print("Med: \t" + str(result['median']['perc']) + " %" + \
    " \t $" + str(round(result['median']['amount'] - scenario['initial'], 2)))
print("Mean: \t" + str(result['mean']['perc']) + " %" + \
    " \t $" + str(round(result['mean']['amount'] - scenario['initial'], 2)))
print("Max: \t" + str(result['max']['perc']) + " %" + \
    " \t $" + str(round(result['max']['amount'] - scenario['initial'], 2)))
print("*************************************************")