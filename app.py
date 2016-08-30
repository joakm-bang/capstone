from flask import Flask, render_template, request, redirect
from bokeh.charts import TimeSeries
from bokeh.embed import components
import pandas as pd
from random import random

app = Flask(__name__)

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
	plot = TimeSeries(data=data, legend=True, xlabel='Date', ylabel='$', title='Stock')
	script, div = components(plot)  

	return render_template('index.html', script=script, div=div)

if __name__ == '__main__':
	app.run(port=33507)
