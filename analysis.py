import pandas as p

#
def load_data(path="Data/GlobalWeatherRepository.csv"):
    df = pd.read_csv(path)
    df['last_updated'] = pd.to_datetime(df['last_updated'])
    df['month'] = df['last_updated'].dt.month
    df['year'] = df['last_updated'].dt.year
    return df



def statistical_summary(df):
    summary = df[['temperature_celsius',
                  'humidity',
                  'wind_kph',
                  'precip_mm',
                  'pressure_mb']].describe()
    return summary

def correlation_analysis(df):
    return df[['temperature_celsius',
               'humidity',
               'wind_kph',
               'precip_mm',
               'pressure_mb']].corr()



def detect_extremes(df):
    extremes = {}

    extremes['heatwave'] = df[df['temperature_celsius'] >
                              df['temperature_celsius'].quantile(0.95)]

    extremes['coldwave'] = df[df['temperature_celsius'] <
                              df['temperature_celsius'].quantile(0.05)]

    extremes['heavy_rain'] = df[df['precip_mm'] >
                                df['precip_mm'].quantile(0.90)]

    extremes['high_wind'] = df[df['wind_kph'] >
                               df['wind_kph'].quantile(0.95)]

    return extremes



def monthly_trend(df):
    return df.groupby('month')['temperature_celsius'].mean()


def yearly_trend(df):
    return df.groupby('year')['temperature_celsius'].mean()
import pandas as pd

def country_temperature_comparison(df):
    return df.groupby("country")["temperature_celsius"].mean().sort_values(ascending=False)

def country_rainfall_comparison(df):
    return df.groupby("country")["precip_mm"].mean().sort_values(ascending=False)

def country_extreme_events(df):
    heatwave_threshold = df["temperature_celsius"].quantile(0.95)
    coldwave_threshold = df["temperature_celsius"].quantile(0.05)
    rain_threshold = df["precip_mm"].quantile(0.90)

    heatwave = df[df["temperature_celsius"] > heatwave_threshold] \
        .groupby("country").size()

    coldwave = df[df["temperature_celsius"] < coldwave_threshold] \
        .groupby("country").size()

    heavy_rain = df[df["precip_mm"] > rain_threshold] \
        .groupby("country").size()

    result = pd.DataFrame({
        "Heatwave Days": heatwave,
        "Coldwave Days": coldwave,
        "Heavy Rain Days": heavy_rain
    }).fillna(0)

    return result.sort_values("Heatwave Days", ascending=False)