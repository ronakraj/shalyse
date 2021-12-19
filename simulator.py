###############################################################
# Stock Price Data Modeller
# By Ronakraj Gosalia
###############################################################

import statistics
from retriever import Retriever
from typing import List

# Test simulation
ticker = "^AXJO"
scenario = {
    'initial': 10000,       # Initial invested amount, $ AUD
    'topup': 1000,          # Regular contributions, $ AUD
    'period': 30,           # Time between contributions, days
    'horizon': 4            # Total investment horizon, years
}

class Shalyse:
    def __init__(self, ticker=ticker, scenario=scenario) -> None:
        """
        Main Share Analysis class where total contributions,
        and statistical analysis of expected return is calculated.
        """
        
        self.ticker = ticker
        self.scenario = scenario
        self.retriever = Retriever(self.ticker)
        self.data = self.retriever.data
        self.info = self.retriever.info
        self.total_contrib = self._get_tot_contr(self.scenario)
        self.total_profit = self._get_tot_prof(self.scenario, self.data)
        self.stats = self._analyse_profit(self.total_profit, self.total_contrib)
        
    def _get_tot_contr(self, scenario: dict) -> int:
        """
        Calculate the total contributations made by investor over 
        investment horizon. This sums the initial investments with
        regular contributions.
        """

        # Total contributed over investment horizon is summation of principal
        # and regular contributions.
        total_contrib = scenario['initial']
        if scenario['period'] > 0:
            total_contrib = total_contrib + scenario['topup'] * \
            (scenario['horizon'] * 365 / scenario['period'])
        
        return total_contrib

    def _get_tot_prof(self, scenario: dict, data: dict) -> List[float]:
        """
        Simulate over all possible entry and exit points the investment
        strategy. The output is an array of expected total profit that 
        can be statistically analysed.
        """

        # Simulation over all historical data
        total_profit = []
        for i in range(0, len(data["Date"])):
            next_period = scenario['horizon'] * 365 + i

            if next_period < len(data["Date"]):
                # 0: Date, 1: Open, 2: High, 3: Low, 4: Close, 5: Adj Close 
                # and 6: Volume
                final_price = float(data["Adj Close"][next_period])

                # Calculate profit on regular contributions
                topup_profit = 0
                if scenario['period'] > 0:
                    for j in range(i + scenario['period'], next_period, \
                            scenario['period']):
                        # Current share price at simulated starting point
                        current_price = float(data["Adj Close"][j])

                        # Calculate total profits made by regular topups over 
                        # simulated interval.
                        topup_profit = topup_profit + \
                            ((final_price - current_price) / current_price) * \
                            scenario['topup']
                
                # Calculate profit on principal
                current_price = float(data["Adj Close"][i])
                princ_profit = ((final_price - current_price) / \
                    current_price) * scenario['initial']

                # Save profit over principal and topups in this scenario
                total_profit.append(princ_profit + topup_profit)

            else:
                break
        
        return total_profit

    def _analyse_profit(self, total_profit: List[float], \
            total_contrib: float) -> dict:
        """
        Analyse the array of profits for all simulated scenarios
        and output statistical information about the distribution.
        """
        # Create empty dictionary fields
        stats = {
            'min': {},
            'median': {},
            '-1std': {},
            'mean': {},
            '+1std': {},
            'max': {}
        }
        
        # Each field has a percentage and absolute value
        for key in stats:
            stats[key] = {'perc': 0, 'abs': 0}
        
        # Evaluate all statistical data to 2 decimal places
        stats['min']['perc'] = round((min(total_profit)) / total_contrib \
                                * 100, 1)
        stats['min']['abs'] = round(min(total_profit), 0)

        stats['median']['perc'] = round((statistics.median(total_profit)) / \
            total_contrib * 100, 1)
        stats['median']['abs'] = round(statistics.median(total_profit), 0)

        stats['-1std']['perc'] = round((statistics.mean(total_profit) - \
            (statistics.stdev(total_profit) / 2)) / total_contrib * 100, 1)
        stats['-1std']['abs'] = round(statistics.mean(total_profit) - \
            (statistics.stdev(total_profit) / 2), 0)

        stats['mean']['perc'] = round((statistics.mean(total_profit)) / \
            total_contrib * 100, 1)
        stats['mean']['abs'] = round(statistics.mean(total_profit), 0)

        stats['+1std']['perc'] = round((statistics.mean(total_profit) + \
            (statistics.stdev(total_profit) / 2)) / total_contrib * 100, 1)
        stats['+1std']['abs'] = round(statistics.mean(total_profit) + \
            (statistics.stdev(total_profit) / 2), 0)

        stats['max']['perc'] = round((max(total_profit)) / total_contrib \
                                * 100, 1)
        stats['max']['abs'] = round(max(total_profit), 0)

        # Display string for each statistic
        for stat in stats:
            stats[stat]['display'] = "{0} {2} ({1:+} {2}) ({3:+} %)".format(
            round(self.total_contrib + stats[stat]['abs'], 0),
            stats[stat]['abs'], self.info['currency'], 
            stats[stat]['perc'])

        return stats
