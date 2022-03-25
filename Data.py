from numpy.core.defchararray import index
import pandas as pd
import numpy as np


class Data:
    def __init__(self, file_name, data_type):
        self.data_type = data_type
        self.data_np = None
        self.results = {}
        if file_name != "GUI":
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
        return

    def get_data(self, data):
        if self.data_type.lower() == "interval":
            print("getting intervals")
            self.data_np = np.dstack([x for x in data])[0]
        elif self.data_type.lower() == "ordinal":
            print("getting ordinals")
            self.data_np = np.stack([x for x in data])
        else:
            raise Exception("Bad data type {}".format(self.data_type))
        print("my data:", self.data_np)
        return

    def add_result(self, function_ran, output):
        self.results.update({function_ran: output})


if __name__ == '__main__':
    import numpy as np
    my_data = Data("GUI", "interval")
    my_data.get_data([[1, 1, 1, 1, 1], [1, 2, 1, 2, 1]])
