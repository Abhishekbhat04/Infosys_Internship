import streamlit as st
import pandas as pd
import plotly.express as px
from analysis import load_data, correlation_analysis
from analysis import country_temperature_comparison, country_rainfall_comparison, country_extreme_events

st.set_page_config(page_title="ClimateScope",
                   page_icon="🌍",
                   layout="wide")

st.markdown("""
<style>
.main { background-color: #f5f7fa; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }
div[data-testid="metric-container"] {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

st.title("🌍 ClimateScope Analytics Dashboard")
st.markdown("### Weather Insights & Regional Climate Trends")
st.markdown("---")

df = load_data()

st.sidebar.header("🔎 Filters")
selected_region = st.sidebar.selectbox(
    "Select Location",
    df["location_name"].unique()
)

filtered_df = df[df["location_name"] == selected_region]

st.subheader("📊 Key Climate Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🌡 Avg Temp (°C)", f"{filtered_df['temperature_celsius'].mean():.2f}")
col2.metric("💧 Avg Humidity (%)", f"{filtered_df['humidity'].mean():.2f}")
col3.metric("🌧 Total Rainfall (mm)", f"{filtered_df['precip_mm'].sum():.2f}")
col4.metric("💨 Max Wind (kph)", f"{filtered_df['wind_kph'].max():.2f}")

st.markdown("---")

st.subheader("📈 Monthly Temperature Trend")

temp_trend = filtered_df.groupby("month")["temperature_celsius"].mean().reset_index()

fig1 = px.line(temp_trend,
               x="month",
               y="temperature_celsius",
               markers=True,
               template="plotly_white")

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

st.subheader("🔍 Climate Variable Correlation")

corr = correlation_analysis(filtered_df)

fig2 = px.imshow(corr,
                 text_auto=True,
                 color_continuous_scale="Blues",
                 template="plotly_white")

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

st.subheader("🗺 Geographic Climate View")

fig3 = px.scatter_mapbox(filtered_df,
                         lat="latitude",
                         lon="longitude",
                         color="temperature_celsius",
                         size="humidity",
                         hover_name="location_name",
                         zoom=4,
                         mapbox_style="carto-positron",
                         color_continuous_scale="Turbo")

fig3.update_layout(margin=dict(l=0, r=0, t=30, b=0))
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

st.subheader("⚠ Extreme Weather Events")

heatwaves = len(filtered_df[
    filtered_df["temperature_celsius"] >
    filtered_df["temperature_celsius"].quantile(0.95)
])

coldwaves = len(filtered_df[
    filtered_df["temperature_celsius"] <
    filtered_df["temperature_celsius"].quantile(0.05)
])

heavy_rain = len(filtered_df[
    filtered_df["precip_mm"] >
    filtered_df["precip_mm"].quantile(0.90)
])

high_wind = len(filtered_df[
    filtered_df["wind_kph"] >
    filtered_df["wind_kph"].quantile(0.95)
])

col1, col2, col3, col4 = st.columns(4)

col1.metric("🔥 Heatwave Days", heatwaves)
col2.metric("❄ Coldwave Days", coldwaves)
col3.metric("🌧 Heavy Rain Days", heavy_rain)
col4.metric("💨 High Wind Days", high_wind)

st.markdown("---")

st.header("🌍 Country Comparison Analysis")

st.subheader("🌡 Average Temperature by Country")
temp_comp = country_temperature_comparison(df).head(10)
fig_temp = px.bar(temp_comp,
                  x=temp_comp.index,
                  y=temp_comp.values,
                  template="plotly_white")
st.plotly_chart(fig_temp, use_container_width=True)

st.subheader("🌧 Average Rainfall by Country")
rain_comp = country_rainfall_comparison(df).head(10)
fig_rain = px.bar(rain_comp,
                  x=rain_comp.index,
                  y=rain_comp.values,
                  template="plotly_white")
st.plotly_chart(fig_rain, use_container_width=True)

st.subheader("🔥 Extreme Events by Country")
extreme_comp = country_extreme_events(df).head(10)
fig_extreme = px.bar(extreme_comp,
                     barmode="group",
                     template="plotly_white")
st.plotly_chart(fig_extreme, use_container_width=True)

st.markdown("---")

st.header("🌍 Country vs Country Comparison")

countries = sorted(df["country"].unique())

col1, col2 = st.columns(2)

with col1:
    country1 = st.selectbox("Select First Country", countries)

with col2:
    country2 = st.selectbox(
        "Select Second Country",
        [c for c in countries if c != country1]
    )

df1 = df[df["country"] == country1]
df2 = df[df["country"] == country2]

comparison_data = pd.DataFrame({
    "Metric": ["Avg Temp", "Avg Humidity", "Avg Wind", "Avg Rainfall"],
    country1: [
        df1["temperature_celsius"].mean(),
        df1["humidity"].mean(),
        df1["wind_kph"].mean(),
        df1["precip_mm"].mean()
    ],
    country2: [
        df2["temperature_celsius"].mean(),
        df2["humidity"].mean(),
        df2["wind_kph"].mean(),
        df2["precip_mm"].mean()
    ]
})

fig_compare = px.bar(comparison_data,
                     x="Metric",
                     y=[country1, country2],
                     barmode="group",
                     template="plotly_white")

st.plotly_chart(fig_compare, use_container_width=True)

st.markdown("---")

st.header("📈 Time-Series Analysis")

col1, col2 = st.columns(2)

with col1:
    ts_country1 = st.selectbox("Country 1 Trend", countries, key="ts1")

with col2:
    ts_country2 = st.selectbox(
        "Country 2 Trend",
        [c for c in countries if c != ts_country1],
        key="ts2"
    )

df_ts1 = df[df["country"] == ts_country1]
df_ts2 = df[df["country"] == ts_country2]

ts1 = df_ts1.groupby("last_updated")["temperature_celsius"].mean().reset_index()
ts2 = df_ts2.groupby("last_updated")["temperature_celsius"].mean().reset_index()

ts1["Country"] = ts_country1
ts2["Country"] = ts_country2

combined_ts = pd.concat([ts1, ts2])

fig_ts = px.line(combined_ts,
                 x="last_updated",
                 y="temperature_celsius",
                 color="Country",
                 template="plotly_white")

st.plotly_chart(fig_ts, use_container_width=True)

st.markdown("---")

st.header("🌍 Global Temperature Choropleth Map")

country_avg_temp = df.groupby("country")["temperature_celsius"].mean().reset_index()

fig_map = px.choropleth(country_avg_temp,
                        locations="country",
                        locationmode="country names",
                        color="temperature_celsius",
                        color_continuous_scale="Turbo",
                        template="plotly_white")

st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")

st.header("🧠 Key Analytical Insights")

country_avg_rain = df.groupby("country")["precip_mm"].mean().reset_index()

hottest_country = country_avg_temp.sort_values(
    "temperature_celsius", ascending=False).iloc[0]

rainiest_country = country_avg_rain.sort_values(
    "precip_mm", ascending=False).iloc[0]

total_heatwaves = len(df[df["temperature_celsius"] >
                          df["temperature_celsius"].quantile(0.95)])

total_heavy_rain = len(df[df["precip_mm"] >
                           df["precip_mm"].quantile(0.90)])

st.success(f"""
• 🌡 Hottest country on average: **{hottest_country['country']}**
  ({hottest_country['temperature_celsius']:.2f}°C)

• 🌧 Rainiest country on average: **{rainiest_country['country']}**
  ({rainiest_country['precip_mm']:.2f} mm)

• 🔥 Total heatwave days detected: **{total_heatwaves}**

• 🌧 Total heavy rainfall days detected: **{total_heavy_rain}**

• 📈 Seasonal and time-series analysis reveal clear climatic variations across regions.
""")