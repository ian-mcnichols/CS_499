import numpy as np


class Data:
    def __init__(self, data_type):
        self.data_type = data_type

    def read_data_file(self, filepath):
        with open(filepath, "r") as freq_file:
            # Find file formatting from first line
            file_lines = freq_file.readlines()
            sections = file_lines[0]
            if len(sections.split(",")) > 1:
                delimiter = ","
            elif len(sections.split("\t")) > 1:
                delimiter = "\t"
            else:
                raise Exception("File is not comma separated or tab delineated.")
            # Read in data
            cols = []
            for i in range(len(sections.split(delimiter))):
                try:
                    random_line = file_lines[1]
                    x = float(random_line.split(delimiter)[i].strip())
                    cols.append(i)
                except ValueError:
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


if __name__ == '__main__':
    # Testing with a file
    my_data = Data("Frequency")
    my_data.read_data_file("/mnt/alam01/slow02/imcnichols/Homework/CS 499/Test_Data/OrdinalDataTest.csv")
    print(my_data.data)
