### import libraries ###
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

database_path = "hawaii.sqlite"

engine = create_engine(f"sqlite:///{database_path}?check_same_thread=False")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


### Create the app ###
app = Flask(__name__)

### Set what the user will get on the index page ###
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to the Climate App API!<br>"
        f"Avaialable routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/temp/start<br>"
        f"/api/v1.0/temp/start/end"
    )

### Set what the user will get on the /precipitation route page ###
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    
    precipitation = {date: prcp for date, prcp in results}

    return jsonify(precipitation)

### Set what the user will get on the /stations route page ###
@app.route("/api/v1.0/stations")
def stations():
    
    results = session.query(Station.station).all()
          
    stations = list(np.ravel(results))       
    return jsonify(stations)

### Set what the user will get on the /tobs route page ###
@app.route("/api/v1.0/tobs")
def tobs():
    
    prev_year = dt.date(2017, 8, 18) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).filter(Measurement.date >= prev_year).filter(Measurement.station=='USC00519281').all()

    tobs = list(np.ravel(results))

    return jsonify(tobs)

### Set what the user will get on the /start date route page ###
@app.route("/api/v1.0/temp/<start>")
def start(start):
    
    sel=[func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results = session.query(*sel).filter(Measurement.date >= start).all()
    temps = list(np.ravel(results))

    return jsonify(temps)


### Set what the user will get on the /start-end date route page ###
@app.route("/api/v1.0/temp/<start>/<end>")
def start_end(start,end):
    
    sel=[func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))

    return jsonify(temps)


### Define main behavior ###
if __name__ == "__main__":
    app.run(debug=True)