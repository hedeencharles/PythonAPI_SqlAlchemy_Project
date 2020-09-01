# import Flask
from flask import Flask, json, jsonify

#Import sqlaclhemy
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc
import numpy as np
import pandas as pd
import datetime as dt 

# Create an engine that can talk to the database
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# reflect the tables
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Assign the station class to a variable called `Measurement`
Measurement = Base.classes.measurement

# # Assign the station class to a variable called "Station"
Station = Base.classes.station

# Create an app, being sure to pass __name__
app = Flask(__name__)


@app.route("/")
def welcome():
    return (
        f"Available Routes:"
        f"<br>"
        f"<a href='/api/v1.0/precipitation'>Precipitation Data</a>"
        f"<br>"
        f"<a href='/api/v1.0/stations'>Stations Data</a>"
        f"<br>"
        f"<a href='/api/v1.0/tobs'>TOBS Data</a>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return prcp data as json"""
    # Create session link for Python to DB
    session = Session(engine)

    ## Design a query to retrieve the last 12 months of precipitation data and plot the results
    date = session.query(func.max(Measurement.date)).all()
    year = int(date[0][0][0:4])
    month = int(date[0][0][5:7])
    day = int(date[0][0][8:10])

    ## Calculate the date 1 year ago from the last data point in the database
    year_ago = dt.date(year, month, day) - dt.timedelta(days=365)
    #print(year_ago)

    ## Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).all()
    
    session.close()

    all_results = []
    for item in results:
        item_dict = {}
        item_dict[item[0]] = item[1]
        all_results.append(item_dict)

    return jsonify(all_results)



@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return prcp data as json"""
    # Create session link for Python to DB
    session = Session(engine)
if __name__ == "__main__":
    app.run(debug=True)

