import matplotlib.pyplot as plt
import numpy as np
import csv


def build_csv(self, output_file_name, data):
    if output_file_name.endswith('.csv') is False:
        output_file_name += ".csv"
    with open(output_file_name, 'w', newline='') as csv_file:
        write = csv.DictWriter(csv_file, fieldnames=['Function', 'Value'])
        write.writeheader()
        for function in data.results:
            write.writerow({'Function': function, 'Value': data[function]})


def build_text(self, output_file_name, data):
    if output_file_name.endswith('.txt') is False:
        output_file_name += ".txt"
    #  Build text


def save_jpeg(self, output_file_name):  # Static function, outputs one graph at a time. Reliant on plt state
    if output_file_name.endswith('.jpeg') is False:
        output_file_name += ".jpeg"
    plt.savefig(output_file_name)


def plot_chart(data, plot_type, title):
    if plot_type == "horizontal bar chart":
        print("plotting horizontal bar chart")
        # TO-DO add code for horizontal bar chart
        # Used for all types of data
        # For each label
    elif plot_type == "vertical bar chart":
        # Used for all types of data
        plt.figure()
        plt.bar(data[0], data[1], width=5)
        plt.title(title)
        plt.show()
    elif plot_type == "pie chart":
        print("plotting pie chart")
        # Used for Ordinal Data
    elif plot_type == "normal distribution curve":
        print("plotting normal distribution curve")
        # Used for Interval and Frequency Data
    elif plot_type == "XY chart":
        plt.figure()
        for data_, plot_type in data:
            if plot_type == 'line':
                plt.plot(data_[0], data_[1], 'r')
            elif plot_type == 'dot':
                plt.plot(data_[:,0], data_[:,1], 'b.')
        plt.title(title)
        plt.show()
    else:
        raise Exception("Invalid chart type {}".format(plot_type))
