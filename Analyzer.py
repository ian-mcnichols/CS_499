import numpy as np
import statistics
import scipy.stats as stats
import matplotlib.pyplot as plt


def run_mean(pretest=None, posttest=None, ordinals=None, datatype="Interval"):
    # Ordinal and interval
    if datatype == "Interval":
        return np.mean(pretest), np.mean(posttest)
    elif datatype == "Ordinal":
        return np.mean(ordinals)
    else:
        raise Exception("Bad data type: {}".format(datatype))


def run_median(pretest=None, posttest=None, ordinals=None, datatype="Interval"):
    # Ordinal and interval
    if datatype == "Interval":
        return np.mean(pretest), np.mean(posttest)
    elif datatype == "Ordinal":
        return np.mean(ordinals)
    else:
        raise Exception("Bad data type: {}".format(datatype))


def run_mode(pretest=None, posttest=None, ordinals=None, datatype="Interval"):
    # Ordinal and interval
    if datatype == "Interval":
        return stats.mode(pretest), stats.mode(posttest)
    elif datatype == "Ordinal":
        return stats.mode(ordinals)
    else:
        raise Exception("Bad data type: {}".format(datatype))


def run_stand_dev(pre_test, post_test):
    # interval
    standard_deviation = np.std(np.stack([pre_test, post_test]))
    return standard_deviation


def run_variance(pre_test, post_test):
    # interval
    variance = np.var(np.stack([pre_test, post_test]))
    return variance


def run_percentiles(pre_test, post_test):
    # interval
    # TODO: figure out pretest/posttest
    # Gets the percentile of the data at 0-100 percent in steps of 10
    percentiles = [x*10 for x in range(11)]
    percentile_data = []
    for i in percentiles:
        print('i:', i)
        percentile_data.append(np.percentile(pre_test, i))
    return percentile_data


def run_probability_dist(pretest=None, posttest=None, ordinals=None, datatype="Interval"):
    # change to histogram output
    # ordinal and interval
    # TODO: make work for ordinal data
    if datatype == "Interval":
        data = posttest - pretest
    elif datatype == "Ordinal":
        data = ordinals
    else:
        raise Exception("Bad data type: {}".format(datatype))
    print('data:',data)
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

    my_data = Data.Data("Data/OrdinalDataTest.csv")
    print('data type:', my_data.data_type)
    #print("ordinals: ", my_data.ordinals)
    #print("pretest: ", my_data.pretest)
    if my_data.data_type == 'Interval':
        print("pretest:", my_data.pretest)
        print("postest:", my_data.posttest)
        print("mean: ", run_mean(my_data.pretest, my_data.posttest, datatype=my_data.data_type))
        print("median: ", run_median(my_data.pretest, my_data.posttest, datatype=my_data.data_type))
        print("mode: ", run_mode(my_data.pretest, my_data.posttest, datatype=my_data.data_type))
        print("standard deviation: ", run_stand_dev(my_data.pretest, my_data.posttest))
        print("variance: ", run_variance(my_data.pretest, my_data.posttest))
        print("percentiles: ", run_percentiles(my_data.pretest, my_data.posttest))
        print("probability dist: ", run_probability_dist(my_data.pretest, my_data.posttest, datatype=my_data.data_type))
        print("least squared line: ", run_least_square_line(my_data.pretest, my_data.posttest))
        print("correlation coefficient:", run_correlation_coeff(my_data.pretest, my_data.posttest))
        print("spearman coefficient: ", run_spearman_rank_corr_coeff(my_data.pretest, my_data.posttest))
    elif my_data.data_type == "Ordinal":
        print("mean: ", run_mean(ordinals=my_data.ordinals, datatype=my_data.data_type))
        print("median: ", run_median(ordinals=my_data.ordinals, datatype=my_data.data_type))
        print("mode: ", run_mode(ordinals=my_data.ordinals, datatype=my_data.data_type))
        print("probability dist: ", run_probability_dist(ordinals=my_data.ordinals, datatype=my_data.data_type))


