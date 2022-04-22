import numpy as np


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
        """Loads data file
        :param filepath: String to .csv data file
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

    def _to_numpy(self):
        """Converts np.genfromtxt output to numpy array of data and row/column labels"""
        if self.data is None:
            return
        # Set column labels
        column_labels = [x for x in self.data.dtype.names]
        self.column_labels = column_labels[1:]
        # Get data from each column
        data = [self.data[x] for x in column_labels]
        # Set row labels, gotten from first column of data
        self.row_labels = [x for x in data[0]]
        # Strip out row labels to get just numerical values
        data_values = data[1:]
        print("data:", data_values)
        # Save numpy array of data values
        self.data_np = np.array(data_values)

    def add_data(self, data, columns, rows):
        """Adds data from list of lists
        :param data: List of lists containing data values
        :param columns: Column labels
        :param rows: Row labels
        """
        # Check that they're all the same length first
        for x in range(len(data) - 1):
            if len(data[x]) != len(data[x+1]):
                print("No data added, dimensions wrong.")
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
            print("No data added, data type wrong.")

    def add_result(self, function_ran, output):
        """Adds function/result pair to results dictionary
        :param function_ran: String, the function
        :param output: the function's output
        """
        self.results.update({function_ran: output})


if __name__ == '__main__':

    my_data = Data("Data/IntervalDataTest.csv", "interval")
    print(my_data.data)
    my_data = Data("GUI", "interval")
    my_data.add_data([['1', '1', '1,', '1', '1'], ['1', '2', '1', '2', '1']], ['pretest', 'posttest'],
                     ['question1', 'question2', 'question3', 'question4', 'question5'])
    print("My data:", my_data.data)

    my_data = Data("GUI", "ordinal")
    my_data.add_data([[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]], [], [])
    print("My data:", my_data.data)

