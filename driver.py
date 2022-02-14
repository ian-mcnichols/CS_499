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
            my_data = Data(file_name=data_file)
            # my_data.read_data_file(data_file)

        functions_to_run = input("Enter the functions to run on this data: ").split(", ")
        do_plot = input("Would you like to plot outputs? y/n:  ")
        do_save = input("Would you like to save the plots as png's? y/n:  ")
        for function_to_run in functions_to_run:
            if function_to_run not in available_functions[data_type]:
                print("Unable to perform function {} on data type {}".format(function_to_run, data_type))
                continue
            output = Analyzer.run_function(function_to_run, my_data.data)
            print("Function output: ", output)
            if do_plot:
                plot_types = available_graphs[function_to_run]
                run_plots = input("Which plot would you like to run out of the available: ", plot_types).split(", ")
                for plot_type in run_plots:
                    visualize.plot_chart(output, plot_type, "<insert title>")
            continue
    return

if __name__ == "__main__":
    main()
