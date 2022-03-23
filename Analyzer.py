import numpy as np
import statistics
import scipy.stats as stats
import matplotlib.pyplot as plt
import visualize


def run_mean(data):
    """Calculates the mean of the given data

    :param pretest: numpy array of pre-test data
    :param posttest: numpy array of post-test data
    :param datatype: "interval" or "ordinal"
    :return: mean of posttest, mean of pretest, mean of difference
    """
    results = []
    max_column = 0
    # For each column
    for i in range(1, len(data.dtype.names)):
        # Get data for column
        column = data[data.dtype.names[i]]
        # Run mean function on column data and add to results
        results.append(np.mean(column))
        max_column = i
    # Find mean of difference between first set of data and last
    difference = data[data.dtype.names[max_column]] - data[data.dtype.names[1]]
    results.append(np.mean(difference))
    return results


def run_median(data, datatype="Interval"):
    """Calculates the median on a given dataset

    :param pretest: numpy array of pre-test data
    :param posttest: numpy array of post-test data
    :param ordinals: numpy array of ordinal data
    :param datatype: "interval" or "ordinal"
    :return: interval-list, the median of the pretest, posttest, and change
             ordinals-int, the index of the column that is the median for all the questions
    """
    if datatype.lower() == "interval":
        results = []
        max_column = 0
        for i in range(1, len(data.dtype.names)):
            # Get data for column
            column = data[data.dtype.names[i]]
            # Run median function on column data and add to results
            results.append(np.median(column))
            max_column = i
        # Find median of difference between first set of data and last
        difference = data[data.dtype.names[max_column]] - data[data.dtype.names[1]]
        results.append(np.median(difference))
        return results
    elif datatype.lower() == "ordinal":
        # Array to store mode for each question
        results = []
        # Determine median response for each question
        # For each row/question
        for i in range(len(data)):
            # Get row as list
            row = list(data[i])
            row_values = []
            # Add number of responses for each index number to list
            for j in range(1, len(row)):
                num_responses = row[j]
                for x in range(num_responses):
                    row_values.append(j)
            # Find median response for each row
            row_median = np.median(row_values)
            results.append(row_median)
        return results
    else:
        raise Exception("Bad data type: {}".format(datatype))


def run_mode(data, datatype="Interval"):
    """Calculates the mode of a given dataset

    :param pretest: numpy array of pre-test data
    :param posttest: numpy array of post-test data
    :param ordinals: numpy array of ordinal data
    :param datatype: "interval" or "ordinal"
    :return: interval-the mode of the pretest, posttest, and change
             ordinals-the mode each row/question
    """
    if datatype.lower() == "interval":
        results = []
        max_column = 0
        for i in range(1, len(data.dtype.names)):
            # Get data for column
            column = data[data.dtype.names[i]]
            # Run mode function on column data and add to results
            results.append(stats.mode(column))
            max_column = i
        # Find median of difference between first set of data and last
        difference = data[data.dtype.names[max_column]] - data[data.dtype.names[1]]
        results.append(stats.mode(difference))
        return results
    elif datatype.lower() == "ordinal":
        # Array to store mode for each question
        results_name = []
        results_number = []
        # Determine answer with highest number of responses for each question
        for i in range(len(data)):
            row = list(data[i])
            row_mode = max(row[1:])
            results_name.append(data.dtype.names[row.index(row_mode)])
            results_number.append(row.index(row_mode))
        visualize.plot_chart(data, "Vertical Bar Chart", results=results_number, data_type='ordinal')
        return results_name
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


def run_function(function_name, data, data_type="Interval"):
    """Driver to run any stats operation given a function and data

    :param function_name: string, operation to run on the data
    :param argv: pretest : numpy array of size [N] (if interval)
                 posttest : numpy array of size [N] (if interval)
                 ordinals: numpy array of size [NxM] (if ordinal)
    :return: function corresponding to operation type
    """
    if function_name == "Mean":
        return run_mean(data)
    elif function_name == "Median":
        return run_median(data, datatype=data_type)
    elif function_name == "Mode":
        return run_mode(data, datatype=data_type)
    # elif function_name == "Standard deviation":
    #     return run_stand_dev(pretest, posttest)
    # elif function_name == "Variance":
    #     return run_variance(pretest, posttest)
    # elif function_name == "Percentiles":
    #     return run_percentiles(pretest, posttest)
    # elif function_name == "Least square line":
    #     return run_least_square_line(pretest, posttest)
    # elif function_name == "Probability distribution":
    #     return run_probability_dist(pretest, posttest, ordinals, datatype=data_type)
    # elif function_name == "Correlation coefficient":
    #     return  run_correlation_coeff(pretest, posttest)
    # elif function_name == "Spearman rank correction coefficient":
    #     return run_spearman_rank_corr_coeff(pretest, posttest)
    else:
        raise Exception("Function does not exist: {}".format(function_name))


if __name__ == "__main__":
    import Data
    import visualize

    my_data = Data.Data("Data/OrdinalDataTest.csv", data_type="ordinal")
    print('data type:', my_data.data_type)
    print(my_data.data_np)
    #print("ordinals: ", my_data.ordinals)
    #print("pretest: ", my_data.pretest)
    if my_data.data_type == 'interval':
        # print("pretest:", my_data.data_np['Pretest'], datatype=my_data.data_type)
        # print("posttest:", my_data.data_np['Posttest'], datatype=my_data.data_type)
        print("mean: ", run_mean(my_data.data_np))
        print("median: ", run_median(my_data.data_np, datatype=my_data.data_type))
        print("mode: ", run_mode(my_data.data_np, datatype=my_data.data_type))
        # print("standard deviation: ", run_stand_dev(my_data.data_np))
        # print("variance: ", run_variance(my_data.data_np)
        # print("percentiles: ", run_percentiles(my_data.data_np)
        # print("probability dist: ",
        #   run_probability_dist(my_data.data_np['Pretest'], my_data.data_np['Posttest'], datatype=my_data.data_type))
        # print("least squared line: ", run_least_square_line(my_data.data_np['Pretest'], my_data.data_np['Posttest']))
        # print("correlation coefficient:", run_correlation_coeff(my_data.data_np['Pretest'], my_data.data_np['Posttest']))
        # print("spearman coefficient: ",
        #   run_spearman_rank_corr_coeff(my_data.data_np['Pretest'], my_data.data_np['Posttest']))
    elif my_data.data_type == "ordinal":
        print("median: ", run_median(my_data.data_np, datatype=my_data.data_type))
        print("mode: ", run_mode(my_data.data_np, datatype=my_data.data_type))
        # print("probability dist: ", run_probability_dist(ordinals=my_data.ordinals, datatype=my_data.data_type))
