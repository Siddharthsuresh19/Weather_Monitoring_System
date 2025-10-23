'''import streamlit as st

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
import streamlit as st
import pandas as pd
import numpy as np

# --- Observer Pattern Base Classes ---
class Subject:
    """The Subject interface (Publisher)."""
    def __init__(self):
        # Use session state to store observers persistently
        if 'observers' not in st.session_state:
            st.session_state['observers'] = []
        
    def register(self, observer: 'Observer'):
        if observer not in st.session_state['observers']:
            st.session_state['observers'].append(observer)

    def remove(self, observer: 'Observer'):
        if observer in st.session_state['observers']:
            st.session_state['observers'].remove(observer)

    def notify(self):
        # Iterate over a copy to prevent modification issues during iteration
        for observer in list(st.session_state['observers']):
            observer.update(self)


class Observer:
    """The Observer interface (Subscriber)."""
    def update(self, subject: Subject):
        """Called by the Subject when its state changes."""
        pass


# --- Concrete Subject ---
class WeatherData(Subject):
    """The Concrete Subject that holds the weather state."""
    def __init__(self):
        super().__init__()
        # Initialize weather data attributes in session state
        if 'temperature' not in st.session_state:
            st.session_state['temperature'] = 0.0
            st.session_state['humidity'] = 0.0
            st.session_state['pressure'] = 0.0
        
    @property
    def temperature(self) -> float: return st.session_state['temperature']
    @property
    def humidity(self) -> float: return st.session_state['humidity']
    @property
    def pressure(self) -> float: return st.session_state['pressure']

    def set_measurements(self, temperature: float, humidity: float, pressure: float):
        """Updates measurements and notifies observers."""
        st.session_state['temperature'] = temperature
        st.session_state['humidity'] = humidity
        st.session_state['pressure'] = pressure
        self.notify()


# --- Concrete Observers ---

class CurrentConditionsDisplay(Observer):
    """Displays the current temperature and humidity."""
    def update(self, subject: WeatherData):
        st.info(f"🌡️ **Current Conditions**")
        st.write(f"**Temperature:** {subject.temperature:.1f}°C")
        st.write(f"**Humidity:** {subject.humidity:.1f}%")

class StatisticsDisplay(Observer):
    """Displays the average, maximum, and minimum temperatures over time."""
    def update(self, subject: WeatherData):
        if 'temps_history' not in st.session_state:
            st.session_state['temps_history'] = []

        # Update history with the new temperature
        st.session_state['temps_history'].append(subject.temperature)
        temps = st.session_state['temps_history']
        
        if not temps:
            st.success("📊 **Statistics**\n*No data yet*")
            return

        avg = sum(temps) / len(temps)
        st.success(f"📊 **Statistics**")
        st.write(f"**Avg Temp:** {avg:.1f}°C")
        st.write(f"**Max Temp:** {max(temps):.1f}°C")
        st.write(f"**Min Temp:** {min(temps):.1f}°C")

class ForecastDisplay(Observer):
    """Displays a simple weather forecast based on pressure trend."""
    def update(self, subject: WeatherData):
        if 'last_pressure' not in st.session_state:
            st.session_state['last_pressure'] = 1013.25 # Initial reference pressure

        current_pressure = subject.pressure
        last_pressure = st.session_state['last_pressure']

        if current_pressure > last_pressure:
            forecast = "☀️ Improving weather (Rising Pressure)"
            emoji = "☀️"
        elif current_pressure == last_pressure:
            forecast = "🌤️ No significant change"
            emoji = "🌤️"
        else:
            forecast = "🌧️ Cooler, rainy weather coming (Falling Pressure)"
            emoji = "🌧️"

        st.warning(f"🔮 **Forecast**")
        st.write(f"**Trend:** {forecast}")
        st.write(f"**Last Pressure:** {last_pressure:.1f} hPa")
        
        # Update last pressure for the next calculation
        st.session_state['last_pressure'] = current_pressure


class HeatIndexDisplay(Observer):
    """Displays the calculated Heat Index."""
    
    # Heat Index Calculation (Simplified for this demonstration, based on your Java code's formula)
    def compute_heat_index(self, t: float, rh: float) -> float:
        """Formula from your Java file, adapted to Python."""
        t_c = t  # Temperature in Celsius
        # The complex formula is typically for T in F. 
        # For simplicity and presentation appeal, we'll use a widely accepted approximation for T in Celsius:
        # Heat Index (HI) = T - 0.55 * (1 - 0.01*RH) * (T - 14.5)
        
        # Using the complex formula from the original Java file (which uses T and RH):
        index = (16.923 + (0.185212 * t_c) + (5.37941 * rh) - (0.100254 * t_c * rh)
                + (0.00941695 * (t_c * t_c)) + (0.00728898 * (rh * rh))
                + (0.000345372 * (t_c * t_c * rh)) - (0.000814971 * (t_c * rh * rh))
                + (0.0000102102 * (t_c * t_c * rh * rh)) - (0.000038646 * (t_c * t_c * t_c))
                + (0.0000291583 * (rh * rh * rh)) + (0.00000142721 * (t_c * t_c * t_c * rh))
                + (0.000000197483 * (t_c * rh * rh * rh)) - (0.0000000218429 * (t_c * t_c * t_c * rh * rh))
                + 0.000000000843296 * (t_c * t_c * rh * rh * rh)
                - (0.0000000000481975 * (t_c * t_c * t_c * rh * rh * rh)))
        return float(index)


    def update(self, subject: WeatherData):
        t = subject.temperature
        rh = subject.humidity
        # The complex formula assumes RH is between 0-100.
        heat_index = self.compute_heat_index(t, rh)
        
        st.error(f"🔥 **Heat Index**")
        st.write(f"**Feels Like:** {heat_index:.1f}°C")
        if heat_index > 35:
            st.caption("⚠️ Extreme Caution: Heat Index is High!")
        
# --- Streamlit App Initialization ---
st.set_page_config(layout="wide", page_title="Weather Monitoring System")
st.title("💡 Observer Design Pattern: Weather Monitoring System")
st.markdown("A demonstration of the **Observer Pattern** where **`WeatherData` (Subject)** notifies various **Displays (Observers)** whenever measurements change.")
st.divider()

# --- Initialize or Retrieve Data and Objects ---
# Initialize session state for history if not present
if 'data_history' not in st.session_state:
    st.session_state['data_history'] = pd.DataFrame(columns=["Time", "Temp (°C)", "Humidity (%)", "Pressure (hPa)"])

# Instantiate the Subject and Observers once
@st.cache_resource
def get_weather_system():
    # Only called on first run
    wd = WeatherData()
    displays = {
        'current': CurrentConditionsDisplay(),
        'stats': StatisticsDisplay(),
        'forecast': ForecastDisplay(),
        'heat': HeatIndexDisplay()
    }
    
    # Register all observers with the Subject
    for display in displays.values():
        wd.register(display)
        
    return wd, displays

weather_data, displays = get_weather_system()

# --- GUI: User Input Section ---
st.header("1. Input Weather Measurements")
col1, col2, col3 = st.columns(3)

with col1:
    temp = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0, step=0.1)
with col2:
    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0, step=0.1)
with col3:
    pressure = st.number_input("Pressure (hPa)", min_value=900.0, max_value=1100.0, value=1013.0, step=0.1)

if st.button("Update Weather Data", type="primary", use_container_width=True):
    # 1. Update the Subject's state (which triggers notify())
    weather_data.set_measurements(float(temp), float(humidity), float(pressure))
    
    # 2. Add to history for the table
    new_row = pd.DataFrame([{
        "Time": pd.Timestamp.now().strftime("%H:%M:%S"), 
        "Temp (°C)": float(temp), 
        "Humidity (%)": float(humidity), 
        "Pressure (hPa)": float(pressure)
    }])
    st.session_state['data_history'] = pd.concat([new_row, st.session_state['data_history']], ignore_index=True)
    
    st.balloons()


st.divider()

# --- GUI: Observer Display Section ---
st.header("2. Observer Displays (Automatic Updates)")
st.markdown("When the button is clicked, **`weather_data.notify()`** is called, and all registered observers are automatically updated.")

display_col1, display_col2, display_col3, display_col4 = st.columns(4)

# Force update all displays immediately on load/rerun to show current state
with display_col1:
    displays['current'].update(weather_data)
with display_col2:
    displays['stats'].update(weather_data)
with display_col3:
    displays['forecast'].update(weather_data)
with display_col4:
    displays['heat'].update(weather_data)

st.divider()

# --- GUI: Data History Section ---
st.header("3. Measurement History")
st.dataframe(st.session_state['data_history'], use_container_width=True)'''
import streamlit as st
import pandas as pd
import numpy as np

# --- Observer Pattern Base Classes ---
class Subject:
    """The Subject interface (Publisher)."""
    def __init__(self):
        # Use session state to store observers persistently
        if 'observers' not in st.session_state:
            st.session_state['observers'] = []
        
    def register(self, observer: 'Observer'):
        if observer not in st.session_state['observers']:
            st.session_state['observers'].append(observer)

    def remove(self, observer: 'Observer'):
        if observer in st.session_state['observers']:
            st.session_state['observers'].remove(observer)

    def notify(self):
        # Iterate over a copy to prevent modification issues during iteration
        for observer in list(st.session_state['observers']):
            observer.update(self)


class Observer:
    """The Observer interface (Subscriber)."""
    def update(self, subject: Subject):
        """Called by the Subject when its state changes."""
        pass


# --- Concrete Subject ---
class WeatherData(Subject):
    """The Concrete Subject that holds the weather state."""
    def __init__(self):
        super().__init__()
        # Initialize weather data attributes in session state
        if 'temperature' not in st.session_state:
            st.session_state['temperature'] = 0.0
            st.session_state['humidity'] = 0.0
            st.session_state['pressure'] = 0.0
        
    @property
    def temperature(self) -> float: return st.session_state['temperature']
    @property
    def humidity(self) -> float: return st.session_state['humidity']
    @property
    def pressure(self) -> float: return st.session_state['pressure'] # <-- Fixed Syntax Error

    def set_measurements(self, temperature: float, humidity: float, pressure: float):
        """Updates measurements and notifies observers."""
        st.session_state['temperature'] = temperature
        st.session_state['humidity'] = humidity
        st.session_state['pressure'] = pressure
        self.notify()


# --- Concrete Observers ---

class CurrentConditionsDisplay(Observer):
    """Displays the current temperature and humidity."""
    def update(self, subject: WeatherData):
        st.info(f"🌡️ **Current Conditions**")
        st.write(f"**Temperature:** {subject.temperature:.1f}°C")
        st.write(f"**Humidity:** {subject.humidity:.1f}%")

class StatisticsDisplay(Observer):
    """Displays the average, maximum, and minimum temperatures over time."""
    def update(self, subject: WeatherData):
        if 'temps_history' not in st.session_state:
            st.session_state['temps_history'] = []

        # Update history with the new temperature
        st.session_state['temps_history'].append(subject.temperature)
        temps = st.session_state['temps_history']
        
        if not temps:
            st.success("📊 **Statistics**\n*No data yet*")
            return

        avg = sum(temps) / len(temps)
        st.success(f"📊 **Statistics**")
        st.write(f"**Avg Temp:** {avg:.1f}°C")
        st.write(f"**Max Temp:** {max(temps):.1f}°C")
        st.write(f"**Min Temp:** {min(temps):.1f}°C")

class ForecastDisplay(Observer):
    """Displays a simple weather forecast based on pressure trend."""
    def update(self, subject: WeatherData):
        if 'last_pressure' not in st.session_state:
            st.session_state['last_pressure'] = 1013.25 # Initial reference pressure

        current_pressure = subject.pressure
        last_pressure = st.session_state['last_pressure']

        if current_pressure > last_pressure:
            forecast = "☀️ Improving weather (Rising Pressure)"
            emoji = "☀️"
        elif current_pressure == last_pressure:
            forecast = "🌤️ No significant change"
            emoji = "🌤️"
        else:
            forecast = "🌧️ Cooler, rainy weather coming (Falling Pressure)"
            emoji = "🌧️"

        st.warning(f"🔮 **Forecast**")
        st.write(f"**Trend:** {forecast}")
        st.write(f"**Last Pressure:** {last_pressure:.1f} hPa")
        
        # Update last pressure for the next calculation
        st.session_state['last_pressure'] = current_pressure


class HeatIndexDisplay(Observer):
    """Displays the calculated Heat Index."""
    
    # IMPROVEMENT: Simplified Heat Index Calculation for better clarity in a Celsius presentation
    def compute_heat_index(self, t: float, rh: float) -> float:
        """Approximation of 'Feels Like' temperature (Simplified for Celsius)."""
        if t < 15:
            return t # No significant heat index below 15C
        else:
            # Formula is T_actual + factor_humidity_effect
            # A simple factor to show the effect of humidity on perceived temperature
            humidity_effect_factor = (rh / 100.0) * (t - 15.0) * 0.4 
            return t + humidity_effect_factor


    def update(self, subject: WeatherData):
        t = subject.temperature
        rh = subject.humidity
        heat_index = self.compute_heat_index(t, rh)
        
        st.error(f"🔥 **Heat Index**")
        st.write(f"**Feels Like:** {heat_index:.1f}°C")
        if heat_index > 30: # Lowered threshold for presentation
            st.caption("⚠️ Caution: Heat Index is Elevated!")
        
# --- Streamlit App Initialization ---
st.set_page_config(layout="wide", page_title="Weather Monitoring System")
st.title("💡 Observer Design Pattern: Weather Monitoring System")
st.markdown("A demonstration of the **Observer Pattern** where **`WeatherData` (Subject)** notifies various **Displays (Observers)** whenever measurements change.")
st.divider()

# --- Initialize or Retrieve Data and Objects ---
# Initialize session state for history if not present
if 'data_history' not in st.session_state:
    st.session_state['data_history'] = pd.DataFrame(columns=["Time", "Temp (°C)", "Humidity (%)", "Pressure (hPa)"])

# Instantiate the Subject and Observers once
@st.cache_resource
def get_weather_system():
    # Only called on first run
    wd = WeatherData()
    displays = {
        'current': CurrentConditionsDisplay(),
        'stats': StatisticsDisplay(),
        'forecast': ForecastDisplay(),
        'heat': HeatIndexDisplay()
    }
    
    # Register all observers with the Subject
    for display in displays.values():
        wd.register(display)
        
    return wd, displays

weather_data, displays = get_weather_system()

# --- GUI: User Input Section ---
st.header("1. Input Weather Measurements")
col1, col2, col3 = st.columns(3)

with col1:
    temp = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0, step=0.1)
with col2:
    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0, step=0.1)
with col3:
    pressure = st.number_input("Pressure (hPa)", min_value=900.0, max_value=1100.0, value=1013.0, step=0.1)

if st.button("Update Weather Data", type="primary", use_container_width=True):
    # 1. Update the Subject's state (which triggers notify())
    weather_data.set_measurements(float(temp), float(humidity), float(pressure))
    
    # 2. Add to history for the table
    new_row = pd.DataFrame([{
        "Time": pd.Timestamp.now().strftime("%H:%M:%S"), 
        "Temp (°C)": float(temp), 
        "Humidity (%)": float(humidity), 
        "Pressure (hPa)": float(pressure)
    }])
    st.session_state['data_history'] = pd.concat([new_row, st.session_state['data_history']], ignore_index=True)
    
    st.balloons()


st.divider()

# --- GUI: Observer Display Section ---
st.header("2. Observer Displays (Automatic Updates)")
st.markdown("When the button is clicked, **`weather_data.notify()`** is called, and all registered observers are automatically updated.")

display_col1, display_col2, display_col3, display_col4 = st.columns(4)

# Force update all displays immediately on load/rerun to show current state
with display_col1:
    displays['current'].update(weather_data)
with display_col2:
    displays['stats'].update(weather_data)
with display_col3:
    displays['forecast'].update(weather_data)
with display_col4:
    displays['heat'].update(weather_data)

st.divider()

# --- GUI: Data History Section ---
st.header("3. Measurement History")
st.dataframe(st.session_state['data_history'], use_container_width=True)