from flask import Flask, render_template, request, redirect
from bokeh.charts import TimeSeries
from bokeh.embed import components
import bokeh
import pandas as pd
from random import random
from datetime import datetime, timedelta

import json
from urllib2 import urlopen, HTTPError
from io import StringIO

app = Flask(__name__)

app.api_key = 'YzCQfNaj_RRvSF7Kcfkm'  #quandl api key

@app.route('/')
def main():
	return redirect('/index')

@app.route('/index',methods=['GET', 'POST'])
def index():
	
	if request.method == 'GET':
		return render_template('index.html')
	if request.method == 'POST':
		
		lag = 1	
		ticker = request.form['ticker']
		keys = ['Close', 'Open', 'Adj. Open', 'Adj. Close', 'High', 'Low']
		series = [s for s in keys if s in request.form.keys()]
		if series == []:
			series = ['Close']
		
		def pad(s):
			s=str(s)
			if len(s)==1:
				s = '0'+s
			return(s)
		now = datetime.now()
		dend = str(now.year)+'-'+pad(now.month)+'-'+pad(now.day)
		go = True
		f = 0
		while go:
			try:
				dstart = str(now.year)+'-'+pad(now.month-1)+'-'+pad(now.day-f)
				dmp = datetime.strptime(dstart, '%Y-%m-%d')
				go = False
			except:
				f = f + 1
		drange = (dstart, dend)
		#drange = ('2016-07-01', '2016-08-01') #fix range	
		
		
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
		plot = TimeSeries(data=data[::-1], x='Date', y=series, legend=True, xlabel='Date', ylabel='$', title=ticker)
		script, div = components(plot) 	
	
		return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
	app.run(port=33507)
