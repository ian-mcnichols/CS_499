from Data import Data
from Analyzer import Analyzer


def main(filepath, data_type):
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
    my_functions = available_functions[data_type]
    my_data = Data(filepath=filepath, data_type=data_type)
    my_analyzer = Analyzer(data_type)
    print(my_data.data.shape)
    
    return

if __name__ == "__main__":
    main()