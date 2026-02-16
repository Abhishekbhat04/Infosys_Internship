import pandas as pd
df = pd.read_csv("Data/GlobalWeatherRepository.csv")
print("First 5 Rows:")
print(df.head())
print("\nColumn Names:")
print(df.columns)
print("\nDataset Info:")
print(df.info())
print("\nSummary Statistics:")
print(df.describe())

df['last_updated'] = pd.to_datetime(df['last_updated'])

df['year'] = df['last_updated'].dt.year
df['month'] = df['last_updated'].dt.month

print("\nAfter Date Conversion:")
print(df[['last_updated', 'year', 'month']].head())


monthly_avg = df.groupby(['country', 'year', 'month']).agg({
    'temperature_celsius': 'mean',
    'precip_mm': 'mean',
    'wind_kph': 'mean',
    'humidity': 'mean'
}).reset_index()

print("\nMonthly Aggregated Data:")
print(monthly_avg.head())
