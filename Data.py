import numpy as np


class Data: # TODO: Find a better way to get the numerical data's rows/cols than try catch blocks
    # Class to read in data from a file or be handed data as a numpy
    # then have the data accessible as a numpy array
    def __init__(self, data_type):
        # sets the data type
        self.data_type = data_type
        self.data = None

    def read_data_file(self, filepath):
        with open(filepath, "r") as freq_file:
            # Find file formatting from first line
            file_lines = freq_file.readlines()
            sections = file_lines[0]
            if len(sections.split(",")) > 1: # if the line is split by commas, csv
                delimiter = ","
            elif len(sections.split("\t")) > 1: # if the line is split by tabs, tdv
                delimiter = "\t"
            else:
                raise Exception("File is not comma separated or tab delineated.")
            # Read in data
            cols = []
            # iterate over the columns to grab the data
            for i in range(len(sections.split(delimiter))):
                try: # append the data if it's all floats
                    random_line = file_lines[1]
                    x = float(random_line.split(delimiter)[i].strip())
                    cols.append(i)
                except ValueError: # if it's a label, skip over
                    continue
            data_array = np.zeros((len(file_lines), len(cols)))
            delete_rows = []
            for i, line in enumerate(file_lines):
                try:
                    line = line.split(delimiter)
                    for j, col in enumerate(cols):
                        data_array[i][j] = line[col]
                except ValueError:
                    delete_rows.append(i)
                    continue
            for delete_row in delete_rows:
                data_array = np.delete(data_array, delete_row, axis=0)
            self.data = data_array
        return

    def add_data(self, new_data):
        new_data = np.array(new_data)
        if self.data is None:
            self.data = new_data
        else:
            if new_data.shape[0] == self.data.shape[0]:
                self.data = np.append(self.data, new_data, axis=1)
            elif new_data.shape[1] == self.data.shape[1]:
                self.data = np.append(self.data, new_data, axis=0)
            else:
                raise Exception("Data to append must match current data's shape on axis 0 or 1")



if __name__ == '__main__':
    # Testing with a file
    my_data = Data("Frequency")
    my_data.add_data(np.random.rand(10, 10))
    print(my_data.data.shape)
    my_data.add_data(np.random.rand(10, 2))
    print(my_data.data.shape)
    my_data.add_data(np.random.rand(1, 12))
    print(my_data.data.shape)
    #my_data.read_data_file("/mnt/alam01/slow02/imcnichols/Homework/CS 499/Test_Data/OrdinalDataTest.csv")
