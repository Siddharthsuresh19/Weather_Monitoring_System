// Updated to implement DisplayElement
public class CurrentConditionsDisplay implements Observer, DisplayElement {
    private float temperature;
    private float humidity;
    
    // The Subject reference is no longer stored as it's not strictly needed here

    public CurrentConditionsDisplay(Subject weatherData) {
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

    // Now public as required by the DisplayElement interface
    public void display() { 
        System.out.println("Current conditions: " + temperature + "°C and " + humidity + "% humidity");
    }
}