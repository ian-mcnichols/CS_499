import matplotlib.pyplot as plt
import numpy as np


def plot_chart(data, plot_type, title):
    if plot_type == "horizontal bar chart":
        print("plotting horizontal bar chart")
    elif plot_type == "vertical bar chart":
        plt.figure()
        plt.bar(data[0], data[1], width=5)
        plt.title(title)
        plt.show()
    elif plot_type == "pie chart":
        print("plotting pie chart")
    elif plot_type == "normal distribution curve":
        print("plotting normal distribution curve")
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
