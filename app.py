import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
     """List all available api routes."""
     return (
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/2015<br/>'
        f'/api/v1.0/2016/2017'
        )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(measurement.date, measurement.prcp).\
                filter(measurement.date >= '2016-08-23').\
                group_by(measurement.date).all()
    
    precipitation_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        precipitation_list.append(prcp_dict)
    return jsonify(precipitation_list)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    station = Base.classes.station

    results = session.query(station.id, station.station, station.name, station.latitude, station.longitude, station.elevation).all()
    
    station_list = []

    for id, station, name, latitude, longitutde, elevation in results:
        station_dict = {}
        station_dict['id'] = id 
        station_dict['name'] = name
        station_dict['station'] = station
        station_dict['latitude'] = latitude
        station_dict['longitude'] = longitutde
        station_dict['elevation'] = elevation
        station_list.append(station_dict)
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')

def tobs():
    session = Session(engine)
    measurement = Base.classes.measurement
    
    results = session.query(measurement.station, measurement.date, measurement.tobs).\
                filter(measurement.station =='USC00519281', measurement.date >= '2016-08-23').all()
    
    tobs_list = []

    for station, date, tobs in results:
        tobs_dict = {}
        tobs_dict['station'] = station
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

@app.route('/api/v1.0/2015')
def start_2015():
    session = Session(engine)
    measurement = Base.classes.measurement
    
    results = session.query(measurement.station, func.min(measurement.tobs), 
                             func.max(measurement.tobs), func.avg(measurement.tobs)).\
                filter(measurement.date >= '2015-01-01').\
                group_by(measurement.station).all()
    
    start_list = []

    for station, TMIN, TMAX, TAVG in results:
        start_dict = {}
        start_dict['station'] = station
        start_dict['TMIN'] = TMIN
        start_dict['TMAX'] = TMAX
        start_dict['TAVG'] = TAVG
        start_list.append(start_dict)
    return jsonify(start_list)

@app.route('/api/v1.0/2016/2017')

def start_end():
    session = Session(engine)
    measurement = Base.classes.measurement
    
    results = session.query(measurement.station, func.min(measurement.tobs), 
                             func.max(measurement.tobs), func.avg(measurement.tobs)).\
                filter(measurement.date >= '2016-01-01', measurement.date <='2016-12-31').\
                group_by(measurement.station).all()
    
    start_end_list = []

    for station, TMIN, TMAX, TAVG in results:
        start_end_dict = {}
        start_end_dict['station'] = station
        start_end_dict['TMIN'] = TMIN
        start_end_dict['TMAX'] = TMAX
        start_end_dict['TAVG'] = TAVG
        start_end_list.append(start_end_dict)
    return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)
