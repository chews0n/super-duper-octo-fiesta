import pandas as pd
from scipy.optimize import curve_fit
import numpy as np
import matplotlib
import math

matplotlib.use('Agg')  # use a different matplotlib backend

import matplotlib.pyplot as plt

plt.ioff()


def exponential_equation(t, qi, di):
    q = qi * np.exp(-di*t)
    return q

def remove_nan_and_zeroes_from_columns(df, variable):
    filtered_df = df[(df[variable].notnull()) & (df[variable] > 0)]
    return filtered_df

def main():
    # this is the start of the main function

    # step 1: read in the csv data from the csv file, the file is located in the same folder and instead of using any arguments, we will just hard code the name of the csv file
    file_path = "master_dataframe_production.csv"

    bakken_data = pd.read_csv(file_path)

    desired_product_type = "Oil"

    bakken_data["ReportDate"] = pd.to_datetime(bakken_data["ReportDate"])

    # we are going to do something called cleaning the data, this will remove things like zeros, NaN values
    bakken_data = remove_nan_and_zeroes_from_columns(bakken_data, desired_product_type)

    unique_well_APIs_list = [33023013930000.0, 33105039980000.0, 33105039970000.0,
                             33013018230000.0, 33013018220000.0]

    for api_idx, api_number in enumerate(unique_well_APIs_list):
        print("api number is: {} {} {}\n".format(api_number, 2, 3))

    print("we are here")

if __name__ == "__main__":
    # This is the start of the running portion of the script executable
    main()

