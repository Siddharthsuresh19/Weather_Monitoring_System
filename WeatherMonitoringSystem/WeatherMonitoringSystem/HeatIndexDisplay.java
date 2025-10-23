// Updated to implement DisplayElement
public class HeatIndexDisplay implements Observer, DisplayElement {
    private float heatIndex = 0f;

    public HeatIndexDisplay(Subject weatherData) {
        weatherData.registerObserver(this);
    }

    public void update(Subject subject) {
        if (subject instanceof WeatherData) {
            WeatherData wd = (WeatherData) subject;
            float t = wd.getTemperature();
            float rh = wd.getHumidity();
            heatIndex = computeHeatIndex(t, rh);
            display();
        }
    }

    // Note: The Heat Index formula is highly complex and typically meant for 
    // Farenheit inputs. We keep the original formula for consistency, 
    // but its output is labeled as Celsius in this context.
    private float computeHeatIndex(float t, float rh) {
        double index = (16.923 + (0.185212 * t) + (5.37941 * rh) - (0.100254 * t * rh)
                + (0.00941695 * (t * t)) + (0.00728898 * (rh * rh))
                + (0.000345372 * (t * t * rh)) - (0.000814971 * (t * rh * rh))
                + (0.0000102102 * (t * t * rh * rh)) - (0.000038646 * (t * t * t))
                + (0.0000291583 * (rh * rh * rh)) + (0.00000142721 * (t * t * t * rh))
                + (0.000000197483 * (t * rh * rh * rh)) - (0.0000000218429 * (t * t * t * rh * rh))
                + 0.000000000843296 * (t * t * rh * rh * rh)
                - (0.0000000000481975 * (t * t * t * rh * rh * rh)));
        return (float) index;
    }

    // Now public as required by the DisplayElement interface
    public void display() {
        System.out.println("Heat index is " + heatIndex);
    }
}
