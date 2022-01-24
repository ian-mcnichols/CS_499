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
        display_data = np.array(data)
        if display_data.shape[0] != 2:
            raise Exception("Invalid shape for XY chart data {}".format(display_data.shape))
        plt.figure()
        plt.title(title)
        plt.plot(display_data[0], display_data[1])
        plt.show()
    else:
        raise Exception("Invalid chart type {}".format(plot_type))
