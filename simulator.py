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
    'topup': 1000,             # Regular contributions, $ AUD
    'period': 28,            # Time between contributions, days
    'horizon': 4            # Total investment horizon, years
}

# Total contributed over investment horizon is summation of principal
# and regular contributions.
total_contrib = scenario['initial']
if scenario['period'] > 0:
    total_contrib = total_contrib + scenario['topup'] * \
    (scenario['horizon'] * 365 / scenario['period'])

# Simulation over all historical data
total_profit = []
for i in range(0, len(data_dict[headers[0]])):
    next_period = scenario['horizon'] * 365 + i

    if next_period < len(data_dict[headers[0]]):
        # 0: Date, 1: Open, 2: High, 3: Low, 4: Close, 5: Adj Close 
        # and 6: Volume
        final_price = float(data_dict[headers[5]][next_period])

        # Calculate profit on regular contributions
        topup_profit = 0
        if scenario['period'] > 0:
            for j in range(i + scenario['period'], next_period, \
                    scenario['period']):
                # Current share price at simulated starting point
                current_price = float(data_dict[headers[5]][j])

                # Calculate total profits made by regular topups over simulated
                # interval.
                topup_profit = topup_profit + \
                    ((final_price - current_price) / current_price) * \
                       scenario['topup']
        
        # Calculate profit on principal
        current_price = float(data_dict[headers[5]][i])
        princ_profit = ((final_price - current_price) / current_price) * \
            scenario['initial']

        # Save profit over principal and topups in this scenario
        total_profit.append(princ_profit + topup_profit)

    else:
        break

print("*************************************************")
print("\t SCENARIO")
print("Initial: \t $" + str(scenario['initial']))
print("Top-up: \t $" + str(scenario['topup']))
print("Period: \t " + str(scenario['period']) + " days between top-ups")
print("Horizon: \t " + str(scenario['horizon']) + " years")
print("Contributions: \t $" + str(total_contrib))
print("*************************************************")
print("\t RESULTS")

result = {
    'min': {'perc': round((min(total_profit)) / total_contrib \
                            * 100, 2), 
            'amount': round(min(total_profit), 2)
            },
    'median': {'perc': round((statistics.median(total_profit)) / \
        total_contrib * 100, 2),
               'amount': round(statistics.median(total_profit), 2)
              },
    '-1std': {'perc': round((statistics.mean(total_profit) - \
        (statistics.stdev(total_profit) / 2)) / total_contrib * 100, 2),
              'amount': round(statistics.mean(total_profit) - \
        (statistics.stdev(total_profit) / 2), 2)
             },
    'mean': {'perc': round((statistics.mean(total_profit)) / \
        total_contrib * 100, 2),
               'amount': round(statistics.mean(total_profit), 2)
              },
    '+1std': {'perc': round((statistics.mean(total_profit) + \
        (statistics.stdev(total_profit) / 2)) / total_contrib * 100, 2),
              'amount': round(statistics.mean(total_profit) + \
        (statistics.stdev(total_profit) / 2), 2)
             },
    'max': {'perc': round((max(total_profit)) / total_contrib \
                            * 100, 2), 
            'amount': round(max(total_profit), 2)
            }
}
print(" \tProfit (%) \t Profit ($) \t Total ($)")
print("Min: \t" + str(result['min']['perc']) + " %" + \
    " \t $" + str(round(result['min']['amount'], 2)) + \
    " \t $" + str(round(result['min']['amount'] + total_contrib, 2)))
print("-1std: \t" + str(result['-1std']['perc']) + " %" + \
    " \t $" + str(round(result['-1std']['amount'], 2)) + \
    " \t $" + str(round(result['-1std']['amount'] + total_contrib, 2)))
print("Med: \t" + str(result['median']['perc']) + " %" + \
    " \t $" + str(round(result['median']['amount'], 2)) + \
    " \t $" + str(round(result['median']['amount'] + total_contrib, 2)))
print("Mean: \t" + str(result['mean']['perc']) + " %" + \
    " \t $" + str(round(result['mean']['amount'], 2)) + \
    " \t $" + str(round(result['mean']['amount'] + total_contrib, 2)))
print("+1std: \t" + str(result['+1std']['perc']) + " %" + \
    " \t $" + str(round(result['+1std']['amount'], 2)) + \
    " \t $" + str(round(result['+1std']['amount'] + total_contrib, 2)))
print("Max: \t" + str(result['max']['perc']) + " %" + \
    " \t $" + str(round(result['max']['amount'], 2)) + \
    " \t $" + str(round(result['max']['amount'] + total_contrib, 2)))
print("*************************************************")