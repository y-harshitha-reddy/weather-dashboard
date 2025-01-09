import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV Files using paths (replace these paths with the actual paths of your CSV files)
city_attributes = pd.read_csv("city_attributes.csv")
humidity = pd.read_csv("humidity.csv")
pressure = pd.read_csv("pressure.csv")
temperature = pd.read_csv("temperature.csv")
weather_description = pd.read_csv("weather_description.csv")
wind_direction = pd.read_csv("wind_direction.csv")
wind_speed = pd.read_csv("wind_speed.csv")

# Set up Streamlit App
st.title("Weather Monitoring Dashboard")

# Sidebar for selecting city
city_list = city_attributes['City'].unique()
selected_city = st.sidebar.selectbox("Select City", city_list)

# Sidebar for filtering by date range
st.sidebar.header("Filter by Date Range")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime(humidity['datetime'].min()))
end_date = st.sidebar.date_input("End Date", pd.to_datetime(humidity['datetime'].max()))

# Convert datetime columns to datetime type
humidity['datetime'] = pd.to_datetime(humidity['datetime'])
pressure['datetime'] = pd.to_datetime(pressure['datetime'])
temperature['datetime'] = pd.to_datetime(temperature['datetime'])
weather_description['datetime'] = pd.to_datetime(weather_description['datetime'])
wind_direction['datetime'] = pd.to_datetime(wind_direction['datetime'])
wind_speed['datetime'] = pd.to_datetime(wind_speed['datetime'])

# Filter the datasets by selected date range
mask = (humidity['datetime'] >= pd.to_datetime(start_date)) & (humidity['datetime'] <= pd.to_datetime(end_date))
humidity_filtered = humidity.loc[mask]
pressure_filtered = pressure.loc[mask]
temperature_filtered = temperature.loc[mask]
wind_speed_filtered = wind_speed.loc[mask]
wind_direction_filtered = wind_direction.loc[mask]
weather_description_filtered = weather_description.loc[mask]

# Function to plot data
def plot_weather_data(data, ylabel, title):
    fig, ax = plt.subplots()
    ax.plot(data['datetime'], data[selected_city])
    ax.set_xlabel('Datetime')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Display weather data
st.header(f"Weather Data for {selected_city}")

# Show humidity chart
st.subheader("Humidity")
plot_weather_data(humidity_filtered, "Humidity (%)", f"Humidity in {selected_city}")

# Show pressure chart
st.subheader("Pressure")
plot_weather_data(pressure_filtered, "Pressure (hPa)", f"Pressure in {selected_city}")

# Show temperature chart
st.subheader("Temperature")
plot_weather_data(temperature_filtered, "Temperature (°C)", f"Temperature in {selected_city}")

# Show wind speed chart
st.subheader("Wind Speed")
plot_weather_data(wind_speed_filtered, "Wind Speed (m/s)", f"Wind Speed in {selected_city}")

# Show wind direction chart
st.subheader("Wind Direction")
plot_weather_data(wind_direction_filtered, "Wind Direction (°)", f"Wind Direction in {selected_city}")

# Show weather description as a table
st.subheader("Weather Description")
city_weather_description_filtered = weather_description_filtered[['datetime', selected_city]]
st.write(city_weather_description_filtered.set_index('datetime'))

# Sidebar: Display filtered data for each metric
st.sidebar.subheader(f"Filtered Data for {selected_city}")
st.sidebar.write("Humidity Data", humidity_filtered[['datetime', selected_city]])
st.sidebar.write("Pressure Data", pressure_filtered[['datetime', selected_city]])
st.sidebar.write("Temperature Data", temperature_filtered[['datetime', selected_city]])
st.sidebar.write("Wind Speed Data", wind_speed_filtered[['datetime', selected_city]])
st.sidebar.write("Wind Direction Data", wind_direction_filtered[['datetime', selected_city]])
st.sidebar.write("Weather Description", weather_description_filtered[['datetime', selected_city]])
