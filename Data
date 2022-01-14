class Data:
    def __init__(self, filepath, data_type):
        self.filepath = filepath
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

    def read_data(self):
        with open(self.filepath, "r") as freq_file:
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


if __name__ == '__main__':
    my_data = Data("//alam01/alam01/slow02/imcnichols/Homework/CS 499/Test_Data/FrequencyDataTest.csv",
                   "Frequency")
    my_data.read_data()
    print("my data expected: ", my_data.expected)
