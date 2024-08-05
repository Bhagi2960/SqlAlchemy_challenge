# Import the dependencies.
import numpy as np
import json
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify, Response


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
session.query(measurement.date).order_by(measurement.date.desc()).first()
preYear = dt.date(2017, 8, 23) - dt.timedelta(days=365)
session.close()


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitations """
    # Query all precipitation values for last year
    results = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= preYear).all()

    #results = session.query(measurement.date, measurement.prcp).all()

    session.close()

# Create a dictionary from the row data and append to a list 
    prcp = []
    for result in results:
        prcp_dict = {}
        prcp_dict["date"] = result[0]
        prcp_dict["prcp"] = result[1]
        prcp.append(prcp_dict)

    return jsonify(prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations """
    # Query all stations
    results = session.query(station.station).group_by(station.id).all()

    session.close()

    # Create a list of all_stations
    all_stations = []
    for result in results:
        st_dict = {}
        st_dict["station"] = result[0]
        all_stations.append(st_dict)
        
        return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations """
    # Query all dates and temperature observations of the most active station for the last year of data
    results = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= preYear).all()

    session.close()

    # Create a list of all_stations
    all_stations = []
    for result in results:
        station_dict = {}
        station_dict["date"] = result[0]
        station_dict["tobs"] = result[1]
        all_stations.append(station_dict)
        
        return jsonify(all_stations)


@app.route("/api/v1.0/start")
def start():   
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of agg data"""
    # Query TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= preYear).all()

    session.close()

    # Create a list of min, max, and avg
    aggregation_data = []
    for result in results:
        aggregate_dict = {}
        aggregate_dict["TMIN"] = result[0]
        aggregate_dict["TMAX"] = result[1]
        aggregate_dict["TAVG"] = result[2]
        aggregation_data.append(aggregate_dict)
        
        return jsonify(aggregation_data)


@app.route("/api/v1.0/start_end")
def start_end():   
    # Create our session (link) from Python to the DB
    session = Session(engine)
    today = dt.datetime(2016, 8, 23)
    """Return a list of agg data"""
    # Query TMIN, TAVG, and TMAX for all dates between dates
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= preYear).filter(measurement.date <= today).all()

    session.close()

    # Create a list of min, max, and avg
    aggregation_data = []
    for result in results:
        aggregate_dict = {}
        aggregate_dict["TMIN"] = result[0]
        aggregate_dict["TMAX"] = result[1]
        aggregate_dict["TAVG"] = result[2]
        aggregation_data.append(aggregate_dict)
        
        return jsonify(aggregation_data)

if __name__ == '__main__':
    app.run(debug=True)