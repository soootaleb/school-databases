import matplotlib

matplotlib.use('Qt5Agg')

import csv, os
import networkx as nx
import matplotlib.pyplot as plt

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
FILE = os.path.join(DATA_DIR, 'twitter_combined.txt')

# if __name__ == "__main__":
with open(FILE, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter = ' ')

    dataset = [[int(o[0]), int(o[1])] for o in reader]

    G = nx.Graph(dataset)
    
    print("OK")
