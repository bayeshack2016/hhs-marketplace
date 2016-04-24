from webapp import app
from flask import render_template, request, jsonify,Response, send_from_directory
import json
from bokeh.plotting import figure
from bokeh.charts import Bar
from bokeh.embed import components 
from bokeh import mpl
import matplotlib.pyplot as plt
import numpy as np
from time import time
import pandas as pd
from datetime import datetime
from bokeh.sampledata.autompg import autompg as df

#print df

@app.route('/')
@app.route('/index')
def index():

    return render_template('main.html')


@app.route('/search', methods=['POST'])
def search():
    age = request.form['age']
    zipcode = request.form['zipcode']
    npi = request.form['npi']

    print age, zipcode, npi
    
    return json.dumps(summarize_plans(zip2state(zipcode), age, npi))

def age2nationalAverage(age):
    age2avg = pd.read_csv('webapp/data/age2avg.csv', dtype=str)
    avg = age2avg[age2avg['Age']==str(age)].IndividualRate.values[0]
    return avg

@app.route('/search_providers', methods=['POST'])
def search_provider():
    age = request.form['age']
    zipcode = request.form['zipcode']
    query = request.form['q'].lower()
    # providers = pd.read_pickle('webapp/data/provider_info.pkl')
    providers = pd.read_hdf('webapp/data/providers.h5','providers')
    providers = providers[(providers.state == zip2state(zipcode)) & providers['last'].str.lower().str.startswith(query)]
    jsons = providers.apply(lambda x: {'npi':x['npi'],
                               'value': x['first'] +' ' + x['last'],
                               'label':x['last']+', '+x['first'],
                               'desc': ', '.join(x[['address','city','state','zip']])
                              },axis=1).values
    return jsonify(result=list(jsons))

def zip2state(zipcode):
    zippd = pd.read_csv('webapp/data/zip2state.csv', dtype=str)
    state = zippd[zippd.Zipcode==str(zipcode)].State.values[0]
    return state

def summarize_plans(state, age, npi):
    todaysdate = str(datetime.now())
    age = str(age)
    if age > '65':
      age = '65'
    elif age < '20':
      age = '20'
    # filter based on what plans are current (not expired) and age
    filteredplans = pd.read_hdf('webapp/data/plan-rates.h5', state, where=['(Age==age) & (RateExpirationDate > todaysdate) & (RateEffectiveDate < todaysdate)'],
                                columns = ['IndividualRate', 'MetalLevel', 'Age','URLForSummaryofBenefitsCoverage','PlanMarketingName'])
    stateave = filteredplans.IndividualRate.mean()
    myave = stateave 
    # plot it
    #filteredplans.groupby('MetalLevel').IndividualRate.mean().plot(kind='bar')
    #statebardf = filteredplans.groupby('MetalLevel').IndividualRate.mean()
    statebardf = filteredplans.groupby('MetalLevel', as_index=False).mean()
    
    #p = mpl.to_bokeh()
    if npi == '':
      p = Bar(filteredplans.groupby('MetalLevel').IndividualRate.mean(), values='IndividualRate',
              xlabel="", ylabel="Montly Premium ($)")
    else:
      print 'input npi is ' + npi
      # read hdf5 of provider-plan pairings
      provnplanpd = pd.read_hdf('webapp/data/plan_providers.h5', state)
      # make a list of planids for the input npi
      planlst = provnplanpd[provnplanpd.npi == npi].plan_id.values
      print planlst
      # read in hdf5 of plan info
      planinfo = pd.read_hdf('webapp/data/plan-rates.h5', state, where=['(Age==age) & (RateExpirationDate > todaysdate) & (RateEffectiveDate < todaysdate)'])

      # for each planid, get the first entry and concatenate them together.
      filteredplans = planinfo[planinfo.PlanId==planlst[0]].groupby('PlanId', as_index=False).first()
      filteredplans.head()
      #pd.concat([filteredplans, filteredplans])

      for ii in range(1, len(planlst)):
          filteredplans = pd.concat([filteredplans, planinfo[planinfo.PlanId==planlst[ii]].groupby('PlanId', as_index=False).first()])

    
      provbardf = filteredplans.groupby('MetalLevel', as_index=False).mean()
      provbardf['average'] = ['provider rates']*len(provbardf.MetalLevel.values)
      statebardf['average'] = ['state average']*len(provbardf.MetalLevel.values)
      myave = statebardf.IndividualRate.mean()
      #provbardf['average'] = [1, 1]
      #statebardf['average'] = [2, 2]
      #plotdf = pd.merge(statebardf, provbardf, on='MetalLevel')
      plotdf = pd.concat([provbardf, statebardf]) 
      #plotdf['state average'] = statebardf['IndividualRate']
      #plotdf['provider rates'] = provbardf['IndividualRate']
      print plotdf  
      p = Bar(plotdf, label='MetalLevel', values='IndividualRate', group='average', legend='top_right',
              xlabel="", ylabel="Montly Premium ($)")
    p.logo = None
    p.plot_height=400
    p.toolbar_location = None
    script,div =  components(p)
    print filteredplans.to_dict(orient='records')
    return {'num_plans':len(filteredplans), 'script': script, 'plot_div': div,
            'national_comp': format_price_comp(float(age2nationalAverage(age))-myave),
            'state_comp': format_price_comp(float(stateave)-myave),
            'plans': render_template('plans.html', plans=filteredplans.sort_values(by='IndividualRate').to_dict(orient='records'))}

def format_price_comp(price):
    price = int(float(price))
    return ('$%d '% price) + ('cheaper' if price < 0 else 'pricier')
