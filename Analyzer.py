import numpy as np
import statistics
import scipy.stats as stats
import matplotlib.pyplot as plt


def run_mean(data):
    output = np.mean(data)
    return output

def run_median(data): 
    output = np.median(data)
    return output

def run_mode(data):
    output = np.mode(data)
    return output

def run_stand_dev(data):
    standard_deviation = statistics.stdev(data)
    return standard_deviation

def run_variance(data):
    return statistics.variance(data)

def run_percentiles(data):
    # Gets the percentile of the data at 0-100 percent in steps of 10
    percentiles = [x*10 for x in range(11)]
    percentile_data = []
    for i in percentiles:
        print('i:', i)
        percentile_data.append(np.percentile(data, i))
    return percentile_data

def run_probability_dist(data):
    x = np.linspace(min(data), max(data), len(data))
    mu, std = stats.norm.fit(data)
    snd = stats.norm(mu, std)
    return snd.pdf(x), mu, std

def run_binomial_dist(data):
    # TODO: Add logic
    return

def run_chi_squared(data):
    return stats.chi2_contingency(data[0], data[1])

def run_least_square_line(data):
    data_a = data[0]
    data_b = data[1]
    A = np.vstack([data_a, np.ones(len(data_a))]).T
    data_b = data_b[:, np.newaxis]
    alpha = np.dot((np.dot(np.linalg.inv(np.dot(A.T,A)),A.T)),data_b)
    line = data_a, alpha[0]*data_a + alpha[1]
    return alpha

def run_correlation_coeff(data):
    return stats.pearsonr(data[0], data[1])

def run_rank_sum(data):
    return stats.ranksums(data)

def spearman_rank_corr_coeff(data):
    return stats.spearmanr(data[0], data[1])


if __name__ == "__main__":
    import Data

    my_data = Data.Data("Test_Data/IntervalDataTest.csv", "Interval")
    my_data.read_data()
    print("my data expected: ", my_data.pretest)
    #print(run_mean(my_data.expected))
    #print(run_stand_dev(my_data.expected))
    #print(run_percentiles(my_data.expected))
    print(run_chi_squared([my_data.pretest, my_data.posttest]))
