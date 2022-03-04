from Data import Data
import Analyzer
import visualize


def main():
    available_functions = {"ordinal": ['mean', 'median', 'mode',
                                       'distribution'],
                           "interval": ['mean', 'median', 'mode',
                                        'stand_dev', 'variance',
                                        'percentiles', 'lsr',
                                        'prob_dist', 'corr_coeff',
                                        'spearman_coeff']}
    while True:
        enter_file = input("Would you like to add data by file? y/n:  ")
        if enter_file.lower() == "y":
            data_file = input("Enter data file:  ")
            data_type = input("Enter data type:  ")
            my_data = Data(file_name=data_file, data_type=data_type)
            # my_data.read_data_file(data_file)
        else:
            break
        if data_type == 'interval':
            print("my data:", my_data.data_np['Pretest'], my_data.data_np['Posttest'])
        else:
            print("my data:", my_data.ordinals)
        functions_to_run = input("Enter the functions to run on this data: ").split(", ")
        for function_to_run in functions_to_run:
            if function_to_run not in available_functions[data_type]:
                print("Unable to perform function {} on data type {}".format(function_to_run, data_type))
                continue
            if data_type == 'interval':
                output = Analyzer.run_function(function_to_run, my_data.data_np['Pretest'], my_data.data_np['Posttest'])
            elif data_type == 'ordinal':
                output = Analyzer.run_function(function_to_run, my_data.ordinals)
            else:
                break
            print("Function output: ", output)
            visualize.plot_chart(my_data, "box plot")
            visualize.plot_chart(my_data, "Histogram")
            continue
    return

if __name__ == "__main__":
    main()
