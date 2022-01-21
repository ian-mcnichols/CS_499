from Data import Data
import Analyzer
import visualize


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
            my_data = Data(data_type=data_type)
            my_data.read_data_file(data_file)

        functions_to_run = input("Enter the functions to run on this data: ").split(", ")
        do_plot = input("Would you like to plot outputs? y/n:  ")
        do_save = input("Would you like to save the plots as png's? y/n:  ")
        for function_to_run in functions_to_run:
            output = Analyzer.run_function(function_to_run, my_data.data) # TODO: Add this logic over in Analyzer
            print("Function output: ", output)
            if do_plot:
                plot_types = available_graphs[function_to_run]
                for plot_type in plot_types:
                    visualize.plot_chart(output, plot_type, "<insert title>")
            continue
    return

if __name__ == "__main__":
    main()
