import csv

def ReadCSV(file):
    '''Function to read data from a csv and return it as a 2 dimensional list'''
    with open(file, 'r') as f:
        output = []
        reader = csv.reader(f)
        for row in reader:
            output.append(row)

        f.close()
        return output