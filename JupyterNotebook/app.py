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
        f"<a href='/api/v1.0/tobs'>Most active Station TOBS Data</a>"
        f"<br>"
        # f"<a href='/api/v1.0/<start>'>Enter Start Date (Year-Month-Day) for MIN, MAX and AVG Temperatures</a>"
        f"<br>"
        # f"<a href='/api/v1.0/<start>/<end>'>Enter Start and End Date (YearMonthDay) for MIN, MAX and AVG Temperatures</a>"


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
    # all_results
    return jsonify(all_results)


@app.route("/api/v1.0/stations")
def stations():
    """Return prcp data as json"""
    # Create session link for Python to DB
    session = Session(engine)

    # Query the station name from the station class
    results = session.query(Station.station, Station.name).all()

    session.close()

    all_results = []
    for item in results:
        all_results.append(item[0])
    # all_results

    return jsonify(all_results)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return prcp data as json"""
    # Create session link for Python to DB
    session = Session(engine)

    # What are the most active stations? (i.e. what stations have the most rows)?
    # List the stations and the counts in descending order.
    station_count = session.query(Measurement.station, func.count(Measurement.station))\
        .group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    # print(f"Station : {station_count[0][0]} was the most active with {station_count[0][1]} reported measurements")

    # Using the station id from the previous query, calculate the lowest temperature recorded, 
    # highest temperature recorded, and average temperature of the most active station
    most_active = session.query(Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs), func.count(Measurement.tobs))\
        .filter(Measurement.station == station_count[0][0]).all()
    most_active

    # Most active station name variable
    most_active_name = {most_active[0][0]}
    # most_active_name = str(most_active_name)
    most_active_name

    # Add the station with the most reports to a list to use later
    most_reports = []
    for active in most_active_name:
    #     print(active)
        most_reports.append(active)

    most_reports = most_reports[0]
    # most_reports

    ## Design a query to retrieve the last 12 months of precipitation data and plot the results
    date = session.query(func.max(Measurement.date)).all()
    year = int(date[0][0][0:4])
    month = int(date[0][0][5:7])
    day = int(date[0][0][8:10])

    ## Calculate the date 1 year ago from the last data point in the database
    year_ago = dt.date(year, month, day) - dt.timedelta(days=365)
    print(year_ago)

    ## Perform a query to retrieve the data and precipitation scores
    tobs_results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= year_ago).filter(Measurement.station == most_reports).all()
    tobs_results


    session.close()

    all_results = []
    for item in tobs_results:
        all_results.append(item[2])
    # all_results

    # all_results = list(np.ravel(tobs_results))

    return jsonify(all_results)


# @app.route("/api/v1.0/<start>")
# def start_date(start):
#     """Fetch the Date that matches
#        the path variable supplied by the user, or a 404 if not."""

#     # Create session link for Python to DB
#     session = Session(engine)

#     # start = ('2017-05-03')
#     results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),\
#                             func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
#     #results 

#     canonicalized = start
#     for date in results:
#         search_term = date[0]
#         print(date[0])
        
#         if search_term == canonicalized:
#             start_stats = []
#             start_stats.append(date[1])
#             start_stats.append(date[2])
#             start_stats.append(date[3])

#             if search_term == canonicalized:
#                 return jsonify(start_stats)

#     session.close()

#     return jsonify({"error": "Date not found."}), 404


# @app.route("/api/v1.0/<start>/<end>")
# def start_end(start, end):
#     """Fetch the start and end Date that matches
#        the path variable supplied by the user, or a 404 if not."""

#     # Create session link for Python to DB
#     session = Session(engine)

#     # start = ('2017-05-03')
#     results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs),\
#                             func.avg(Measurement.tobs)).filter(Measurement.date == start).all()
#     #results 

#     canonicalized = start
#     for date in results:
#         search_term = date[0]
#         print(date[0])
        
#         if search_term == canonicalized:
#             start_stats = []
#             start_stats.append(date[1])
#             start_stats.append(date[2])
#             start_stats.append(date[3])

#             if search_term == canonicalized:
#                 return jsonify(start_stats)

#     session.close()

#     return jsonify({"error": "Date not found."}), 404



if __name__ == "__main__":
    app.run(debug=True)

