import numpy as np
import statistics
import scipy.stats as stats
import matplotlib.pyplot as plt


class Analyzer:
    def __init__(self, data_type):
        self.data_type = data_type
        self.plot_output = True

    def toggle_plotting(self):
        self.plot_output = not self.plot_output

    def plot_chart(self, data, plot_type, title):
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

    def run_mean(self, data):  # No plotting needed here
        output = np.mean(data)
        return output

    def run_median(self, data): # No plotting
        output = np.median(data)
        return output

    def run_mode(self, data): # No plotting
        output = np.mode(data)
        return output

    def run_stand_dev(self, data):  # No plotting
        standard_deviation = statistics.stdev(data)
        return standard_deviation

    def run_variance(self, data):  # No plotting
        return statistics.variance(data)

    def run_percentiles(self, data):
        # Gets the percentile of the data at 0-100 percent in steps of 10
        percentiles = [x*10 for x in range(11)]
        percentile_data = []
        for i in percentiles:
            print('i:', i)
            percentile_data.append(np.percentile(data, i))
        if self.plot_output:
            self.plot_chart([percentiles, percentile_data], "vertical bar chart", "Percentiles")
        return percentile_data

    def run_probability_dist(self, data):
        x = np.linspace(min(data), max(data), len(data))
        mu, std = stats.norm.fit(data)
        snd = stats.norm(mu, std)
        if self.plot_output:
            self.plot_chart([x, snd.pdf(x)], "XY chart", "Probability Distribution")
        return snd.pdf(x), mu, std

    def run_binomial_dist(self, data):
        # TODO: Add logic
        return

    def run_chi_squared(self, data):
        return stats.chi2_contingency(data[0], data[1])

    def run_least_square_line(self, data):
        data_a = data[0]
        data_b = data[1]
        A = np.vstack([data_a, np.ones(len(data_a))]).T
        data_b = data_b[:, np.newaxis]
        alpha = np.dot((np.dot(np.linalg.inv(np.dot(A.T,A)),A.T)),data_b)
        line = data_a, alpha[0]*data_a + alpha[1]
        return alpha

    def run_correlation_coeff(self, data_a, data_b):
        return stats.pearsonr(data_a, data_b)

    def run_rank_sum(self, data_a, data_b):
        return stats.ranksums(data_a, data_b)

    def spearman_rank_corr_coeff(self, data_a, data_b):
        return stats.spearmanr(data_a, data_b)


if __name__ == "__main__":
    import Data

    my_data = Data.Data("Test_Data/IntervalDataTest.csv", "Interval")
    my_data.read_data()
    print("my data expected: ", my_data.pretest)
    my_analyzer = Analyzer(my_data.data_type)
    #print(my_analyzer.run_mean(my_data.expected))
    #print(my_analyzer.run_stand_dev(my_data.expected))
    #print(my_analyzer.run_percentiles(my_data.expected))
    print(my_analyzer.run_chi_squared([my_data.pretest, my_data.posttest]))
