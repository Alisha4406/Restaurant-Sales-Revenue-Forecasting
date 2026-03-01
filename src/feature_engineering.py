import pandas as pd

def create_features(df):

    df['Total_Revenue'] = df['Quantity'] * df['Price']

    df['Hour'] = df['Order Time'].dt.hour
    df['Day'] = df['Order Time'].dt.day
    df['Month'] = df['Order Time'].dt.month
    df['Weekday'] = df['Order Time'].dt.weekday
    df['Weekend'] = df['Weekday'].apply(lambda x: 1 if x >= 5 else 0)

    return df


def aggregate_daily(df):

    daily_sales = df.groupby(df['Order Time'].dt.date).agg({
        'Quantity': 'sum',
        'Total_Revenue': 'sum'
    }).reset_index()

    daily_sales.rename(columns={'Order Time': 'Date'}, inplace=True)

    daily_sales['Date'] = pd.to_datetime(daily_sales['Date'])

    daily_sales['Day'] = daily_sales['Date'].dt.day
    daily_sales['Month'] = daily_sales['Date'].dt.month
    daily_sales['Weekday'] = daily_sales['Date'].dt.weekday
    daily_sales['Weekend'] = daily_sales['Weekday'].apply(lambda x: 1 if x >= 5 else 0)

    # 🔥 VERY IMPORTANT FEATURES (increase accuracy)
    daily_sales['Lag_1'] = daily_sales['Total_Revenue'].shift(1)
    daily_sales['Lag_2'] = daily_sales['Total_Revenue'].shift(2)
    daily_sales['Lag_3'] = daily_sales['Total_Revenue'].shift(3)

    daily_sales['Rolling_Mean_3'] = daily_sales['Total_Revenue'].rolling(3).mean()
    daily_sales['Rolling_Mean_7'] = daily_sales['Total_Revenue'].rolling(7).mean()

    daily_sales = daily_sales.dropna()

    return daily_sales