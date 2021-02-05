#Import Dependencies
from flask import Flask, jsonify

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

# Setup Database 
#---------------------------------------------------------
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#---------------------------------------------------------

# Reflect the Tables
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys

#References to both tables
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


#Flask Setup
#---------------------------------------------------------
app = Flask(__name__)
#---------------------------------------------------------

#Home Route
@app.route("/")
def home():
    return(
    "<h1>Hawaii Climate App (Flask API)</h1>"
    "<h3>Available Routes:</h3>"
    "/api/v1.0/precipitation<br/>"
    "<strong>All precipitation data</strong>"
    "<br/>"
    "<br/>"
    "/api/v1.0/stations<br/>"
    "<strong>A list of all weather observation stations</strong>"
    "<br/>"
    "<br/>"
    "/api/v1.0/tobs<br/>"
    "<strong>All temperature observations</strong>"
    "<br/>"
    "<br/>"
    '/api/v1.0/"(start_date)"<br/>'
    "<strong>A JSON list of the minimum temperature, the average temperature, and the max temperature for all dates greater than and equal to the start date</strong>"
    "<br/>"
    "<br/>"
    '/api/v1.0/"(start_date)"/"(End_Date)"<br/>'
    "<strong>A JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range</strong>"
    "<br/>"
    "<br/>"
    'Date formatting example: 2017-01-29'
    )

#Precipitation Data Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>="2016-08-23").all()
    precipitation_dict = list(np.ravel(precipitation_results))

    return jsonify(precipitation_dict)

#Station Data Route
@app.route("/api/v1.0/stations")
def stations():
    station_results = session.query(Station.station, Station.name).all()

    station_dict = list(np.ravel(station_results))

    return jsonify(station_dict)

#Temperature Observation Data Route
@app.route("/api/v1.0/tobs")
def tobs():
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date>="2016-08-23").\
            filter(Measurement.date<="2017-08-23").all()

            
    tobs_dict = list(np.ravel(tobs_results))

    return jsonify(tobs_dict)

# Start Day Through Final Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
        # Convert to normal list to be Jsonified
        start_day_list = list(start_day)
        return jsonify(start_day_list)

# Start Day - End Day Route
#.filter called twice to ensure all dates between 2 set days are included
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
       
        start_end_day_list = list(start_end_day)
        return jsonify(start_end_day_list)

if __name__ == '__main__':
    app.run(debug=True)


























