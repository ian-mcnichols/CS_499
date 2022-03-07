import matplotlib.pyplot as plt
import numpy as np
import csv


def build_csv(output_file_name, data):
    if output_file_name.endswith('.csv') is False:
        output_file_name += ".csv"
    with open(output_file_name, 'w', newline='') as csv_file:
        write = csv.DictWriter(csv_file, fieldnames=['Function', 'Value'])
        write.writeheader()
        for function in data.results:
            write.writerow({'Function': function, 'Value': data[function]})


def build_text(output_file_name, data):
    if output_file_name.endswith('.txt') is False:
        output_file_name += ".txt"
    #  Build text


def save_jpeg(self, output_file_name):  # Static function, outputs one graph at a time. Reliant on plt state
    if output_file_name.endswith('.jpeg') is False:
        output_file_name += ".jpeg"
    plt.savefig(output_file_name)


def plot_chart(data, plot_type):
    if plot_type == "vertical bar chart":
        plt.figure()
        plt.bar(data[0], data[1], width=5)
        plt.title("title")
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
        if data.data_type == "Interval":
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
    elif plot_type == "XY chart":
        plt.figure()
        for data_, plot_type in data:
            if plot_type == 'line':
                plt.plot(data_[0], data_[1], 'r')
            elif plot_type == 'dot':
                plt.plot(data_[:, 0], data_[:, 1], 'b.')
        plt.title("title")
        plt.show()
    elif plot_type == "Scatter":
        print("Plotting Scatter Plot")
        # For interval data
        color = ['red', 'blue']
        # x = data.data_np[data.data_np.dtype.names[1]] #pretest
        # y = x
        # plt.plot(data.data_np)
        # x2 = data.data_np[data.data_np.dtype.names[2]] #posttest
        # plt.show()
    else:
        raise Exception("Invalid chart type {}".format(plot_type))
