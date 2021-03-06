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
                    elif function == "Spearman rank correlation coefficient":
                        row = ["Spearman coefficient"]
                        row.append(results[function][0])
                        write.writerow(row)

                        row = ["Spearman p-value"]
                        row.append(results[function][0])
                        write.writerow(row)
                    elif function == "Least square line":
                        row = ["LSRL slope:"]
                        row.append(results[function][0])
                        write.writerow(row)

                        row = ["LSRL y-intercept"]
                        row.append(results[function][0])
                        write.writerow(row)
                    elif function == "Percentiles":
                        for percentile_list in results[function]:
                            if type(percentile_list[0]) is list:  # List of lists of percentiles
                                for i in range(len(percentile_list)):
                                    row = [function + " " + headers[i]]
                                    row.append(percentile_list[i])
                                    write.writerow(row)
                            else:  # Difference list
                                row = [function + " Difference between first and last column"]
                                row.append(results[function][-1])
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
            elif function == "Spearman rank correlation coefficient":
                results_summary += f"\tSpearman coefficient: {results[function][0]}\n"
                results_summary += f"\tp-value: {results[function][1]}\n\n"
                continue
            elif function == "Least square line":
                results_summary += f"\ty = {results[function][0]}x + ({results[function][1]})\n\n"
                continue
            elif function == "Percentiles":
                for percentile_list in results[function]:
                    if type(percentile_list[0]) is list:  # List of lists of percentiles
                        for i in range(len(percentile_list)):
                            results_summary += f"\t{headers[i]}: {percentile_list[i]}\n"
                    else:  # Difference list
                        results_summary += f"\tDifference between first and last column: {percentile_list}\n"
                results_summary += "\n"
                continue
            if type(results[function]) is list:
                for i in range(len(results[function])):
                    if results[function][i] != results[function][-1]:
                        results_summary += "\t" + headers[i] + ": "
                        results_summary += str(results[function][i]) + "\n"
                    else:
                        results_summary += "\tDifference between first and last column: "
                        results_summary += "{}\n\n".format(results[function][i])
            else:
                results_summary += "\t" + str(results[function]) + "\n\n"
    # Data is ordinal
    else:
        # For each function run, add summary of results from that function
        for function in results:
            results_summary += "Results from {}:\n".format(function)
            if function == "Probability distribution":
                results_summary += "\tSee probability distribution graphs in output folder\n\n"
                continue
            if type(results[function]) is list:
                for i in range(len(results[function])):
                    results_summary += "\t # {}: {}\n".format(i+1, results[function][i])
            results_summary += "\n\n"
    return results_summary


def plot_chart(data, plot_type, results=None, data_type=None, save=True,
               display=True):
    if plot_type == "Vertical Bar Chart":
        # Set up size
        fig, ax = plt.subplots(figsize=(10, 5), num="Ordinal Mode Plot")
        # Set y-labels from column labels
        y_labels = []
        y_ticks = []
        for i in range(len(data.column_labels)):
            y_ticks.append(i+1)
            y_labels.append(data.column_labels[i])
        # Set x-labels from row labels
        row_labels = []
        for j in range(len(data.row_labels)):
            row_labels.append(j+1)
        # Plot results
        plt.bar(row_labels, results)
        # Set up labels and title
        plt.xlabel('Row')
        plt.title("Most Common Result for Each Row")
        plt.xticks(range(min(row_labels), max(row_labels)+1, 1), rotation=45)
        plt.yticks(y_ticks)
        ax.set_yticklabels(y_labels)
        plt.margins(x=0.005)
        plt.tight_layout()
        if save:
            plt.savefig('output/Ordinal_Chart.jpg')
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
        fig, ax = plt.subplots(num="Box and Whisker Plot")
        ax.boxplot(column_data)
        # Get current number of labels
        num_labels, curr_labels = plt.xticks()
        # Set labels to column names
        plt.xticks(num_labels, labels)
        plt.title("Box and Whisker Plot for {} Data".format(data.data_type))
        if save:
            plt.savefig('output/Box_and_Whisker.jpg')
        if display:
            plt.show()
    elif plot_type == "Histogram":
        # For each column, create a histogram
        for i in range(len(data.column_labels)):
            plt.figure("{} Histogram".format(data.column_labels[i]))
            plt.hist(data.data_np[i], bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                     edgecolor='black')
            plt.xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
            plt.title(data.column_labels[i] + " Histogram")
            if save:
                plt.savefig("output/ {} Histogram.jpg".format(data.column_labels[i]))
            if display:
                plt.show()
    elif plot_type == "Probability Distribution":
        if data_type.lower() == "interval":
            if do_logging:
                logging.info("Plotting probability distribution")
            for idx, column in enumerate(data.data_np):
                plt.figure("Column {} Probability Distribution".format(idx+1))
                temp = np.ndarray.tolist(column)
                temp.sort()
                plt.hist(temp, weights=np.ones(len(temp)) / len(temp), edgecolor='black')
                plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
                plt.title("Column {} Probability Distribution".format(idx+1))
                if save:
                    plt.savefig("output/Col_{}_distribution.jpg".format(idx+1))
                if display:
                    plt.show()
        elif data_type.lower() == "ordinal":
            if do_logging:
                logging.info("Plotting probability distribution")
            columns, rows = data.data_np.shape
            if do_logging:
                logging.info(f"num rows: {rows}")
            for i in range(rows):
                fig = plt.figure()
                # Get row as list
                row = list(data.data_np[:, i])
                row_values = []
                # Add number of responses for each index number to list
                for j in range(len(row)):
                    num_responses = row[j]
                    for x in range(int(num_responses)):
                        row_values.append(j+1)
                plt.hist(row_values, weights=np.ones(len(row_values)) / len(row_values), edgecolor='black')
                plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
                plt.title("Row {} Probability Distribution".format(i+1))
                if save:
                    fig.savefig("output/Row_{}_distribution.jpg".format(i+1))
                # Close plot to save memory
                plt.close(fig)
    else:
        raise Exception("Invalid chart type {}".format(plot_type))
