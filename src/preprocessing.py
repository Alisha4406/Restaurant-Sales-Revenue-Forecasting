import pandas as pd

def load_data(path):
    return pd.read_csv(path)

def clean_data(df):
    df = df.dropna()
    df['Order Time'] = pd.to_datetime(df['Order Time'])
    df['Quantity'] = df['Quantity'].astype(int)
    df['Price'] = df['Price'].astype(float)
    return df