import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
#import dash_table_experiments as dt
import plotly
import flask
import pandas as pd
import numpy as np
import os
import sys

tokensPath = "../private/"

# Add the directory containing your module to
# the Python path (wants absolute paths)
sys.path.append(tokensPath)

from tokens import *

map_data = pd.read_csv('https://raw.githubusercontent.com/centraldedados/incendios/master/data/incendios2015.csv')

app = dash.Dash()

# Boostrap CSS.
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})
