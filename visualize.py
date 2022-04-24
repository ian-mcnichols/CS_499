import matplotlib.pyplot as plt
import csv
from matplotlib.ticker import PercentFormatter
import numpy as np
import logging
do_logging = True


def build_csv(results, headers, data_type):
    # Specify which functions have multiple values
    multi_funcs = ["Mean", "Median", "Mode", "Standard deviation", "Variance"]
    output_file_name = "Results.csv"
    # Write each function's results to a .csv file
    with open("output/" + output_file_name, 'w', newline='') as csv_file:
        write = csv.writer(csv_file)
        write.writerow(['Function', 'Value'])
        if data_type == "Interval":
            for function in results:
                row = [function]
                if type(results[function]) is list:
                    if function in multi_funcs:
                        for i in range(len(results[function])):
                            if results[function][i] != results[function][-1]:
                                row = [function + " " + headers[i]]
                            else:
                                row = [function + " Difference between first and last column"]
                            row.append(results[function][i])
                            write.writerow(row)
                    else:
                        for result in results[function]:
                            row.append(result)
                        write.writerow(row)
                else:
                    row.append(results[function])
                    write.writerow(row)
        # Data is ordinal
        else:
            for function in results:
                if type(results[function]) is list:
                    for i in range(len(results[function])):
                        row = [function + " #" + str(i+1), results[function][i]]
                        write.writerow(row)
    csv_file.close()


def build_text(results, headers, data_type):
    output_file_name = "Results.txt"
    # Write results summary to text file
    with open("output/" + output_file_name, 'w', newline='') as txt_file:
        txt_file.write(create_results_summary(data_type, results, headers))
    txt_file.close()


def create_results_summary(data_type, results, headers):
    # Reset result summary
    results_summary = ""
    if data_type == "Interval":
        # For each function run, add summary of results from that function
        for function in results:
            results_summary += "Results from " + function + ":\n"
            if function == "Probability distribution":
                results_summary += "\tSee probability distribution graphs\n\n"
                continue
            if type(results[function]) is list:
                for i in range(len(results[function])):
                    if results[function][i] != results[function][-1]:
                        results_summary += "\t" + headers[i] + ": "
                        results_summary += str(results[function][i]) + "\n"
                    else:
                        results_summary += "\tDifference between first and last column: "
                        results_summary += str(results[function][i]) + "\n\n"
            else:
                results_summary += "\t" + str(results[function]) + "\n\n"
    # Data is ordinal
    else:
        # For each function run, add summary of results from that function
        for function in results:
            results_summary += "Results from " + function + ":\n"
            if function == "Probability distribution":
                results_summary += "\tSee probability distribution graphs\n\n"
                continue
            if type(results[function]) is list:
                for i in range(len(results[function])):
                    results_summary += "\t #" + str(i + 1) + ": " + str(results[function][i]) + "\n"
            results_summary += "\n\n"
    return results_summary


def plot_chart(data, plot_type, results=None, data_type=None, save=True,
               display=True):
    if plot_type == "Vertical Bar Chart":
        # Set up size
        fig, ax = plt.subplots(figsize=(15, 8))
        # Set y-labels from column labels
        y_labels = []
        y_ticks = []
        for i in range(len(data.column_labels)):
            y_ticks.append(i)
            y_labels.append(data.column_labels[i] + " - " + str(i))
        # Set x-labels from row labels
        row_labels = []
        for j in range(len(data.row_labels)):
            row_labels.append(j+1)
        # Plot results
        plt.bar(row_labels, results)
        # Set up labels and title
        plt.xlabel('Question Number')
        plt.ylabel('Response Value')
        plt.title("Most Common Response for Each Question")
        plt.xticks(range(min(row_labels), max(row_labels)+1, 1), rotation=45)
        plt.yticks(y_ticks)
        ax.set_yticklabels(y_labels)
        plt.margins(x=0.005)
        plt.tight_layout()
        if save:
            plt.savefig('output/' + 'Ordinal_Chart.jpg')
        if display:
            plt.show()
    elif plot_type == "box plot":
        # Set up labels for x-axis
        labels = []
        column_data = []
        for i in range(len(data.column_labels)):
            labels.append(data.column_labels[i])
            column_data.append(data.data_np[i])
        # Set up plot and display
        fig, ax = plt.subplots()
        ax.boxplot(column_data)
        # Get current number of labels
        num_labels, curr_labels = plt.xticks()
        # Set labels to column names
        plt.xticks(num_labels, labels)
        plt.title("Box and Whisker Plot for " + data.data_type + " Data")
        if save:
            plt.savefig('output/' + 'Box_and_Whisker.jpg')
        if display:
            plt.show()
    elif plot_type == "Histogram":
        # For each column, create a histogram
        for i in range(len(data.column_labels)):
            plt.hist(data.data_np[i], bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                     edgecolor='black')
            plt.xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
            plt.xlabel("Scores")
            plt.ylabel("Number of Results")
            plt.title(data.column_labels[i] + " Histogram")
            if save:
                plt.savefig("output/" + data.column_labels[i] + ' Histogram.jpg')
            if display:
                plt.show()
    elif plot_type == "Probability Distribution":
        if data_type.lower() == "interval":
            if do_logging:
                logging.info("Plotting probability distribution")
            for idx, column in enumerate(data.data_np):
                plt.figure()
                temp = np.ndarray.tolist(column)
                temp.sort()
                plt.hist(temp, weights=np.ones(len(temp)) / len(temp), edgecolor='black')
                plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
                plt.title("Column {} Probability Distribution".format(idx+1))
                if save:
                    plt.savefig("output/Col_{}_distribution".format(idx+1))
                if display:
                    plt.show()
        elif data_type.lower() == "ordinal":
            if do_logging:
                logging.info("Plotting probability distribution")
            columns, rows = data.data_np.shape
            if do_logging:
                logging.info(f"num rows: {rows}")
            for i in range(rows):
                plt.figure()
                # Get row as list
                row = list(data.data_np[:, i])
                row_values = []
                # Add number of responses for each index number to list
                for j in range(len(row)):
                    num_responses = row[j]
                    for x in range(num_responses):
                        row_values.append(j+1)
                plt.hist(row_values, weights=np.ones(len(row_values)) / len(row_values), edgecolor='black')
                plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
                plt.title("Row {} Probability Distribution".format(i+1))
                if save:
                    plt.savefig("output/Row_{}_distribution".format(i+1))
                if display:
                    plt.show()
    else:
        raise Exception("Invalid chart type {}".format(plot_type))