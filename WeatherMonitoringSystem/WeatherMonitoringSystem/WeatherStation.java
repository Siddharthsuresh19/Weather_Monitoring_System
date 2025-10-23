public class WeatherStation {
    public static void main(String[] args) {
        WeatherData weatherData = new WeatherData();

        new CurrentConditionsDisplay(weatherData);
        new StatisticsDisplay(weatherData);
        // FIX: Maintain a reference to the observer we want to remove later
        ForecastDisplay forecastDisplayReference = new ForecastDisplay(weatherData);
        new HeatIndexDisplay(weatherData);

        System.out.println("--- Simulating weather measurements ---");
        weatherData.setMeasurements(26.6f, 65f, 1013.1f);
        weatherData.setMeasurements(27.2f, 70f, 1009.5f);
        weatherData.setMeasurements(25.4f, 90f, 1005.4f);

        System.out.println("\n--- Removing ForecastDisplay and updating again ---");
        // Use the maintained reference for correct removal
        weatherData.removeObserver(forecastDisplayReference); 
        weatherData.setMeasurements(28.0f, 75f, 1016.0f);
    }
}