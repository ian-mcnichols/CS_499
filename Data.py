from numpy.core.defchararray import index
import numpy as np


class Data:
    def __init__(self, file_name, data_type):
        self.data_type = data_type
        self.data_np = None
        self.column_labels = None
        self.row_labels = None
        self.results = {}
        if file_name != "GUI":
            # Read in the given file
            self.read_data_file(filepath=file_name)

    def read_data_file(self, filepath):
        """Loads data from a .csv file
        :param filepath The string path to a .csv file
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
            # Read in data as a numpy array
            self.data_np = np.genfromtxt(filepath, dtype=None, delimiter=', ', skip_header=1, encoding=None)
            # Set names for columns, striping white space
            self.data_np.dtype.names = [x.strip() for x in sections.split(delimiter)]
            file.close()
            self._to_numpy()
        return

    def _to_numpy(self):
        """Converts np.genfromtxt output to numpy array of data and row/column labels"""
        if self.data_np is None:
            return
        column_labels = [x for x in self.data_np.dtype.names]
        data = [self.data_np[x] for x in column_labels]
        row_labels = [x for x in data[0]]
        self.row_labels = row_labels
        self.column_labels = column_labels[1:]
        data = data[1:]
        print("data:", data)
        self.data_np = np.array(data) #np.dstack(data)[0]

    def add_data(self, data, columns, rows):
        """Adds data from list of lists
        :param data List of lists, containing rows and columns of data
        :param columns Number of columns
        :param rows Number of rows
        """
        # checking that they're all the same length first
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
        """Adds results from a function to the object's results dictionary
        :param function_ran A string describing which function was run
        :param output The output of that function
        """
        self.results.update({function_ran: output})
