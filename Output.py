import csv
import matplotlib.pyplot as plt


class Output:
    def __init__(self):
        self.field_names = ['Function', 'Value']
        self.functions_ran = []
        self.results = {}

    def add_result(self, function_ran, output):
        self.functions_ran.append(function_ran)
        self.results.update({function_ran: output})

    def build_csv(self, output_file_name):
        if output_file_name.endswith('.csv') is False:
            output_file_name += ".csv"
        with open(output_file_name, 'w', newline='') as csv_file:
            write = csv.DictWriter(csv_file, fieldnames=self.field_names)
            write.writeheader()
            for function in self.functions_ran:
                write.writerow({'Function': function, 'Value': self.results[function]})

    def build_text(self, output_file_name):
        if output_file_name.endswith('.txt') is False:
            output_file_name += ".txt"
        #  Build text

    def save_jpeg(self, output_file_name):  # Static function, outputs one graph at a time. Reliant on plt state
        if output_file_name.endswith('.jpeg') is False:
            output_file_name += ".jpeg"
        plt.savefig(output_file_name)

    def clear(self):
        self.field_names = ['Function', 'Value']
        self.functions_ran = []
        self.results = {}


if __name__ == '__main__':
    # Sample use case
    x = Output()
    x.add_result("mean", 5)
    x.add_result("sd", 10)
    x.add_result("mode", 4)
    x.build_csv('output')
