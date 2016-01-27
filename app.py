from flask import Flask, render_template, request, redirect, url_for
import requests
import pandas
from datetime import datetime
from dateutil.relativedelta import relativedelta
import dill
from sklearn.ensemble import RandomForestRegressor

#some helper functions


# now the flask app
app = Flask(__name__)
#app.vars = {}
#app.vars['4'] = 'closing price'
#app.vars['5'] = 'volume'
#app.vars['11'] = 'adjusted closing price'

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

@app.route('/placesGone.html', methods=['GET','POST'])
def placesGone():
  return render_template('placesGone.html')

@app.route('/topPlaces.html', methods=['GET','POST'])
def topPlaces():
  return render_template('topPlaces.html')

@app.route('/travelTimes.html', methods=['GET','POST'])
def travelTimes():
  return render_template('travelTimes.html')

@app.route('/travelTimes_extended.html', methods=['GET','POST'])
def travelTimes_extended():
  return render_template('travelTimes_extended.html')

@app.route('/predictionForm.html', methods=['GET','POST'])
def predictionForm():
  if request.method == 'GET':  
    return render_template('predictionForm.html')
  else:
    #transform data via the dictvectorizer
    X = {'neighborhood': str(request.form['neighborhood']), 'avg_temp': float(request.form['temperature']), 'weekday': str(request.form['dayofweek']), 'PRCP': int(request.form['rain']), 'SNOW': int(request.form['snow'])}
    X = vectorizer.transform(X)

    #then make some predictions based on the input values
    prediction = rf.predict(X)

    #create the template webpage on the fly
    outpage = 'templates/prediction.html'
    with open(outpage,'wb') as fp:
      theline = '<!doctype html> <html lang=\"en\"> <head> <meta charset=\"utf-8\"> <title>CitiBike Helper</title> <link rel=\"stylesheet\" type=\"text/css\" href=\"{{ url_for(\'static\', filename=\'styles/style.css\')}}\"> </head> <body> <font size="+4">'+str(int(round(prediction)))+'</font> <form id=\'userinfoform\' action=\'modelDetails.html\' method=\'get\'> <p> <input type=\'submit\' name=\'modelDetails\' value=\'Model Details\' /> </p> </form> </body> </html>'
      fp.write(theline)
      
    return render_template('prediction.html')
      
@app.route('/modelDetails.html', methods=['GET','PSOT'])
def modelDetails():
  return render_template('modelDetails.html')

if __name__ == '__main__':
  app.run(port=33507)
