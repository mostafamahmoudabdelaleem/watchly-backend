from app import app
import json
from flask import request, jsonify, render_template, abort
from app.scraper.akwam_scraper import *



@app.route('/api/v1/all_series',methods=['GET'])
def api_v1_all_series():
    response = ''
    with open('all_series.json', encoding="utf8") as f:
        response = json.load(f)
    return jsonify(response)


@app.route('/api/v1/all_movies',methods=['GET'])
def api_v1_all_movies():
    response = ''
    with open('all_movies.json', encoding="utf8") as f:
        response = json.load(f)
    return jsonify(response)


@app.route('/api/v1/series',methods=['GET'])
def api_v1_series():
    series_link = request.args.get('link')
    if series_link == None or series_link == '':
        abort(400)
    response = scrape_single_series(series_link)
    return jsonify(response)


@app.route('/api/v1/links',methods=['GET'])
def api_v1_links():
    link = request.args.get('link')
    if link == None or link == '':
        abort(400)
    response = scrape_links(link)
    return jsonify(response)
