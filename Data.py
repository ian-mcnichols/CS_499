from numpy.core.defchararray import index
import pandas as pd
import numpy as np


class Data:
    def __init__(self, file_name):
        # Initialize to none
        self.data_type = "Null"
        self.data_np = None
        self.results = {}
        # have to have a way to tell it it is gui input
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
            # Determine data type
            if sections.split(delimiter)[0].strip() == "Sample #":
                self.data_type = "Frequency"
            elif sections.split(delimiter)[0].strip() == "Subject ID":
                self.data_type = "Interval"
            elif sections.split(delimiter)[0].strip() == "Question #":
                self.data_type = "Ordinal"
            else:
                raise Exception("File is not in expected format")
            file.close()
        # Read in data as a numpy array
        self.data_np = np.genfromtxt(filepath, dtype=None, delimiter=', ', skip_header=1, encoding=None)
        # Set names for columns, striping white space
        self.data_np.dtype.names = [x.strip() for x in sections.split(delimiter)]

        return

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
    my_data = Data("IntervalDataTest.csv")
    print(my_data.data_np)
    print(my_data.data_type)
    print(my_data.data_np.dtype.names)
    print(my_data.data_np[my_data.data_np.dtype.names[1]])
    print(my_data.data_np['Pretest'])
