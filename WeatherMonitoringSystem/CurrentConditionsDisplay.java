public class CurrentConditionsDisplay implements Observer {
    private float temperature;
    private float humidity;
    private Subject weatherData;

    public CurrentConditionsDisplay(Subject weatherData) {
        this.weatherData = weatherData;
        weatherData.registerObserver(this);
    }

    public void update(Subject subject) {
        if (subject instanceof WeatherData) {
            WeatherData wd = (WeatherData) subject;
            this.temperature = wd.getTemperature();
            this.humidity = wd.getHumidity();
            display();
        }
    }

    private void display() {
        System.out.println("Current conditions: " + temperature + "°C and " + humidity + "% humidity");
    }
}
