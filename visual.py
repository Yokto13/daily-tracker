import matplotlib.pyplot as plt
import csv

data = []
CSV_PATH = "myresults.csv"

with open(CSV_PATH) as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        data.append(row)

keys = data[0].keys()

x = list(range(len(data)))

def average(l):
    return sum(l) / len(l)

for k in keys:
    y = []
    if k == "timestamp":
        continue
    for row in data:
        n = float(row[k])
        y.append(n)
    print(k)
    print("average", average(y))
    plt.plot(x, y, 'ro')
    plt.savefig(f"plots/{k}.png")
    plt.clf()

