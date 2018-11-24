from flask import Flask
from flask import render_template
from flask import request
import pyowm
import os
import json

owm = pyowm.OWM(API_key = os.environ["APIKEY"])
def conversionTemp(kelvin):
	celsius = kelvin-273.15
	return celsius
def compareTemperature(temp1, temp2):
	if (temp1 > temp2):
		return temp1
	elif (temp2 > temp1):
		return temp2
	else: 
		return (temp1, temp2)
observation = owm.weather_at_place("London")
print (observation)
app = Flask(__name__)
@app.route ("/")
def index():
	return render_template ("index.html")

@app.route("/ort", methods=["GET", "POST"])
def orte():
	ort = request.form ["ort"]
	ort.replace (" ", "")
	ortsliste = ort.split(", ")
	for city in ortsliste:
		observation = owm.weather_at_place(city)
		w = observation.get_weather() 
		t1 = w.get_temperature()
		
		for i in range(ortsliste.index(city)+1, len(ortsliste)):
			city2 = ortsliste[i]
			observation2 = owm.weather_at_place(city2)
			w2 = observation2.get_weather() 
			t2 = w2.get_temperature()
			ergebnis = compareTemperature(t1["temp"], t2["temp"])
			if (ergebnis==t1["temp"]):
				t1["temp"]=conversionTemp(t1["temp"])
				return "Stadt: "+city+", Temperatur: "+str(t1["temp"])+"°C"
			elif(ergebnis==t2["temp"]):
				t2["temp"]=conversionTemp(t2["temp"])
				return "Stadt: "+city2+", Temperatur: "+str(t2["temp"])+"°C"
			else:
				t1["temp"]=conversionTemp(t1["temp"])
				t2["temp"]=conversionTemp(t2["temp"])
				return "Stadt: "+city+", Temperatur: "+str(t1["temp"])+"°C"+"<br />Stadt: "+city2+", Temperatur: "+str(t2["temp"])+"°C"
	print(ortsliste)
	#return ortsliste