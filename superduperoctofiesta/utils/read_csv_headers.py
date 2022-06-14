from os import listdir
from os.path import isfile, join
import os
import pandas as pd

# this determines the path for the folder where the csv/xls files are stored
mypath = os.path.join(os.getcwd(), "files_to_read")

# This loops through all of the files in the path you just gave and populates a list in python
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# Loop through the files and read in the csv/header data
header_list = list()
file_list = list()
for rfile in onlyfiles:

    # this gives the full path to the file you are looking for
    full_rfile_path = os.path.join(os.getcwd(),"files_to_read", rfile)

    # This will; use pandas to read in the file that you are looking for and will determine if it needs to skip one row or if the file is a xls or csv
    if rfile.endswith('.csv'):
        file_list.append(rfile)
        header_list.append(pd.read_csv(full_rfile_path, nrows=1, encoding= 'unicode_escape').columns.tolist())

        if len(header_list[len(header_list) - 1]) < 2:
            header_list[len(header_list) - 1] = pd.read_csv(full_rfile_path, nrows=1, encoding='unicode_escape', skiprows=1).columns.tolist()
    elif rfile.endswith('.xls') or rfile.endswith('.xlsx'):
        file_list.append(rfile)
        header_list.append(pd.read_excel(full_rfile_path, nrows=1).columns.tolist())

        if len(header_list[len(header_list) - 1]) < 2:
            header_list[len(header_list) - 1] = pd.read_excel(full_rfile_path, nrows=1, skiprows=1).columns.tolist()
    else:
        continue

# This prints out the filename and header of the files
for cnt, rfile in enumerate(file_list):
    print("FILENAME: {}".format(rfile))
    print("HEADERS: {}".format(header_list[cnt]))