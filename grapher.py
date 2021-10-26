import matplotlib.pyplot as plt
import pandas as pd

def plot(filename):
    df = pd.read_csv(filename, names=['seconds', 'uncorrected', 'corrected'])
    ax = df.plot.scatter(x='seconds',y='uncorrected')
    plt.show()
