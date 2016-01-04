import glob
import pandas

#weather data
weather_df = pandas.read_csv("C:\Users\Rich\Documents\GitHub\CitiBikeApp\data\jkf_temp_data.txt")

filelist = glob.glob("C:\Users\Rich\Documents\GitHub\CitiBikeApp\data\*.csv")


df = pandas.read_csv(filelist[0])
