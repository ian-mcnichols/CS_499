from Data import Data
from Analyzer import Analyzer


def main():
    available_functions = {"Frequency": [], # We need more info on the statistical functions.
                           "Ordinal": [], 
                           "Interval": []}
    available_graphs = {"mean": [],
                        "median": [],
                        "mode": [],
                        "stand_dev": [],
                        "variance": [],
                        "percentiles": ['vertical bar'],
                        "prob_dist": ['XY chart'],
                        "binomial_dist": [],
                        "chi_squared": [],
                        "least_square_line": [],
                        "corr_coeff": [],
                        "rank_sum": [],
                        "spearman_rank": []}
    while True:
        enter_file = input("Would you like to add data by file? y/n:  ")
        if enter_file.lower() == "y":
            data_file = input("Enter data file:  ")
            data_type = input("Enter data type:  ")
            my_functions = available_functions[data_type]
            my_data = Data(filepath=data_file, data_type=data_type)
            my_analyzer = Analyzer(data_type)
        function_to_run = input("Enter the function to run on this data: ")
    
    return

if __name__ == "__main__":
    main()
