import pandas as pd

def plot(filename):
    df = pd.read_csv(filename)
    print(df[0])