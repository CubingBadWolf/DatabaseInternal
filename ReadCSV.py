import csv

def ReadCSV(file):
    with open(file, 'r') as f:
        output = []
        reader = csv.reader(f)
        for row in reader:
            output.append(row)
        return output