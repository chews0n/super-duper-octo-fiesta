from weather_predictor.data import DownloadWeatherData
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date
import time

from catboost import CatBoostRegressor, Pool
from sklearn.metrics import r2_score, mean_absolute_error

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


    # TODO: Create a training and test (2022 data for test) combined dataframe in pandas, hint: pandas has a function
    #  called "concat" that will allow you to combine multiple dataframes from a list of dataframes, you have the
    #  list of dataframes now in "data"

    df_train = pd.concat(data, ignore_index=True) # in order to get the dataframe without some funky column indices that overwrite one another, use ignore_index=True
    #df_test = pd.read_csv("weather-data-calgary-2022.csv")

    # Will use Islam's original dataframe read in for the test data
    df_test = pd.read_csv("weather-data-calgary-{0}.csv".format(test_year))

    # TODO: You will want to truncate the list to today's date in "df_test", otherwise I believe that most of the data
    #  afterwards is garbage. Use the package "datetime" to determine how many days have passed to today
    #  eg. "datetime.date.today()" and find the delta from Jan. 1 of the "test_year"
    Now = datetime.now()
    StartDate = datetime.strptime(str(test_year) + '-01-01', '%Y-%m-%d')
    Delta = (Now - StartDate)
    print(Delta)


    # TODO: Drop the junk columns from the list above "unused_columns" using pandas function "drop",
    #  looks something like df_test.drop(columns=unused_columns, axis=1) and similar for df_train
    df_test.drop(columns=unused_columns, axis=1, inplace=True)
    df_train.drop(columns=unused_columns, axis=1, inplace=True)

    # TODO: Clean up the dataframes by removing the NaN values in the dataframe and just replace them with zeros,
    #  eg. df_test.fillna(0.0), be sure to fill them with float values (0.0 vs 0 for integers).
    df_train.fillna(0.0, inplace=True)  # fills na or nan with 0.
    df_test.fillna(0.0, inplace=True)

    # TODO: There are some weird text values in some of the columns as well, we'll remove these values and also replace
    #  them with 0.0 using the pandas function "replace" and a regex search function,
    #  eg. df_train.replace(r"[a-zA-Z]", 0.0) where the r before the " refers to regex and the values in the brackets
    #  are the ones we're searching for to remove
    df_train.replace(r"[a-zA-Z]", 0.0)
    df_test.replace(r"[a-zA-Z]", 0.0)


    # TODO: Copy out the "Date/Time" column to separate variable for the test dataframe basically to be used for
    #  plotting later on, then drop the "Date/Time" column from the test/train dataframes
    Date_Time_Test_List = df_test["Date/Time"]
    #df_train.drop(columns=['Date/Test'])
    #df_test.drop(columns=['Date/Test'])
    df_train.drop('Date/Time', inplace=True, axis=1)
    df_test.drop('Date/Time', inplace=True, axis=1)
    print(df_train.head())
    print(df_test.head())
    print(Date_Time_Test_List)

    # TODO: Create another column for the previous day's max temperature in both the test and train dataframes,
    #  hint you will use the column 'Max Temp (°C)' and the "shift" function of the dataframe, note that this is daily data
    train_prev_day_max_temp = df_train['Max Temp (°C)'].shift(periods=1, axis=0, fill_value=0)
    df_train_2 = df_train.assign(PrevDayMaxTemp=train_prev_day_max_temp)
    print(df_train_2.head())

    test_prev_day_max_temp = df_test['Max Temp (°C)'].shift(periods=1, axis=0, fill_value=0)
    df_test_2 = df_test.assign(PrevDayMaxTemp=test_prev_day_max_temp)
    print(df_test_2.head())

    print("hello")
    # TODO: Start building the machine learning model... More on this to come, unless you want to start tackling
    #  this on your own

    # X is usualyl inputs or controls (sometimes this can also be U) and Y are the outputs from the model

    y_test = np.array(df_test_2['Max Temp (°C)'])
    x_test = np.array(df_test_2.drop(['Max Temp (°C)'], axis=1))

    y_train = np.array(df_train_2['Max Temp (°C)'])
    x_train = np.array(df_train_2.drop(['Max Temp (°C)'], axis=1))

    x_col = list(df_train_2.columns.drop(['Max Temp (°C)']))

    # Establish a baseline error to evaluate how well our machine learning model does at predicting the temperature
    # SO, right now we have a training set, a test set (from the current year) and outputs for the related inputs
    # We now need to build a model and for this since it can be difficult to make your own machine learning package
    # we'll use an external library to train and build the model

    # build model
    regressor = CatBoostRegressor(iterations=500, learning_rate=0.1, logging_level='Silent', random_seed=0)

    train_pool = Pool(x_train, y_train)
    regressor.fit(train_pool, eval_set=(x_test, y_test))

    # Predict the results
    y_pred = regressor.predict(x_test)

    print("stopping here....")

    # TODO: Plot and compare the predicted data to the data that actually happened, so this actual data is in the test dataframes. You'll use matplotlib for this and the plot should look something like the image that I am going to put in the folder





if __name__ == "__main__":
    main()
