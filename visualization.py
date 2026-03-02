import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")


def plot_temperature_trend(monthly_data):
    plt.figure()
    monthly_data.plot()
    plt.title("Average Monthly Temperature")
    plt.xlabel("Month")
    plt.ylabel("Temperature (°C)")
    plt.tight_layout()
    plt.show()


def plot_correlation_heatmap(corr):
    plt.figure()
    sns.heatmap(corr, annot=True)
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.show()


def plot_precip_distribution(df):
    plt.figure()
    sns.histplot(df['precip_mm'], kde=True)
    plt.title("Precipitation Distribution")
    plt.tight_layout()
    plt.show()


def plot_extreme_events(df):
    plt.figure()
    plt.scatter(df['temperature_celsius'], df['precip_mm'])
    plt.xlabel("Temperature")
    plt.ylabel("Precipitation")
    plt.title("Extreme Weather Scatter")
    plt.tight_layout()
    plt.show()