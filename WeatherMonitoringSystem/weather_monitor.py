import streamlit as st

# --- Observer pattern base classes ---
class Subject:
    def __init__(self):
        self._observers = []

    def register(self, observer):
        self._observers.append(observer)

    def remove(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)


class Observer:
    def update(self, subject):
        pass


# --- Concrete Subject ---
class WeatherData(Subject):
    def __init__(self):
        super().__init__()
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0

    def set_measurements(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.notify()


# --- Concrete Observers ---
class CurrentConditionsDisplay(Observer):
    def update(self, subject):
        st.info(f"🌡️ Current: {subject.temperature}°C, Humidity: {subject.humidity}%")

class StatisticsDisplay(Observer):
    def __init__(self):
        self.temps = []

    def update(self, subject):
        self.temps.append(subject.temperature)
        avg = sum(self.temps) / len(self.temps)
        st.success(f"📊 Avg/Max/Min Temp: {avg:.1f}/{max(self.temps)}/{min(self.temps)}")

class ForecastDisplay(Observer):
    def __init__(self):
        self.last_pressure = 1013.25

    def update(self, subject):
        current = subject.pressure
        if current > self.last_pressure:
            forecast = "☀️ Improving weather"
        elif current == self.last_pressure:
            forecast = "🌤️ No change"
        else:
            forecast = "🌧️ Rainy weather coming"
        self.last_pressure = current
        st.warning(f"🔮 Forecast: {forecast}")


# --- Streamlit App ---
st.title("🌦️ Weather Monitoring System (Observer Pattern)")
st.caption("Demonstrates Observer Design Pattern with dynamic updates")

# Initialize WeatherData and displays
weather_data = WeatherData()
current_display = CurrentConditionsDisplay()
stats_display = StatisticsDisplay()
forecast_display = ForecastDisplay()

weather_data.register(current_display)
weather_data.register(stats_display)
weather_data.register(forecast_display)

# User Input
temp = st.slider("Temperature (°C)", 0, 50, 25)
humidity = st.slider("Humidity (%)", 0, 100, 60)
pressure = st.slider("Pressure (hPa)", 900, 1100, 1013)

if st.button("Update Weather Data"):
    weather_data.set_measurements(temp, humidity, pressure)