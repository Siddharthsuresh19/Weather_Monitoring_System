public class StatisticsDisplay implements Observer {
    private float maxTemp = Float.MIN_VALUE;
    private float minTemp = Float.MAX_VALUE;
    private float tempSum = 0f;
    private int numReadings = 0;

    public StatisticsDisplay(Subject weatherData) {
        weatherData.registerObserver(this);
    }

    public void update(Subject subject) {
        if (subject instanceof WeatherData) {
            WeatherData wd = (WeatherData) subject;
            float temp = wd.getTemperature();
            tempSum += temp;
            numReadings++;
            if (temp > maxTemp) maxTemp = temp;
            if (temp < minTemp) minTemp = temp;
            display();
        }
    }

    private void display() {
        System.out.println("Avg/Max/Min temperature = " + (tempSum / numReadings) + "/" + maxTemp + "/" + minTemp);
    }
}
