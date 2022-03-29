import matplotlib.pyplot as plt
import numpy as np
import csv


def build_csv(output_file_name, results, headers, data_type):
    multi_funcs = ["Mean", "Median", "Mode", "Standard deviation", "Variance"]
    if output_file_name.endswith('.csv') is False:
        output_file_name += ".csv"
    with open(output_file_name, 'w', newline='') as csv_file:
        write = csv.writer(csv_file)
        write.writerow(['Function', 'Value'])
        if data_type == "Interval":
            for function in results:
                row = [function]
                if type(results[function]) is list:
                    if function in multi_funcs:
                        for i in range(len(results[function])):
                            if results[function][i] != results[function][-1]:
                                row = [function + " " + headers[i+1]]
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



def build_text(output_file_name, results, headers, data_type):
    if output_file_name.endswith('.txt') is False:
        output_file_name += ".txt"
    with open(output_file_name, 'w', newline='') as csv_file:
        write = csv.writer(csv_file)
        write.writerow(['Function', 'Value'])
        if data_type == "Interval":
            for function in results:
                row = [function]
                if type(results[function]) is list:
                    for i in range(len(results[function])):
                        if results[function][i] != results[function][-1]:
                            row = [function + " " + headers[i + 1]]
                        else:
                            row = [function + " Difference between first and last column"]
                        row.append(results[function][i])
                        write.writerow(row)

                else:
                    row.append(results[function])
                    write.writerow(row)
        else:
            for function in results:
                if type(results[function]) is list:
                    for i in range(len(results[function])):
                        row = [function + " #" + str(i+1), results[function][i]]
                        write.writerow(row)
        csv_file.close()


def save_jpeg(self, output_file_name):  # Static function, outputs one graph at a time. Reliant on plt state
    if output_file_name.endswith('.jpeg') is False:
        output_file_name += ".jpeg"
    plt.savefig(output_file_name)


def plot_chart(data, plot_type, results=None, data_type=None, save=True,
               display=True):
    if plot_type == "Vertical Bar Chart":
        fig, ax = plt.subplots(figsize=(15, 8))
        y_labels = []
        y_ticks = []
        for i in range(1, len(data.column_labels)):
            y_ticks.append(i)
            y_labels.append(data.column_labels[i] + " - " + str(i))
        row_labels = []
        for j in range(len(data.row_labels)):
            row_labels.append(j+1)
        plt.bar(row_labels, results)
        plt.xlabel('Question Number')
        plt.ylabel('Response Value')
        plt.title("Most Common Response for Each Question")
        plt.xticks(range(min(row_labels), max(row_labels)+1, 1), rotation=45)
        plt.yticks(y_ticks)
        ax.set_yticklabels(y_labels)
        plt.margins(x=0.005)
        plt.tight_layout()
        if save:
            plt.savefig('Ordinal_Chart.jpg')
        if display:
            plt.show()
    elif plot_type == "box plot":
        print("plotting box plot")
        # Set up labels for x-axis
        labels = []
        column_data = []
        for i in range(1, len(data.column_labels)):
            labels.append(data.column_labels[i])
            column_data.append(data.data_np[i-1])
        # Set up plot and display
        fig, ax = plt.subplots()
        ax.boxplot(column_data)
        # Get current number of labels
        num_labels, curr_labels = plt.xticks()
        # Set labels to column names
        plt.xticks(num_labels, labels)
        plt.title("Box and Whisker Plot for " + data.data_type + " Data")
        if save:
            plt.savefig('Box_and_Whisker.jpg')
        if display:
            plt.show()
    elif plot_type == "Histogram":
        print("Plotting Histogram")
        # for each column, create a histogram
        for i in range(1, len(data.column_labels)):
            plt.hist(data.data_np[i-1], bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                     edgecolor='black')
            plt.xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
            plt.xlabel("Scores")
            plt.ylabel("Number of Results")
            plt.title(data.column_labels[i] + " Scores Histogram")
            if save:
                plt.savefig(data.column_labels[i] + ' Histogram.jpg')
            if display:
                plt.show()
    else:
        raise Exception("Invalid chart type {}".format(plot_type))
