from numpy.core.defchararray import index


class Data:
    def __init__(self, data_type):
        self.data_type = data_type
        # Ordinal data variables
        self.SD = []
        self.D = []
        self.N = []
        self.A = []
        self.SA = []
        # Frequency data variables
        self.expected = []
        self.actual = []
        # Interval data variables
        self.pretest = []
        self.posttest = []

    def read_data_file(self, filepath):
        with open(filepath, "r") as freq_file:
            # Find file formatting from first line
            sections = freq_file.readline()
            if len(sections.split(",")) > 1:
                delimiter = ","
            elif len(sections.split("\t")) > 1:
                delimiter = "\t"
            else:
                raise Exception("File is not comma separated or tab delineated.")
            # Read in data
            while True:
                next_line = freq_file.readline()
                # Return if reached the end of file
                if not next_line:
                    break
                # Add data to self variables depending on data type
                if self.data_type == "Frequency":
                    self.expected.append(float(next_line.split(delimiter)[1].strip()))
                    self.actual.append(float(next_line.split(delimiter)[2].strip()))
                elif self.data_type == "Ordinal":
                    self.SD.append(float(next_line.split(delimiter)[1].strip()))
                    self.D.append(float(next_line.split(delimiter)[2].strip()))
                    self.N.append(float(next_line.split(delimiter)[3].strip()))
                    self.A.append(float(next_line.split(delimiter)[4].strip()))
                    self.SA.append(float(next_line.split(delimiter)[5].strip()))
                elif self.data_type == "Interval":
                    self.pretest.append(float(next_line.split(delimiter)[1].strip()))
                    self.posttest.append(float(next_line.split(delimiter)[2].strip()))
                else:
                    raise Exception("Bad data type {}".format(self.data_type))
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


if __name__ == '__main__':
    import numpy as np
    my_data = Data("Frequency")
    my_data.read_data_file("/mnt/alam01/slow02/imcnichols/Homework/CS 499/Test_Data/FrequencyDataTest.csv")
    print("my data expected: ", my_data.expected)
    my_data = Data("Frequency")
    my_actual = np.random.rand(100)
    my_expected = np.random.rand(100)
    labels = ["Expected", "Actual"]
    my_data.get_data([my_expected, my_actual], labels)
    print(my_expected == my_data.expected)
    print(my_actual == my_data.actual)
