import folium
from folium import plugins
from preprocessor import Preprocessor
from formatPoints import *
from loadData import loadDataFromS3

from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
from plotlyPlot import plotlyPlot

application = Flask(__name__)


@application.route('/callback', methods=['POST', 'GET'])
def cb():
    return gm(request.args.get('data'))


@application.route('/')
def index():
    return render_template('loc_ts.html', graphJSON=gm())


@application.route('/map')
def display_map():
    return render_template('map.html')


def gm(island='Honolulu'):
    df = generate_location_ts(loc=island)
    final_ts = df.review_count
    fig = plotlyPlot(final_ts)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def update_map(cleaned_count):
    points, indices = generate_location_points(cleaned_count)[0], \
                      generate_location_points(cleaned_count)[1]
    time_map = folium.Map([21.3487, -157.944], zoom_start=10.5)
    hm = plugins.HeatMapWithTime(points, index=indices, auto_play=True, max_opacity=0.6)
    hm.add_to(time_map)
    time_map.save('templates/map.html')
    return


def generate_location_ts(loc='Honolulu'):
    df = pd.read_pickle("ts.pkl")
    df = df[df.neighbourhood_group_cleansed == loc]
    df = df.groupby('date', sort=True)['listing_id'].count().rename('review_count').reset_index().set_index('date')
    return df


if __name__ == '__main__':
    reviews = loadDataFromS3('flask-airbnb', 'reviews-4.csv')
    listings = loadDataFromS3('flask-airbnb', 'listings-4.csv')
    P = Preprocessor()
    ts = P.process_count(reviews, listings)
    ts.to_pickle('ts.pkl')
    r_count = P.process_location_count(reviews, listings)
    update_map(r_count)

    application.run(debug=True)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     loc = None
#
#     if request.method == 'post':
#         loc = request.form['island']
#
#     def update_map(location='Maui'):
#         points, indices = generate_location_points(location)[0], generate_location_points(location)[1]
#         time_map = folium.Map([20.85, -156.5], zoom_start=10.5)
#         hm = plugins.HeatMapWithTime(points, index=indices, auto_play=True, max_opacity=0.6)
#         hm.add_to(time_map)
#         return time_map
#
#     if loc:
#         m = update_map(loc)
#         m.save('templates/map.html')
#
#     return render_template('index.html')
#
#
# @app.route('/map')
# def display_map():
#     return render_template('map.html')
