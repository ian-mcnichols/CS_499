import numpy as np
import statistics
import scipy.stats as stats
import matplotlib.pyplot as plt


def run_mean(pretest=None, posttest=None, intervals=None):
    # Ordinal and interval
    if not intervals:
        data = np.stack(pretest, posttest)
    elif not pretest:
        data = intervals
    else:
        raise Exception("No inputs given to run_mean")
    output = np.mean(data)
    return output


def run_median(pretest=None, posttest=None, intervals=None):
    # Ordinal and interval
    if not intervals:
        data = np.stack(pretest, posttest)
    elif not pretest:
        data = intervals
    else:
        raise Exception("No inputs given to run_median")
    output = np.median(data)
    return output


def run_mode(pretest=None, posttest=None, intervals=None):
    # Ordinal and interval
    if not intervals:
        data = np.stack(pretest, posttest)
    elif not pretest:
        data = intervals
    else:
        raise Exception("No inputs given to run_mode")
    output = np.mode(data)
    return output


def run_stand_dev(pre_test, post_test):
    # interval
    standard_deviation = np.std(pre_test, post_test)
    return standard_deviation


def run_variance(pre_test, post_test):
    # interval
    variance = np.var(pre_test, post_test)
    return variance


def run_percentiles(pre_test, post_test):
    # interval
    # Gets the percentile of the data at 0-100 percent in steps of 10
    percentiles = [x*10 for x in range(11)]
    percentile_data = []
    for i in percentiles:
        print('i:', i)
        percentile_data.append(np.percentile(data, i))
    return percentile_data


def run_probability_dist(pre_test, post_test):
    # change to histogram output
    x = np.linspace(min(data), max(data), len(data))
    mu, std = stats.norm.fit(data)
    snd = stats.norm(mu, std)
    return snd.pdf(x), mu, std


def run_least_square_line(pre_test, post_test):
    # interval
    A = np.vstack([pre_test, np.ones(len(pre_test))]).T
    post_test = post_test[:, np.newaxis]
    alpha = np.dot((np.dot(np.linalg.inv(np.dot(A.T,A)),A.T)),post_test)
    line = pre_test, alpha[0]*pre_test + alpha[1]
    return line


def run_correlation_coeff(pre_test, post_test):
    # interval
    corr_coef = np.corrcoef(pre_test, post_test)
    return corr_coef


def run_spearman_rank_corr_coeff(pre_test, post_test):
    # interval ? (maybe, can possibly delete)
    return stats.spearmanr(pre_test, post_test)


if __name__ == "__main__":
    import Data
    import visualize

    my_data = Data.Data("Interval")
    my_data.read_data_file("Data/IntervalDataTest.csv")
    print("my data expected: ", my_data.pretest)
    run_mean(my_data.pretest, my_data.posttest)
