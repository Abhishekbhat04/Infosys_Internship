import streamlit as st
import pandas as pd
import plotly.express as px
from analysis import load_data, correlation_analysis
from analysis import country_temperature_comparison, country_rainfall_comparison, country_extreme_events

# 🔐 AUTH IMPORTS
from auth import init_user_file, register_user, login_user

# Initialize user file
init_user_file()

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ===============================
# 🔐 LOGIN / SIGNUP UI
# ===============================

st.title("🌍 ClimateScope Login")

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.success("Logged in successfully")
            st.rerun()
        else:
            st.error("Invalid credentials")

elif choice == "Sign Up":
    new_user = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")

    if st.button("Create Account"):
        success, msg = register_user(new_user, new_password)
        if success:
            st.success(msg)
        else:
            st.error(msg)


# ===============================
# 🌍 MAIN DASHBOARD (PROTECTED)
# ===============================

if st.session_state.logged_in:

    st.set_page_config(
        page_title="ClimateScope",
        page_icon="🌍",
        layout="wide"
    )

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.sidebar.success("Logged In ✅")

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
    # 📊 Global Climate Visualizations
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
        template="plotly_white"
    )
    st.plotly_chart(fig_temp_humidity, use_container_width=True)

    st.subheader("🌧 Rainfall Distribution")

    fig_rain = px.histogram(
        df,
        x="precip_mm",
        nbins=40,
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
    # 📊 Key Metrics
    # ===============================

    st.subheader("📊 Key Climate Indicators")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🌡 Avg Temp (°C)", f"{filtered_df['temperature_celsius'].mean():.2f}")
    col2.metric("💧 Avg Humidity (%)", f"{filtered_df['humidity'].mean():.2f}")
    col3.metric("🌧 Total Rainfall (mm)", f"{filtered_df['precip_mm'].sum():.2f}")
    col4.metric("💨 Max Wind (kph)", f"{filtered_df['wind_kph'].max():.2f}")

    st.markdown("---")

    # ===============================
    # 📈 Monthly Trend
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
    # 🔍 Correlation
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
    # 🗺 Map
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
        mapbox_style="carto-positron"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # ===============================
    # ⚠ Extreme Events
    # ===============================

    st.subheader("⚠ Extreme Weather Events")

    heatwaves = len(filtered_df[filtered_df["temperature_celsius"] > filtered_df["temperature_celsius"].quantile(0.95)])
    coldwaves = len(filtered_df[filtered_df["temperature_celsius"] < filtered_df["temperature_celsius"].quantile(0.05)])
    heavy_rain = len(filtered_df[filtered_df["precip_mm"] > filtered_df["precip_mm"].quantile(0.90)])
    high_wind = len(filtered_df[filtered_df["wind_kph"] > filtered_df["wind_kph"].quantile(0.95)])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🔥 Heatwave Days", heatwaves)
    col2.metric("❄ Coldwave Days", coldwaves)
    col3.metric("🌧 Heavy Rain Days", heavy_rain)
    col4.metric("💨 High Wind Days", high_wind)

    st.markdown("---")

    # ===============================
    # 🌍 Country Comparison
    # ===============================

    st.header("🌍 Country Comparison Analysis")

    temp_comp = country_temperature_comparison(df).head(10)
    st.plotly_chart(px.bar(temp_comp, x=temp_comp.index, y=temp_comp.values), use_container_width=True)

    rain_comp = country_rainfall_comparison(df).head(10)
    st.plotly_chart(px.bar(rain_comp, x=rain_comp.index, y=rain_comp.values), use_container_width=True)

    extreme_comp = country_extreme_events(df).head(10)
    st.plotly_chart(px.bar(extreme_comp, barmode="group"), use_container_width=True)

    st.markdown("---")

    # ===============================
    # 🌍 Choropleth
    # ===============================

    st.header("🌍 Global Temperature Choropleth Map")

    country_avg_temp = df.groupby("country")["temperature_celsius"].mean().reset_index()

    fig_map = px.choropleth(
        country_avg_temp,
        locations="country",
        locationmode="country names",
        color="temperature_celsius",
        color_continuous_scale="Turbo"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("---")

    # ===============================
    # 🧠 Insights
    # ===============================

    st.header("🧠 Key Analytical Insights")

    country_avg_rain = df.groupby("country")["precip_mm"].mean().reset_index()

    hottest_country = country_avg_temp.sort_values("temperature_celsius", ascending=False).iloc[0]
    rainiest_country = country_avg_rain.sort_values("precip_mm", ascending=False).iloc[0]

    st.success(f"""
    • 🌡 Hottest country: {hottest_country['country']} ({hottest_country['temperature_celsius']:.2f}°C)
    • 🌧 Rainiest country: {rainiest_country['country']} ({rainiest_country['precip_mm']:.2f} mm)
    """)