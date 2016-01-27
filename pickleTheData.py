import glob
import pandas
import datetime
import os
import pickle

filelist = glob.glob("C:\Users\Rich\Documents\GitHub\CitiBikeApp\data*.csv")

bikeData = {}

for item in filelist:
    result = pandas.read_csv(item)
    path, file = os.path.split(item)
    try:
        month = datetime.datetime(int(file[0:4]), int(file[5:7]),1)
    except ValueError:
        month = datetime.datetime(int(file[0:4]), int(file[4:6]),1)

    bikeData[month] = result

pickle.dump(bikeData,"pickled_data.pkl")
