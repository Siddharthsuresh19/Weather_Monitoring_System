// Updated to implement DisplayElement
public class ForecastDisplay implements Observer, DisplayElement {
    private float lastPressure = 1013.25f;
    private float currentPressure;

    public ForecastDisplay(Subject weatherData) {
        weatherData.registerObserver(this);
    }

    public void update(Subject subject) {
        if (subject instanceof WeatherData) {
            WeatherData wd = (WeatherData) subject;
            currentPressure = wd.getPressure();
            display();
            lastPressure = currentPressure; // Update lastPressure AFTER display
        }
    }

    // Now public as required by the DisplayElement interface
    public void display() {
        System.out.print("Forecast: ");
        if (currentPressure > lastPressure) {
            System.out.println("Improving weather on the way!");
        } else if (currentPressure == lastPressure) {
            System.out.println("More of the same.");
        } else {
            System.out.println("Watch out for cooler, rainy weather.");
        }
    }
}