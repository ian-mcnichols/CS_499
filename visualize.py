import matplotlib.pyplot as plt
import numpy as np


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
        display_data = np.array(data)
        # Used for INterval and Frequency Data
        if display_data.shape[0] != 2:
            raise Exception("Invalid shape for XY chart data {}".format(display_data.shape))
        plt.figure()
        plt.title(title)
        plt.plot(display_data[0], display_data[1])
        plt.show()
    else:
        raise Exception("Invalid chart type {}".format(plot_type))
