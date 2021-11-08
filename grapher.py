import matplotlib.pyplot as plt
import pandas as pd

def plot(filename):
    df = pd.read_csv(filename, names=['seconds', 'uncorrected', 'corrected'])
    ax1 = df.plot(kind='scatter', x='seconds', y='uncorrected',label='uncorrected', color='b')
    ax2 = df.plot(kind='scatter', x='seconds', y='corrected', label='corrected', color='r', ax=ax1)
    plt.show()
