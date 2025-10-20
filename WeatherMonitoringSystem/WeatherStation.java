public class WeatherStation {
    public static void main(String[] args) {
        WeatherData weatherData = new WeatherData();

        new CurrentConditionsDisplay(weatherData);
        new StatisticsDisplay(weatherData);
        new ForecastDisplay(weatherData);
        new HeatIndexDisplay(weatherData);

        System.out.println("--- Simulating weather measurements ---");
        weatherData.setMeasurements(26.6f, 65f, 1013.1f);
        weatherData.setMeasurements(27.2f, 70f, 1009.5f);
        weatherData.setMeasurements(25.4f, 90f, 1005.4f);

        System.out.println("--- Removing ForecastDisplay and updating again ---");
        weatherData.removeObserver(new ForecastDisplay(weatherData)); // Or maintain reference
        weatherData.setMeasurements(28.0f, 75f, 1016.0f);
    }
}
