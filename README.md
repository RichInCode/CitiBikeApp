# CitiBikeApp
An app for viewing Citi Biki sharing data and rider predictions.

https://citibikehelper.herokuapp.com/

# Description
This is the codebase for the Citi Bike Helper App. Note that this app has no official affiliation with Citi Bike and merely represents a body of personal work.  The codebase is for an app to bring some insights into the data on bike rides on the Citi Bike Sharing Program in NYC.  The structure and interaction of the webpage is handled with the Flask web development framework in Python.  The app is built to serve three functions.

1) Provide some visualizations of intesting trends in the data.
2) Provide a prediction engine to estimate the number of riders that are expected in a given day of the week in a specific zone given the local weather information.
3) Connect to the Citi Bike system live API to display nearby stations and a tally of open parking spots and bikes for rental.

# Data Source
This project uses data obtained by Citi Bike (https://www.citibikenyc.com/system-data).  The data was downloaded in monthly chunks with CSV files encoding each ride as a row in the data.  Information for each ride includes the start and stop time of the ride, the bike id, the start and end station ids and names, and the latitidue and longitude of the start and stop stations.  There is also information connected to the individual rider, such as whether or not the rental occurred from someone with a daily pass or a subscription.  If the ride was connected to a subscription, additional rider information is included, such as gender and age.

The ride information was combined with local weather data download from NOAA (https://www.ncdc.noaa.gov/) using the weather station at JFK airport.  The weather data obtained was in the form of CSV files with each row an individual weather reading.  Periodic weather readings occurred throughout the day.

All data processing, cleaning, sorting and slicing has been done using Data Frames in the Pandas package in Python.  To combine rider data with weather data, daily average temperature was used, as well as total daily rainfall.  It is noted that an improvement could be made to use this information more differentially, but that will be left for a later version.

