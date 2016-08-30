from flask import Flask, render_template, request, redirect
from bokeh.charts import TimeSeries
from bokeh.embed import components
import bokeh
import pandas as pd
from random import random

import json
from urllib2 import urlopen, HTTPError
from io import StringIO

app = Flask(__name__)

app.api_key = 'YzCQfNaj_RRvSF7Kcfkm'  #quandl api key

@app.route('/')
def main():
	return redirect('/index')

@app.route('/index')
def index():
	
	dat = dict()
	dat['Date'] = range(1000,1100)
	dat['Price'] = []
	for x in dat['Date']:
		dat['Price'].append(random())
	
	data = pd.DataFrame.from_dict(dat)
	plot = TimeSeries(data=data, x='Date', y=['Price'], legend=True, xlabel='Date', ylabel='$', title='Stock')
	script, div = components(plot) 
	
	ticker = 'GOOG'
	drange = ('2016-06-01', '2016-07-01')
	
	
	#read from csv for now
	url = 'https://www.quandl.com/api/v3/datasets/WIKI/{0}.csv?trim_start={1}&trim_end={2}&api_key={3}'.format(ticker, str(drange[0]), str(drange[1]),app.api_key)
	try:
		csvdata = urlopen(url).read()
	except HTTPError:
		return render_template('index.html', ticker=ticker, error='Invalid ticker')
	data = pd.read_csv(StringIO(csvdata.decode('utf-8')), index_col=0, parse_dates=True)
	data['Date'] = data.index
	plot = TimeSeries(data=data[['Open', 'Close']], legend=True, xlabel='Date', ylabel='$', title=ticker)
	script, div = components(plot)
	
	
	url = 'https://www.quandl.com/api/v3/datasets/WIKI/{0}.json?trim_start={1}&trim_end={2}&api_key={3}'.format(ticker, str(drange[0]), str(drange[1]),app.api_key)
	try:
		jsondata = urlopen(url).read()
	except HTTPError:
		return render_template('index.html', ticker=ticker, error='Invalid ticker')
	jsondata = json.loads(jsondata)
	data = pd.DataFrame.from_dict(jsondata['dataset']['data'])	
	data.columns = jsondata['dataset']['column_names']
	data.index = data.Date
	pd.to_datetime(data.index)
	plot = TimeSeries(data=data, x='Date', y=['Close', 'Open'], legend=True, xlabel='Date', ylabel='$', title='Stock')
	script, div = components(plot) 	

	return render_template('index.html', script=script, div=div)

if __name__ == '__main__':
	app.run(port=33507)
