import numpy as np
import logging
do_logging = True


class Data:
    def __init__(self, file_name, data_type):
        # Initialize variables
        self.data_type = data_type
        self.data = None
        self.data_np = None
        self.column_labels = None
        self.row_labels = None
        self.results = {}
        # If not reading in data from manual entry
        if file_name != "GUI":
            # Read in the given file
            self.read_data_file(filepath=file_name)

    def read_data_file(self, filepath):
        """Loads data from a .csv file
        :param filepath: The string path to a .csv file
        """
        with open(filepath, "r") as file:
            # Find file formatting from first line
            sections = file.readline()
            if len(sections.split(",")) > 1:
                delimiter = ","
            elif len(sections.split("\t")) > 1:
                delimiter = "\t"
            else:
                raise Exception("File is not comma separated or tab delineated.")
            # Read in data
            self.data = np.genfromtxt(filepath, dtype=None, delimiter=', ', skip_header=1, encoding=None)
            # Set names for columns, striping white space
            self.data.dtype.names = [x.strip() for x in sections.split(delimiter)]
            file.close()
            # Strip down data to numpy with values, list of column labels, and list of row labels
            self._to_numpy()
        return

    def _to_numpy(self):
        """Converts np.genfromtxt output to numpy array of data and row/column labels"""
        if self.data is None:
            return
        # Set column labels
        column_labels = [x for x in self.data.dtype.names]
        self.column_labels = column_labels[1:]

    def add_data(self, data, columns, rows):
        """Adds data from list of lists
        :param data: List of lists, containing rows and columns of data
        :param columns: Number of columns
        :param rows: Number of rows
        """
        # Check that they're all the same length first
        for x in range(len(data) - 1):
            if len(data[x]) != len(data[x+1]):
                if do_logging:
                    logging.error("No data added, dimensions wrong.")
                return
        try:
            self.data_np = np.dstack(data)[0].astype('float')
            if len(columns) != self.data_np.shape[0]:
                columns = ["Column {}".format(str(i+1)) for i in range(self.data_np.shape[0])]
            if len(rows) != self.data_np.shape[1]:
                rows = ["Row {}".format(str(i+1)) for i in range(self.data_np.shape[1])]
            self.column_labels = columns
            self.row_labels = rows
        except ValueError:
            if do_logging:
                logging.error("No data added, data type wrong.")

    def add_result(self, function_ran, output):
        """Adds results from a function to the object's results dictionary
        :param function_ran: A string describing which function was run
        :param output: The output of that function
        """
        self.results.update({function_ran: output})

if __name__ == '__main__':

    my_data = Data("Data/IntervalDataTest.csv", "interval")

    if do_logging:
        logging.info(np.array2string(my_data.data_np))
    my_data = Data("GUI", "interval")
    my_data.add_data([['1', '1', '1,', '1', '1'], ['1', '2', '1', '2', '1']], ['pretest', 'posttest'],
                     ['question1', 'question2', 'question3', 'question4', 'question5'])
    if do_logging:
        logging.info(f"My data: {np.array2string(my_data.data_np)}")

    my_data = Data("GUI", "ordinal")
    my_data.add_data([[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]], [], [])
    if do_logging:
        logging.info(f"My data: {np.array2string(my_data.data_np)}")
