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
    standard_deviation = np.std(data)
    return standard_deviation


def run_variance(data):
    variance = np.var(data)
    return variance


def run_percentiles(data):
    # Gets the percentile of the data at 0-100 percent in steps of 10
    percentiles = [x*10 for x in range(11)]
    percentile_data = []
    for i in percentiles:
        print('i:', i)
        percentile_data.append(np.percentile(data, i))
    return percentile_data


def run_probability_dist(data):
    if len(data.shape) > 1:
        print("Warning: Cannot run on 2D data. Using first dimension")
    data = data[:,0]
    x = np.linspace(min(data), max(data), len(data))
    mu, std = stats.norm.fit(data)
    snd = stats.norm(mu, std)
    return snd.pdf(x), mu, std


def run_binomial_dist(data):
    # TODO: Add logic
    print('data shape:', data.shape)
    p = len(np.where(data[:,0] < data[:,1])) / data.shape[0]
    data_binom = stats.binom.rvs(n=data.shape[0], p=p)
    return data_binom


def run_chi_squared(data):
    if len(data.shape) < 2:
        raise Exception("Data shape not accepted {}".format(str(data.shape)))
    chi_squared_test = 0
    for i in range(data.shape[0]):
        chi_squared_test += (data[i][1] - data[i][0])**2 / data[i][0]
    return chi_squared_test


def run_least_square_line(data):
    if len(data.shape) < 2:
        raise Exception("Data shape not accepted {}".format(str(data.shape)))
    data_a = data[:,0]
    data_b = data[:,1]
    A = np.vstack([data_a, np.ones(len(data_a))]).T
    data_b = data_b[:, np.newaxis]
    alpha = np.dot((np.dot(np.linalg.inv(np.dot(A.T,A)),A.T)),data_b)
    line = data_a, alpha[0]*data_a + alpha[1]
    return line


def run_correlation_coeff(data):
    return stats.pearsonr(data[0], data[1])


def run_rank_sum(data):
    return stats.ranksums(data)


def run_spearman_rank_corr_coeff(data):
    return stats.spearmanr(data[0], data[1])


def run_function(function_name, data):
    if len(data.shape) > 2:
        raise Exception("Cannot handle data shape {}".format(str(data.shape)))
    if function_name == "mean":
        return run_mean(data)
    elif function_name == "median":
        return run_median(data)
    elif function_name == "mode":
        return run_mode(data)
    elif function_name == "standard deviation":
        return run_stand_dev(data)
    elif function_name == "variance":
        return run_variance(data)
    elif function_name == "percentiles":
        return run_percentiles(data)
    elif function_name == "probability distribution":
        return run_probability_dist(data)
    elif function_name == "binomial distribution":
        return run_binomial_dist(data)
    elif function_name == "chi squared":
        return run_chi_squared(data)
    elif function_name == "least square":
        return run_least_square_line(data)
    elif function_name == "correlation coefficient":
        return run_correlation_coeff(data)
    elif function_name == "rank sum":
        return run_rank_sum(data)
    elif function_name == "spearman rank coefficient":
        return run_spearman_rank_corr_coeff(data)
    else:
        raise Exception("Unknown function type {}".format(function_name))


if __name__ == "__main__":
    import Data
    import visualize

    my_data = Data.Data("Interval")
    my_data.read_data_file("Data/IntervalDataTest.csv")
    print("my data expected: ", my_data.data)
    print('standard dev:', run_stand_dev(my_data.data))
    print('variance:', run_variance(my_data.data))
    print('probability dist:', run_probability_dist(my_data.data))
    print('binomial dist:', run_binomial_dist(my_data.data))
    print('least square:', run_least_square_line(my_data.data))
    print('chi squared:', run_chi_squared(my_data.data))
    line = run_least_square_line(my_data.data)
    visualize.plot_chart([(line, 'line'), (my_data.data, 'dot')], plot_type='XY chart', title='least square regression')
