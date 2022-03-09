import matplotlib.pyplot as plt
import numpy as np
import csv


def build_csv(output_file_name, data):
    if output_file_name.endswith('.csv') is False:
        output_file_name += ".csv"
    with open(output_file_name, 'w', newline='') as csv_file:
        write = csv.DictWriter(csv_file, fieldnames=['Function', 'Value'])
        write.writeheader()
        for function in data:
            write.writerow({'Function': function, 'Value': data[function]})


def build_text(output_file_name, data):
    if output_file_name.endswith('.txt') is False:
        output_file_name += ".txt"
    #  Build text


def save_jpeg(self, output_file_name):  # Static function, outputs one graph at a time. Reliant on plt state
    if output_file_name.endswith('.jpeg') is False:
        output_file_name += ".jpeg"
    plt.savefig(output_file_name)


def plot_chart(data, plot_type, results=None, data_type=None):
    if plot_type == "Vertical Bar Chart":
        fig, ax = plt.subplots(figsize=(15, 8))
        y_labels = []
        y_ticks = []
        for i in range(1, len(data.dtype.names)):
            y_ticks.append(i)
            y_labels.append(data.dtype.names[i] + " - " + str(i))
        row_labels = []
        for j in range(len(data)):
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
        plt.show()
    elif plot_type == "box plot":
        print("plotting box plot")
        # Set up labels for x-axis
        labels = []
        columns = []
        for i in range(1, len(data.data_np.dtype.names)):
            labels.append(data.data_np.dtype.names[i])
            columns.append(data.data_np[data.data_np.dtype.names[i]])
        # Set up plot and display
        fig, ax = plt.subplots()
        ax.boxplot(columns)
        # Get current number of labels
        num_labels, curr_labels = plt.xticks()
        # Set labels to column names
        plt.xticks(num_labels, labels)
        plt.title("Box and Whisker Plot for " + data.data_type + " Data")
        plt.savefig('Box_and_Whisker.jpg')
        plt.show()
    elif plot_type == "Histogram":
        print("Plotting Histogram")
        if data_type == "interval":
            # for each column, create a histogram
            for i in range(1, len(data.data_np.dtype.names)):
                plt.hist(data.data_np[data.data_np.dtype.names[i]], bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                         edgecolor='black')
                plt.xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
                plt.xlabel("Scores")
                plt.ylabel("Number of Results")
                plt.title(data.data_np.dtype.names[i] + " Scores Histogram")
                plt.savefig(data.data_np.dtype.names[i] + ' Histogram.jpg')
                plt.show()
    # elif plot_type == "Stacked Box":
    else:
        raise Exception("Invalid chart type {}".format(plot_type))
