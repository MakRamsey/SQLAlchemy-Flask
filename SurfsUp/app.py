# Import the dependencies.
from flask import Flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
import numpy as np

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
# Creating home endpoint/route to display all available endpoints/routes
# Set up dynamaic endpoint available route to show proper formatting
@app.route("/")
def welcome():
    return (
        f"Welcome! Please reference the list of available routes below:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"'start' and 'end' date should be formatted as YYYY-MM-DD in the above two endpoint URLs"
    )

# Creating precipitation endpoint/route
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Establish query date
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Execute query using context manager
    with Session(engine) as session:
        results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= query_date).all()

    # Store query results in a dictionary for display
    results_dictionary = {date: prcp for date, prcp in results}

    # Display jsonified result
    return jsonify(results_dictionary)

# Creating the stations endpoint/route
@app.route("/api/v1.0/stations")
def stations():

    # Execute query using context manager
    with Session(engine) as session:
        results = session.query(station.station).all()

    # Store query results in a list for display
    list_of_stations = [result[0] for result in results]

    # Display jsonified result
    return jsonify(list_of_stations)

# Creating the tobs endpoint/route
@app.route("/api/v1.0/tobs")
def tobs():

    # Establish query date
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Execute query using context manager
    with Session(engine) as session:
        results = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= query_date).all()
    
    # Store query results as a list of dictionarires for display
    temperatures_list =[]
    for date, tobs in results:
        temperatures_list.append({date: tobs})

    # Display jsonified result
    return jsonify(temperatures_list)

# Creating the first dynamic/variable endpoint/route which accepts 'start date'
@app.route("/api/v1.0/temp/<start>")
def data_for_start(start):
    
    # Execute query based on the 'start date' input using context manager
    with Session(engine) as session:
        results = session.query(func.min(measurement.tobs),
        func.avg(measurement.tobs),
        func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    
    # Store query results as a list of dictionarires for display
    temp_data = []
    for TMIN, TAVG, TMAX in results:
        temp_data.append({
             'TMIN': TMIN,
             'TAVG': TAVG,
             'TMAX': TMAX
        })

    # Display jsonified result
    return jsonify(temp_data)

# Creating the second dynamic/variable endpoint/route which accepts 'start date' & 'end date'
@app.route("/api/v1.0/temp/<start>/<end>")
def data_for_start_end(start, end):
    
    # Execute query based on the 'start date' & 'end date' inputs using context manager
    with Session(engine) as session:
        results = session.query(func.min(measurement.tobs),
        func.avg(measurement.tobs),
        func.max(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()
    
    # Store query results as a list of dictionarires for display
    temp_data = []
    for TMIN, TAVG, TMAX in results:
        temp_data.append({
             'TMIN': TMIN,
             'TAVG': TAVG,
             'TMAX': TMAX
        })

    # Display jsonified result
    return jsonify(temp_data)

# Flask conclusion protocol
if __name__ == "__main__":
    app.run(debug=True)