from weather_predictor.data import DownloadWeatherData


def main():
    weather_data = DownloadWeatherData()
    weather_data.download_data()


if __name__ == "__main__":
    main()
