import numpy as np
import statistics
import scipy.stats as stats


class Analyzer:
    def __init__(self, data_type):
        self.data_type = data_type
        self.plot_output = True

    def set_rows(self, row_start, row_end):
        self.rows = range(row_start, row_end)

    def set_cols(self, col_start, col_end):
        self.cols = range(col_start, col_end)

    def toggle_plotting(self):
        self.plot_output = not self.plot_output

    def run_mean(self, data):
        return np.mean(data)

    def run_median(self, data):
        return np.median(data)

    def run_mode(self, data):
        return np.mode(data)

    def run_stand_dev(self, data):
        return statistics.stdev(data)

    def run_variance(self, data):
        return statistics.variance(data)

    def run_percentiles(self, data, percent):
        return np.percentile(data, percent)

    def run_probability_dist(self, data):
        return stats.norm(data)

    def run_binomial_dist(self, data_a, data_b):
        return stats.binom.stats(data_a, data_b)

    def run_chi_squared(self, data_a, data_b):
        return stats.chi2_contingency(data_a, data_b)

    def run_least_square_line(self, data_a, data_b):
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

    my_data = Data.Data("//alam01/alam01/slow02/imcnichols/Homework/CS 499/Test_Data/FrequencyDataTest.csv",
                        "Frequency")
    my_data.read_data()
    print("my data expected: ", my_data.expected)
    my_analyzer = Analyzer(my_data.data_type)
    print(my_analyzer.run_mean(my_data.expected))
