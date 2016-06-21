from flask import Flask, render_template, request, redirect, url_for
import requests
import pandas
from datetime import datetime
from dateutil.relativedelta import relativedelta
import dill
from sklearn.ensemble import RandomForestRegressor
import urllib2
import json
import collections
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter, date2num
#from bokeh.plotting import figure
#from bokeh.resources import CDN
#from bokeh.embed import file_html, components

#some helper functions

def deg2rad(deg):
  return deg*(3.14/180.)

def calculateMiles(lat1, lon1, lat2, lon2):
  dlon = deg2rad(lon2 - lon1)
  dlat = deg2rad(lat2 - lat1)
  a = (np.sin(dlat/2.))**2 + np.cos(lat1)*np.cos(lat2)*(np.sin(dlon/2.))**2
  c = 2.*np.arctan2(np.sqrt(a), np.sqrt(1-a))
  d = 3961.*c
  return d

# now the flask app
app = Flask(__name__)

#get the features desired for the prediction from the form
#load pickle data
# this includes the DictVectorizer mapping
# and the model
with open('./model_pickled.pkl','rb') as fp:
  vectorizer = dill.load(fp)
  rf = dill.load(fp)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
  return render_template('index.html')

@app.route('/liveFeed2.html',methods=['GET','POST'])
def liveFeed2():
  if request.method == 'GET':
    stationsDict = {}
    htmlinformation = urllib2.urlopen("https://gbfs.citibikenyc.com/gbfs/en/station_information.json")
    data = json.load(htmlinformation)
    data = stations = data['data']
    stations = data['stations']
    for station in stations:
      #stationsDict[station['station_id']] = (station['name'], station['lat'], station['lon'])
      stationsDict[station['station_id']] = station['name']
      #stationsList.append(station['name'])
      #stationsList = sorted(stationsList)

    ## sort the dictionary
    stationsDict = collections.OrderedDict(sorted(stationsDict.iteritems(), key=lambda x: x[1]))

    return render_template('liveFeed2.html', stationsDict = stationsDict)
  else:

    selected_station_id = request.form['option']

    stationDict = {} ## encoding between station id and name
    freeSpotsDict = {}    ## number of free spots
    freeBikesDict = {}   ## number of available spots
    distanceDict = {}

    htmlstatus = urllib2.urlopen("https://gbfs.citibikenyc.com/gbfs/en/station_status.json")
    htmlinformation = urllib2.urlopen("https://gbfs.citibikenyc.com/gbfs/en/station_information.json")
    data = json.load(htmlinformation)
    last_updated = datetime.fromtimestamp(int(data['last_updated']))
    ## make a dictionary translating station id to street name
    data = data['data']
    stations = data['stations']
    for station in stations:
      stationDict[station['station_id']] = (station['name'], station['lat'], station['lon'])

    data = json.load(htmlstatus)
    data = data['data']
    stations = data['stations']
    selected_lat = stationDict[selected_station_id][1]
    selected_lon = stationDict[selected_station_id][2]
    selected_station = stationDict[selected_station_id][0]
    for station in stations:
      d = calculateMiles(selected_lat, selected_lon, stationDict[station['station_id']][1], stationDict[station['station_id']][2])
      if d > 0.5:
        continue
      distanceDict[stationDict[station['station_id']]] = round(d,2)
      freeSpotsDict[stationDict[station['station_id']]] = station['num_docks_available']
      freeBikesDict[stationDict[station['station_id']]] = station['num_bikes_available']

    ## sort and list top ten
    #freeSpotsDict = collections.OrderedDict(sorted(freeSpotsDict.items(), key=lambda x: x[1],reverse=False))
    #freeBikesDict = collections.OrderedDict(sorted(freeBikesDict.items(), key=lambda x: x[1],reverse=False))

    #fig = plt.subplots()
    #templist = []
    #for key in freeSpotsDict:
      #templist.append(freeSpotsDict[key])
      #ax.scatter([last_updated],[freeSpotsDict[key]])
      #plt.plot([last_updated], [freeSpotsDict[key]],'o')
    #p.xaxis.axis_label = "time"
    #p.yaxis.axis_label = "number of free spots"
    #figJS,figDiv = components(p,CDN)
    #plt.legend(freeSpotsDict.keys())
    #ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
    #fig.autofmt_xdate()
    #plt.savefig("./static/test_plot.jpg")
    return render_template('test2.html',distanceDict=distanceDict,freeSpotsDict=freeSpotsDict,freeBikesDict=freeBikesDict, selected_station=selected_station)
    

@app.route('/basicDemographics.html',methods=['GET','POST'])
def basicDemographics():
  return render_template('basicDemographics.html')

@app.route('/test.html',methods=['GET','POST'])
def test():
  return render_template('test.html')

@app.route('/placesGone.html', methods=['GET','POST'])
def placesGone():
  return render_template('placesGone.html')

@app.route('/placesGone_extended.html', methods=['GET','POST'])
def placesGone_extended():
  return render_template('placesGone_extended.html')

@app.route('/topPlaces.html', methods=['GET','POST'])
def topPlaces():
  return render_template('topPlaces.html')

@app.route('/topPlaces_extended.html', methods=['GET','POST'])
def topPlaces_extended():
  return render_template('topPlaces_extended.html')

@app.route('/travelTimes.html', methods=['GET','POST'])
def travelTimes():
  return render_template('travelTimes.html')

@app.route('/travelTimes_extended.html', methods=['GET','POST'])
def travelTimes_extended():
  return render_template('travelTimes_extended.html')

@app.route('/tripDurations.html', methods=['GET','POST'])
def tripDurations():
  return render_template('tripDurations.html')

@app.route('/predictionForm.html', methods=['GET','POST'])
def predictionForm():
  if request.method == 'GET':  
    return render_template('predictionForm.html')
  else:
    #transform data via the dictvectorizer
    X = {'neighborhood': str(request.form['neighborhood']), 'avg_temp': float(request.form['temperature']), 'weekday': str(request.form['dayofweek']), 'PRCP': float(request.form['rain']), 'SNOW': float(request.form['snow'])}
    X = vectorizer.transform(X)

    #then make some predictions based on the input values
    prediction = rf.predict(X)

    #create the template webpage on the fly
    outpage = 'templates/prediction.html'
    with open(outpage,'wb') as fp:
      theline = '<!doctype html> <html lang=\"en\"> <head> <meta charset=\"utf-8\"> <title>CitiBike Helper</title> <link rel=\"stylesheet\" type=\"text/css\" href=\"{{ url_for(\'static\', filename=\'styles/default.css\')}}\"> </head> <body> <div id="header-wrapper"> <div id="header" class="container"> </div>  photo credit: <a href="http://www.flickr.com/photos/36604011@N08/9410440991">Citi bike</a> via <a href="http://photopin.com">photopin</a> <a href="https://creativecommons.org/licenses/by-nd/2.0/">(license)</a> </div>	<div id="wrapper"> <div id="page" class="conainter"> <div id="content"> <div class="title"> <h2>Prediction for the number of riders</h2> <span class="byline">in a day with the specified parameters</span> </div> <font size="+4">'+str(int(round(prediction)))+'</font> <form id=\'userinfoform\' action=\'modelDetails.html\' method=\'get\'> <p> <input class=\"button\" type=\'submit\' name=\'modelDetails\' value=\'Model Details\' /> </p> </form> </body> </html>'
      fp.write(theline)
      
    return render_template('prediction.html')
      
@app.route('/modelDetails.html', methods=['GET','PSOT'])
def modelDetails():
  return render_template('modelDetails.html')

if __name__ == '__main__':
  app.run(port=33507)
