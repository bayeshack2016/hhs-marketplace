from webapp import app
from flask import render_template, request, jsonify,Response, send_from_directory
import json
from bokeh.plotting import figure
from bokeh.embed import components 
from bokeh import mpl
import matplotlib.pyplot as plt
import numpy as np

@app.route('/')
@app.route('/index')
def index():

    return render_template('main.html')


@app.route('/search', methods=['POST'])
def search():
    age = request.form['age']
    zipcode = request.form['zipcode']
    print age, zipcode
    script,div = test_plot()
    return json.dumps({'num_plans':35, 'script': script, 'plot_div': div})

def test_plot():
    x = np.linspace(-2 * np.pi, 2 * np.pi, 100)
    y = np.sin(x)
    z = np.cos(x)
     
    plt.plot(x, y, "r-", marker='o')
     
    # dashed lines work
    plt.plot(x, z, "g-x", linestyle="-.")
        # plt.scatter( [1, 2, 3, 4, 5],[6, 7, 2, 4, 5])
        # plt.title('testing')

    p = mpl.to_bokeh()
    p.logo = None
    p.toolbar_location = None
    return components(p)
