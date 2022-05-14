from weather_predictor.data import DownloadWeatherData
import pandas as pd
import numpy as np
from IPython.display import display
from datetime import datetime, timedelta
from catboost import CatBoostRegressor, Pool
from sklearn.metrics import r2_score, mean_absolute_error
pd.options.display.max_columns = None
#print.datetime.now() + timedelta(days=5,hours=-5)


unused_columns = ['Longitude (x)', 'Latitude (y)', 'Climate ID',
                  'Station Name', 'Data Quality', 'Max Temp Flag',
                  'Min Temp Flag', 'Mean Temp Flag', 'Heat Deg Days Flag',
                  'Cool Deg Days Flag', 'Total Rain Flag', 'Total Snow Flag',
                  'Total Precip Flag', 'Snow on Grnd Flag', 'Dir of Max Gust Flag',
                  'Spd of Max Gust Flag', 'Total Rain (mm)', 'Total Snow (cm)',
                  'Heat Deg Days (°C)', 'Cool Deg Days (°C)', 'Dir of Max Gust (10s deg)', 'Spd of Max Gust (km/h)']

def main():
    global unused_columns

    weather_data = DownloadWeatherData()
    weather_data.download_data()

    start_year = 2010
    end_year = 2021
    test_year = 2022
    data = list()

    for i in range(start_year, end_year + 1):  #change made to exclude the year 2022 from the training data
        data.append(pd.read_csv("weather-data-calgary-{0}.csv".format(i)))

    #print("hello")

    # TODO: Create a training and test (2022 data for test) combined dataframe in pandas, hint: pandas has a function
    #  called "concat" that will allow you to combine multiple dataframes from a list of dataframes, you have the
    #  list of dataframes now in "data"

    df_train = pd.concat(data, ignore_index=True) # in order to get the dataframe without some funky column indices that overwrite one another, use ignore_index=True

    # Will use Islam's original dataframe read in for the test data
    df_test = pd.read_csv("weather-data-calgary-{0}.csv".format(test_year))
    #print(df_test)
    #df_test.head() #why this function did not work
    #display(df_test)
    # TODO: You will want to truncate the list to today's date in "df_test", otherwise I believe that most of the data
    #  afterwards is garbage. Use the package "datetime" to determine how many days have passed to today
    #  eg. "datetime.date.today()" and find the delta from Jan. 1 of the "test_year"
    now = datetime.now()
    start_test_year = datetime(2022, 1, 1)
    days_to_truncate = (now - start_test_year).days
    #print(days_to_truncate)

    # TODO: Drop the junk columns from the list above "unused_columns" using pandas function "drop",
    #  looks something like df_test.drop(columns=unused_columns, axis=1) and similar for df_train
    df_test.drop(columns=unused_columns, axis=1, inplace=True)
    df_train.drop(columns=unused_columns, axis=1, inplace=True)
    #print(df_train)
    # TODO: Clean up the dataframes by removing the NaN values in the dataframe and just replace them with zeros,
    #  eg. df_test.fillna(0.0), be sure to fill them with float values (0.0 vs 0 for integers).
    df_test.fillna(0.0, inplace=True)
    df_train.fillna(0.0, inplace=True)
    #df_train.to_csv("train.csv")
    # TODO: There are some weird text values in some of the columns as well, we'll remove these values and also replace
    #  them with 0.0 using the pandas function "replace" and a regex search function,
    #  eg. df_train.replace(r"[a-zA-Z]", 0.0) where the r before the " refers to regex and the values in the brackets
    #  are the ones we're searching for to remove
    df_train.replace(r"[a-zA-Z", 0.0)
    df_test.replace(r"[a-zA-Z", 0.0)
    #how do we know that there are some weired text values???


    # TODO: Copy out the "Date/Time" column to separate variable for the test dataframe basically to be used for
    #  plotting later on, then drop the "Date/Time" column from the test/train dataframes
    date_time_copy = df_test["Date/Time"]
    df_train.drop("Date/Time", axis=1, inplace=True)
    df_test.drop("Date/Time", axis=1, inplace=True)
    #print(df_train.head())

    # TODO: Create another column for the previous day's max temperature in both the test and train dataframes,
    #  hint you will use the column 'Max Temp (°C)' and the "shift" function of the dataframe, note that this is daily data
    train_prev_day_max_temp = df_train['Max Temp (°C)'].shift(periods=1, axis=0, fill_value=0)
    df_train2 = df_train.assign(prevdaymaxtemp=train_prev_day_max_temp)
    print(df_train2)
    test_prev_day_max_temp =df_test['Max Temp (°C)'].shift(periods=1, axis=0, fill_value=0)
    df_test2= df_test.assign(prevdaymaxtemp=test_prev_day_max_temp)
    print(df_test2)

    # TODO: Start building the machine learning model... More on this to come, unless you want to start tackling
    #  this on your own

    # X is inputs or controls and Y are the outputs from the model
    x_test=np.array(df_test2.drop(['Max Temp (°C)']), axis=1)
    y_test=np.array(df_test2['Max Temp (°C)'])

    x_train =np.array(df_train2['Max Temp (°C)'])
    y_train= np.array(df_train2.drop(['Max Temp (°C)']))

    #build model
    regressor = CatBoostRegressor(iterations=500, learning_rate=0.1, logging_level='Silent', random_seed=0)

    train_pool = pool(x_train,y_train)
if __name__ == "__main__":
    main()