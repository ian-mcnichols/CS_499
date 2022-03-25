from numpy.core.defchararray import index
#import pandas as pd
import numpy as np


class Data:
    def __init__(self, file_name, data_type):
        self.data_type = data_type
        self.data_np = None
        self.results = {}

        # have to have a way to tell if it is gui input
        if file_name == "GUI":
            self.get_data()
        else:
            # Read in the given file
            self.read_data_file(filepath=file_name)

    def read_data_file(self, filepath):
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
        data = data[1:]
        self.data_np = np.dstack(data)[0]

    def get_data(self, data, labels):
        if self.data_type == "Frequency":
            self.expected = data[labels.index("Expected")]
            self.actual = data[labels.index("Actual")]
        elif self.data_type == "Ordinal":
            self.SD = data[labels.index("SD")]
            self.D = data[labels.index("D")]
            self.N = data[labels.index("N")]
            self.A = data[labels.index("A")]
            self.SA = data[labels.index("SA")]
        elif self.data_type == "Interval":
            self.pretest = data[labels.index("Pretest")]
            self.posttest = data[labels.index("Posttest")]
        else:
            raise Exception("Bad data type {}".format(self.data_type))
        return

    def add_result(self, function_ran, output):
        self.results.update({function_ran: output})


if __name__ == '__main__':
    import numpy as np
    my_data = Data("Data/IntervalDataTest.csv", "interval")
