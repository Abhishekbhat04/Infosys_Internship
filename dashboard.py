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

# ===============================
# 📊 Global Climate Visualizations (Milestone 3)
# ===============================

st.header("📊 Global Climate Visualizations")

st.subheader("🌡 Global Temperature Trend Over Time")

fig_global_temp = px.line(
    df,
    x="last_updated",
    y="temperature_celsius",
    color="country",
    title="Global Temperature Trend",
    template="plotly_white"
)

st.plotly_chart(fig_global_temp, use_container_width=True)


st.subheader("🌡 Temperature vs Humidity")

fig_temp_humidity = px.scatter(
    df,
    x="temperature_celsius",
    y="humidity",
    color="country",
    size="wind_kph",
    hover_name="location_name",
    title="Temperature vs Humidity Relationship",
    template="plotly_white"
)

st.plotly_chart(fig_temp_humidity, use_container_width=True)


st.subheader("🌧 Rainfall Distribution")

fig_rain = px.histogram(
    df,
    x="precip_mm",
    nbins=40,
    title="Global Rainfall Distribution",
    template="plotly_white"
)

st.plotly_chart(fig_rain, use_container_width=True)

st.markdown("---")


# Sidebar Filter
st.sidebar.header("🔎 Filters")
selected_region = st.sidebar.selectbox(
    "Select Location",
    df["location_name"].unique()
)

filtered_df = df[df["location_name"] == selected_region]
st.sidebar.markdown("---")
st.sidebar.subheader("⬇ Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_climate_data.csv",
    mime="text/csv"
)

# ===============================
# Key Climate Indicators
# ===============================

st.subheader("📊 Key Climate Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🌡 Avg Temp (°C)", f"{filtered_df['temperature_celsius'].mean():.2f}")
col2.metric("💧 Avg Humidity (%)", f"{filtered_df['humidity'].mean():.2f}")
col3.metric("🌧 Total Rainfall (mm)", f"{filtered_df['precip_mm'].sum():.2f}")
col4.metric("💨 Max Wind (kph)", f"{filtered_df['wind_kph'].max():.2f}")

st.markdown("---")

# ===============================
# Monthly Temperature Trend
# ===============================

st.subheader("📈 Monthly Temperature Trend")

temp_trend = filtered_df.groupby("month")["temperature_celsius"].mean().reset_index()

fig1 = px.line(
    temp_trend,
    x="month",
    y="temperature_celsius",
    markers=True,
    template="plotly_white"
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# ===============================
# Correlation Analysis
# ===============================

st.subheader("🔍 Climate Variable Correlation")

corr = correlation_analysis(filtered_df)

fig2 = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="Blues",
    template="plotly_white"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ===============================
# Map Visualization
# ===============================

st.subheader("🗺 Geographic Climate View")

fig3 = px.scatter_mapbox(
    filtered_df,
    lat="latitude",
    lon="longitude",
    color="temperature_celsius",
    size="humidity",
    hover_name="location_name",
    zoom=4,
    mapbox_style="carto-positron",
    color_continuous_scale="Turbo"
)

fig3.update_layout(margin=dict(l=0, r=0, t=30, b=0))

st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ===============================
# Extreme Weather Events
# ===============================

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

# ===============================
# Country Comparison
# ===============================

st.header("🌍 Country Comparison Analysis")

st.subheader("🌡 Average Temperature by Country")

temp_comp = country_temperature_comparison(df).head(10)

fig_temp = px.bar(
    temp_comp,
    x=temp_comp.index,
    y=temp_comp.values,
    template="plotly_white"
)

st.plotly_chart(fig_temp, use_container_width=True)

st.subheader("🌧 Average Rainfall by Country")

rain_comp = country_rainfall_comparison(df).head(10)

fig_rain = px.bar(
    rain_comp,
    x=rain_comp.index,
    y=rain_comp.values,
    template="plotly_white"
)

st.plotly_chart(fig_rain, use_container_width=True)

st.subheader("🔥 Extreme Events by Country")

extreme_comp = country_extreme_events(df).head(10)

fig_extreme = px.bar(
    extreme_comp,
    barmode="group",
    template="plotly_white"
)

st.plotly_chart(fig_extreme, use_container_width=True)

st.markdown("---")

# ===============================
# Global Choropleth Map
# ===============================

st.header("🌍 Global Temperature Choropleth Map")

country_avg_temp = df.groupby("country")["temperature_celsius"].mean().reset_index()

fig_map = px.choropleth(
    country_avg_temp,
    locations="country",
    locationmode="country names",
    color="temperature_celsius",
    color_continuous_scale="Turbo",
    template="plotly_white"
)

st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")

# ===============================
# Insights
# ===============================

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
""")
st.markdown("---")

st.header("🌤 Weather Condition Distribution")

weather_count = df["condition_text"].value_counts().reset_index()
weather_count.columns = ["Condition", "Count"]

fig_weather = px.pie(
    weather_count,
    values="Count",
    names="Condition",
    title="Weather Condition Distribution",
    template="plotly_white"
)

st.plotly_chart(fig_weather, use_container_width=True)