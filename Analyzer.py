import numpy as np
import statistics
import scipy.stats as stats
import matplotlib.pyplot as plt



def run_mean(pretest=None, posttest=None, ordinals=None, datatype="Interval"):
    """Calculates the mean of the given data

    :param pretest: numpy array of pre-test data
    :param posttest: numpy array of post-test data
    :param ordinals: numpy array of ordinal data
    :param datatype: "interval" or "ordinal"
    :return: if interval: mean of posttest, mean of pretest, mean of difference
             if ordinal: average max. number of votes on the most popular answer
    """
    # Ordinal and interval
    if datatype.lower() == "interval":
        return [np.mean(pretest), np.mean(posttest), np.mean(posttest - pretest)]
    elif datatype.lower() == "ordinal":
        return np.mean([x.max() for x in ordinals])
    else:
        raise Exception("Bad data type: {}".format(datatype))


def run_median(pretest=None, posttest=None, ordinals=None, datatype="Interval"):
    """Calculates the median on a given dataset

    :param pretest: numpy array of pre-test data
    :param posttest: numpy array of post-test data
    :param ordinals: numpy array of ordinal data
    :param datatype: "interval" or "ordinal"
    :return: interval-list, the median of the pretest, posttest, and change
             ordinals-int, the index of the column that is the median for all the questions
    """
    if datatype.lower() == "interval":
        return [np.median(pretest), np.median(posttest), np.median(posttest - pretest)]
    elif datatype.lower() == "ordinal":
        columns = [sum(ordinals[:,i]) for i in range(ordinals.shape[1])]
        return np.where(columns == max(columns))[0][0]  # I think there is a better way to do this
    else:
        raise Exception("Bad data type: {}".format(datatype))


def run_mode(pretest=None, posttest=None, ordinals=None, datatype="Interval"):
    """Calculates the mode of a given dataset

    :param pretest: numpy array of pre-test data
    :param posttest: numpy array of post-test data
    :param ordinals: numpy array of ordinal data
    :param datatype: "interval" or "ordinal"
    :return: interval-the mode of the pretest, posttest, and change
             ordinals-the mode of all of it. TODO: figure out what this should be
    """
    if datatype.lower() == "interval":
        return [stats.mode(pretest)[0][0], stats.mode(posttest)[0][0], stats.mode(posttest-pretest)[0][0]]
    elif datatype.lower() == "ordinal":
        return stats.mode(ordinals)[0][0]
    else:
        raise Exception("Bad data type: {}".format(datatype))


def run_stand_dev(pre_test, post_test):
    """calculates the standard deviation of interval data

    :param pre_test: numpy array of size [N]
    :param post_test: numpy array of size [N]
    :return: float, standard deviation of the change in data
    """
    standard_deviation = np.std(post_test-pre_test)
    return standard_deviation


def run_variance(pre_test, post_test):
    """calculates the variance of interval data

    :param pre_test: numpy array of size [N]
    :param post_test: numpy array of size [N]
    :return: float, variance of the change in data
    """
    variance = np.var(post_test-pre_test)
    return variance


def run_percentiles(pre_test, post_test):
    """Calculates the percentiles of interval data

    :param pre_test: numpy array of size [N]
    :param post_test: numpy array of size [N]
    :return: [10] list of floats, the 10-100th percentile of the change in pre-post test data
    """
    change_data = post_test - pre_test
    percentiles = [x*10 for x in range(11)]
    percentile_data = []
    for i in percentiles:
        percentile_data.append(np.percentile(change_data, i))
    return percentile_data


def run_probability_dist(pretest=None, posttest=None, ordinals=None, datatype="Interval"):
    # change to histogram output
    # ordinal and interval
    # TODO: make work for ordinal data
    if datatype == "Interval":
        data = posttest - pretest
    elif datatype == "Ordinal":
        data = ordinals[0]
    else:
        raise Exception("Bad data type: {}".format(datatype))
    x = np.linspace(min(data), max(data), len(data))
    mu, std = stats.norm.fit(data)
    snd = stats.norm(mu, std)
    return snd.pdf(x), mu, std


def run_least_square_line(pre_test, post_test):
    """Calculates the least square regression line of correlation between pretest and posttest

    :param pre_test: numpy array of size [N]
    :param post_test: numpy array of size [N]
    :return:
    """
    A = np.vstack([pre_test, np.ones(len(pre_test))]).T
    post_test = post_test[:, np.newaxis]
    alpha = np.dot((np.dot(np.linalg.inv(np.dot(A.T,A)),A.T)),post_test)
    line = pre_test, alpha[0]*pre_test + alpha[1]
    return line


def run_correlation_coeff(pre_test, post_test):
    """Return Pearson product-moment correlation coefficient

    :param pre_test: numpy array of size [N]
    :param post_test: numpy array of size [N]
    :return: float, the minimum value of the correlation coefficient matrix
    """
    # take the first value of the correlation matrix
    corr_coef = np.corrcoef(pre_test, post_test)[1][0]
    return corr_coef


def run_spearman_rank_corr_coeff(pre_test, post_test):
    """Calculates a Spearman rank-order correlation coefficient and the p-value to test for non-correlation.

    :param pre_test: numpy array of size [N]
    :param post_test: numpy array of size [N]
    :return: rho : float or ndarray (2-D square) Spearman correlation matrix or correlation coefficient
                    (if only 2 variables are given as parameters. Correlation matrix is square with length equal to
                     total number of variables (columns or rows) in a and b combined.

    :return: p-value : float The two-sided p-value for a hypothesis test whose null hypothesis is that two sets of
                       data are uncorrelated, has same dimension as rho.

    """
    return stats.spearmanr(pre_test, post_test)[0], stats.spearmanr(pre_test, post_test)[1]


def run_function(function_name, *argv):
    """Driver to run any stats operation given a function and data

    :param function_name: string, operation to run on the data
    :param argv: pretest : numpy array of size [N] (if interval)
                 posttest : numpy array of size [N] (if interval)
                 ordinals: numpy array of size [NxM] (if ordinal)
    :return: function corresponding to operation type
    """
    pretest = None
    posttest = None
    ordinals = None
    if len(argv) > 1:
        data_type = "Interval"
        pretest = argv[0]
        posttest = argv[1]
    elif len(argv) == 1:
        data_type = "Ordinal"
        ordinals = argv[0]
    else:
        raise Exception("Unknown input types {}".format(argv))
    if function_name == "mean":
        return run_mean(pretest, posttest, ordinals, datatype=data_type)
    elif function_name == "median":
        return run_median(pretest, posttest, ordinals, datatype=data_type)
    elif function_name == "mode":
        return run_mode(pretest, posttest, ordinals, datatype=data_type)
    elif function_name == "stand_dev":
        return run_stand_dev(pretest, posttest)
    elif function_name == "variance":
        return run_variance(pretest, posttest)
    elif function_name == "percentiles":
        return run_percentiles(pretest, posttest)
    elif function_name == "lsr":
        return run_least_square_line(pretest, posttest)
    elif function_name == "prob_dist":
        return run_probability_dist(pretest, posttest, ordinals, datatype=data_type)
    elif function_name == "corr_coeff":
        return  run_correlation_coeff(pretest, posttest)
    elif function_name == "spearman_coeff":
        return run_spearman_rank_corr_coeff(pretest, posttest)
    else:
        raise Exception("Function does not exist: {}".format(function_name))


if __name__ == "__main__":
    import Data
    import visualize

    my_data = Data.Data("Data/IntervalDataTest.csv")
    print('data type:', my_data.data_type)
    #print("ordinals: ", my_data.ordinals)
    #print("pretest: ", my_data.pretest)
    if my_data.data_type == 'Interval':
        print("pretest:", my_data.data_np['Pretest'])
        print("posttest:", my_data.data_np['Posttest'])
        print("mean: ", run_mean(my_data.data_np['Pretest'], my_data.data_np['Posttest'], datatype=my_data.data_type))
        print("median: ", run_median(my_data.data_np['Pretest'], my_data.data_np['Posttest'], datatype=my_data.data_type))
        print("mode: ", run_mode(my_data.data_np['Pretest'], my_data.data_np['Posttest'], datatype=my_data.data_type))
        print("standard deviation: ", run_stand_dev(my_data.data_np['Pretest'], my_data.data_np['Posttest']))
        print("variance: ", run_variance(my_data.data_np['Pretest'], my_data.data_np['Posttest']))
        print("percentiles: ", run_percentiles(my_data.data_np['Pretest'], my_data.data_np['Posttest']))
        print("probability dist: ",
          run_probability_dist(my_data.data_np['Pretest'], my_data.data_np['Posttest'], datatype=my_data.data_type))
        print("least squared line: ", run_least_square_line(my_data.data_np['Pretest'], my_data.data_np['Posttest']))
        print("correlation coefficient:", run_correlation_coeff(my_data.data_np['Pretest'], my_data.data_np['Posttest']))
        print("spearman coefficient: ",
          run_spearman_rank_corr_coeff(my_data.data_np['Pretest'], my_data.data_np['Posttest']))
    elif my_data.data_type == "Ordinal":
        print("mean: ", run_mean(ordinals=my_data.ordinals, datatype=my_data.data_type))
        print("median: ", run_median(ordinals=my_data.ordinals, datatype=my_data.data_type))
        print("mode: ", run_mode(ordinals=my_data.ordinals, datatype=my_data.data_type))
        print("probability dist: ", run_probability_dist(ordinals=my_data.ordinals, datatype=my_data.data_type))
