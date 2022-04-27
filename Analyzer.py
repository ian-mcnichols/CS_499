import numpy as np
import scipy.stats as stats


def run_mean(data):
    """Calculates the mean of the given data

    :param data: data to run the function on
    :return: array containing the mean of each column of values in the data, and the mean of the difference
             between the last column and the first column
    """
    results = []
    # For each column
    for i in range(data.shape[0]):
        # Get data for column
        column = data[i]
        # Run mean function on column data and add to results
        results.append(np.mean(column))
    # Find mean of difference between first set of data and last
    difference = data[-1] - data[0]
    results.append(np.mean(difference))
    return results


def run_median(data, datatype="Interval"):
    """Calculates the median on a given dataset

    :param data: data to run the function on
    :param datatype: "interval" or "ordinal"
    :return: results, array containing either the median for each column of data for interval data
                      OR the median response for each question/row for ordinal data
    """
    # Array to store results for each set of data
    results = []
    if datatype.lower() == "interval":
        for i in range(data.shape[0]):
            # Get data for column
            column = data[i]
            # Run median function on column data and add to results
            results.append(np.median(column))
        # Find median of difference between first set of data and last
        difference = data[-1] - data[0]
        results.append(np.median(difference))
        return results
    elif datatype.lower() == "ordinal":
        # Determine median response for each question
        # For each row/question
        columns, rows = data.shape
        for i in range(rows):
            # Get row as list
            row = list(data[:, i])
            row_values = []
            # Add number of responses for each index number to list
            for j in range(len(row)):
                num_responses = row[j]
                for x in range(num_responses):
                    row_values.append(j)
            # Find median response for each row
            row_median = np.median(row_values)
            # Add 1 to change from column starting at 0 to columns starting at 1
            results.append(row_median+1)
        return results
    else:
        raise Exception("Bad data type: {}".format(datatype))


def run_mode(data, datatype="Interval"):
    """Calculates the mode of a given dataset

    :param data: data to run the function on
    :param datatype: interval or ordinal
    :return: the mode for each column of data for interval data and the mode of the difference between the first \
     and last columns, or the mode for each row if ordinal data
    """
    if datatype.lower() == "interval":
        results = []
        for i in range(data.shape[0]):
            # Get data for column
            column = data[i]
            # Run mode function on column data and add to results
            results.append(stats.mode(column)[0][0])
        # Find mode of difference between first set of data and last
        difference = data[-1] - data[0]
        results.append(stats.mode(difference)[0][0])
        return results
    elif datatype.lower() == "ordinal":
        # Array to store mode for each question
        results_number = []
        # Determine answer (column) with highest number of responses for each question (row)
        columns, rows = data.shape
        for i in range(rows):
            row = list(data[:, i])
            row_mode = max(row)
            results_number.append(row.index(row_mode)+1)
        return results_number
    else:
        raise Exception("Bad data type: {}".format(datatype))


def run_stand_dev(data):
    """Calculates the standard deviation of interval data

    :param data: data to run the function on
    :return: list, standard deviation of each column of data and the change in first and last column of data
    """
    results_stand_dev = []
    for i in range(data.shape[0]):
        # Get data for column
        column = data[i]
        # Run standard deviation function on column data and add to results
        results_stand_dev.append(np.std(column))
    # Find Standard deviation of difference between first set of data and last
    difference = data[-1] - data[0]
    results_stand_dev.append(np.std(difference))
    return results_stand_dev


def run_variance(data):
    """Calculates the variance of interval data

    :param data: data to run function on
    :return: list, variance of the each column of data and the change in first and last column of data
    """
    results_variance = []
    for i in range(data.shape[0]):
        # Get data for column
        column = data[i]
        # Run variation function on column data and add to results
        results_variance.append(np.var(column))
    # Find variation of difference between first set of data and last
    difference = data[-1] - data[0]
    results_variance.append(np.var(difference))
    return results_variance


def run_percentiles(data):
    """Calculates the percentiles of interval data

    :param data: data to run the function on
    :return: [10] list of floats, the 0-100th percentile of each column of data and the change in first and last
             columns of data
    """
    # Difference between the last column of data and the first column of data
    change_data = data[-1] - data[0]
    percentiles = [x * 10 for x in range(11)]
    # For each column of data, excluding row labels, create an array for the results
    column_results = [[] for i in range(data.shape[0])]
    change_percentile = []
    # For each column
    for i in range(data.shape[0]):
        # For each percentile
        for j in percentiles:
            column_results[i].append(np.percentile(data[i], j))
    for j in percentiles:
        change_percentile.append(np.percentile(change_data, j))
    return [column_results, change_percentile]


def run_probability_dist(data, datatype):
    """A placeholder, probability distribution is solely a plotting problem"""
    return


def run_least_square_line(data):
    """Calculates the least square regression line of correlation between first and last column of data

    :param data: data to run the function on
    :return: slope of LSRL, y-intercept of LSRL
    """
    out = stats.linregress(data[0], data[-1])
    return [out[0], out[1]]


def run_correlation_coeff(data):
    """Return Pearson product-moment correlation coefficient

    :param data: data to run the function on
    :return: float, the minimum value of the correlation coefficient matrix
    """
    # take the first value of the correlation matrix
    corr_coef = np.corrcoef(data[0], data[-1])[1][0]
    return corr_coef


def run_spearman_rank_corr_coeff(data):
    """Calculates a Spearman rank-order correlation coefficient and the p-value to test for non-correlation.

    :param data: data to run function on
    :return: float or ndarray (2-D square) Spearman correlation matrix or correlation coefficient \
                    (if only 2 variables are given as parameters. Correlation matrix is square with length equal to \
                     total number of variables (columns or rows) in a and b combined.)
    """
    results = [stats.spearmanr(data[0], data[-1])[0],
            stats.spearmanr(data[0], data[-1])[1]]
    for idx, result in enumerate(results):
        if result != 0 and not (result > 0) and not (result < 0):
            results[idx] = 1
    return results


def run_function(function_name, data, data_type="Interval"):
    """Driver to run any stats operation given a function and data

    :param function_name: string, operation to run on the data
    :param data: numpy array of data to run on
    :param data_type: string, ordinal or interval
    :param display: boolean, whether to display plots
    :param save: boolean, whether to save plots
    :return: function corresponding to operation type
    """
    if function_name == "Mean":
        return run_mean(data)
    elif function_name == "Median":
        return run_median(data, datatype=data_type)
    elif function_name == "Mode":
        return run_mode(data, datatype=data_type)
    elif function_name == "Standard deviation":
        return run_stand_dev(data)
    elif function_name == "Variance":
        return run_variance(data)
    elif function_name == "Percentiles":
        return run_percentiles(data)
    elif function_name == "Least square line":
        return run_least_square_line(data)
    elif function_name == "Probability distribution":
        return run_probability_dist(data, datatype=data_type)
    elif function_name == "Correlation coefficient":
        return run_correlation_coeff(data)
    elif function_name == "Spearman rank correlation coefficient":
        return run_spearman_rank_corr_coeff(data)
    else:
        raise Exception("Function does not exist: {}".format(function_name))
