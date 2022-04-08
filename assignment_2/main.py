from weather_predictor.data import DownloadWeatherData

import pandas as pd

unused_columns = ['Longitude (x)', 'Latitude (y)', 'Climate ID',
                  'Station Name', 'Data Quality', 'Max Temp Flag',
                  'Min Temp Flag', 'Mean Temp Flag', 'Heat Deg Days Flag',
                  'Cool Deg Days Flag', 'Total Rain Flag', 'Total Snow Flag',
                  'Total Precip Flag', 'Snow on Grnd Flag', 'Dir of Max Gust Flag',
                  'Spd of Max Gust Flag', 'Total Rain (mm)', 'Total Snow (cm)',
                  'Heat Deg Days (°C)', 'Cool Deg Days (°C)', 'Dir of Max Gust (10s deg)', 'Spd of Max Gust (km/h)']

def main():
    weather_data = DownloadWeatherData()
    weather_data.download_data()

    start_year = 2010
    end_year = 2022
    data = list()

    for i in range(start_year, end_year+1):
        data.append(pd.read_csv("weather-data-calgary-{0}.csv".format(i)))

    print("hello")

if __name__ == "__main__":
    main()
