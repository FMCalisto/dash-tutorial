#!/usr/bin/python
# -*- coding: utf-8 -*-

import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import plotly
from plotly import graph_objs as go
from plotly.graph_objs import *
from flask import Flask
import pandas as pd
import numpy as np
import os
import copy
import sys

tokensPath = "../private/"

# Add the directory containing your module to
# the Python path (wants absolute paths)
sys.path.append(tokensPath)

from tokens import *

app = dash.Dash(__name__)
server = app.server

# API keys and datasets

#map_data = pd.read_csv('https://raw.githubusercontent.com/amyoshino/SONYC-Dash-App/master/SONYC_Dataset.csv')

map_data = pd.read_csv('https://raw.githubusercontent.com/centraldedados/incendios/master/data/incendios2015.csv')

map_data.drop('ano', 1, inplace=True)
map_data.drop('codigo_sgif', 1, inplace=True)
map_data.drop('codigo_anpc', 1, inplace=True)
map_data.drop('tipo', 1, inplace=True)
map_data.drop('distrito', 1, inplace=True)
map_data.drop('concelho', 1, inplace=True)
map_data.drop('freguesia', 1, inplace=True)
# map_data.drop('local', 1, inplace=True)
map_data.drop('ine', 1, inplace=True)
map_data.drop('x', 1, inplace=True)
map_data.drop('y', 1, inplace=True)
# map_data.drop('lat', 1, inplace=True)
# map_data.drop('lon', 1, inplace=True)
map_data.drop('data_alerta', 1, inplace=True)
map_data.drop('hora_alerta', 1, inplace=True)
map_data.drop('data_extincao', 1, inplace=True)
map_data.drop('hora_extincao', 1, inplace=True)
map_data.drop('data_primeira_intervencao', 1, inplace=True)
map_data.drop('hora_primeira_intervencao', 1, inplace=True)
map_data.drop('fonte_alerta', 1, inplace=True)
map_data.drop('nut', 1, inplace=True)
map_data.drop('area_povoamento', 1, inplace=True)
map_data.drop('area_mato', 1, inplace=True)
map_data.drop('area_agricola', 1, inplace=True)
map_data.drop('area_pov_mato', 1, inplace=True)
# map_data.drop('area_total', 1, inplace=True)
map_data.drop('reacendimento', 1, inplace=True)
map_data.drop('queimada', 1, inplace=True)
map_data.drop('falso_alarme', 1, inplace=True)
map_data.drop('fogacho', 1, inplace=True)
map_data.drop('incendio', 1, inplace=True)
map_data.drop('agricola', 1, inplace=True)
map_data.drop('perimetro', 1, inplace=True)
map_data.drop('aps', 1, inplace=True)
map_data.drop('causa', 1, inplace=True)
# map_data.drop('tipo_causa', 1, inplace=True)
map_data.drop('regiao_prof', 1, inplace=True)
map_data.drop('ugf', 1, inplace=True)

# Boostrap CSS.

app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'
                   })  # noqa: E501

layout = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='Each dot is an NYC Middle School eligible for SONYC funding',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(
            lon=-73.91251,
            lat=40.7342
        ),
        zoom=10,
    )
)

# Controls (dropdowns)

group = ['All']
group = group + ['Low', 'Medium', 'High', 'Very High']
group_class = [{'label': str(item), 'value': str(item)} for item in
               group]

# Creating layouts for datatable

layout_right = copy.deepcopy(layout)
layout_right['height'] = 300
layout_right['margin-top'] = '20'
layout_right['font-size'] = '12'

mp_max = map_data['area_total'].max()
mp_min = map_data['area_total'].min()

print(mp_max)
print(mp_min)


# Components style

def color_scale(md, selected_row_indices=[]):
    color = []
    max_score = mp_max
    min_score = mp_min
    for row in md['area_total']:
        scale = (row - mp_min) / (mp_max - mp_min)
        if scale <= 0.06:
            color.append('#26EC04')
        elif scale <= 0.12:
            color.append('#8FDB44')
        elif scale <= 0.18:
            color.append('#A5D643')
        elif scale <= 0.24:
            color.append('#B8D343')
        elif scale <= 0.30:
            color.append('#B8D343')
        elif scale <= 0.36:
            color.append('#DBCD44')
        elif scale <= 0.42:
            color.append('#E1CD44')
        elif scale <= 0.48:
            color.append('#F0CB45')
        elif scale <= 0.54:
            color.append('#F3C644')
        elif scale <= 0.60:
            color.append('#F2BE41')
        elif scale <= 0.66:
            color.append('#F0AE3D')
        elif scale <= 0.72:
            color.append('#EFA73B')
        elif scale <= 0.78:
            color.append('#EE9F39')
        elif scale <= 0.84:
            color.append('#ED8934')
        elif scale <= 0.90:
            color.append('#E95729')
        else:
            color.append('#FD0101')
    for i in selected_row_indices:
        color[i] = '#1500FA'
    return color


def gen_map(map_data):

    # groupby returns a dictionary mapping the values of the first field
    # 'classification' onto a list of record dictionaries with that
    # classification value.

    return {'data': [{
        'type': 'scattermapbox',
        'lat': list(map_data['lat']),
        'lon': list(map_data['lon']),
        'text': list(map_data['area_total']),
        'mode': 'markers',
        'name': list(map_data['local']),
        'marker': {'size': 6, 'opacity': 1.0,
                   'color': color_scale(map_data)},
        }], 'layout': layout}


# Layout

app.layout = html.Div([html.Div([html.H1('WFex',
                      style={'font-family': 'Helvetica',
                      'margin-top': '25', 'margin-bottom': '0'},
                      className='eight columns'),
                      html.Img(src='http://static1.squarespace.com/static/546fb494e4b08c59a7102fbc/t/591e105a6a496334b96b8e47/1497495757314/.png'
                      , className='two columns', style={  # Title - Row
    'height': '9%',
    'width': '9%',
    'float': 'right',
    'position': 'relative',
    'padding-top': 10,
    'padding-right': 0,
    }),
        html.P('A decision support system for Portuguese forest fires.'
               , style={'font-family': 'Helvetica', 'font-size': '120%'
               , 'width': '80%'}, className='eight columns')],
        className='row'), html.Div([html.Div([html.P('Choose Fire Types:'
                                   ), dcc.Checklist(id='Types',
                                   options=[{'label': 'Florestal',
                                   'value': 'Florestal'},
                                   {'label': 'Agricola', 'value': 'Agricola'
                                   }, {'label': 'Queimada',
                                   'value': 'Queimada'}],
                                   values=['Florestal', 'Agricola',
                                   'Queimada'],
                                   labelStyle={'display': 'inline-block'
                                   })], className='six columns',
                                   style={'margin-top': '10'}),
                                   html.Div([html.P('area_total:'),
                                   dcc.Dropdown(id='area_total',
                                   options=group_class, multi=False,
                                   value='All')],
                                   className='two columns',
                                   style={'margin-top': '10'}),
                                   html.Div([html.P('Crime BIN (group):'
                                   ), dcc.Dropdown(id='Crime',
                                   options=group_class, multi=False,
                                   value='All')],
                                   className='two columns',
                                   style={'margin-top': '10'}),
                                   html.Div([html.P('Obesity BIN (group):'
                                   ), dcc.Dropdown(id='Obesity',
                                   options=group_class, multi=False,
                                   value='All')],
                                   className='two columns',
                                   style={'margin-top': '10'})],
                                   className='row'),
        html.Div([html.Div([dcc.Graph(id='map-graph', animate=True,
                 style={'margin-top': '20'})], className='six columns'
                 ), html.Div([dt.DataTable(  # Selectors
                                             # Map + table + Histogram
    rows=map_data.to_dict('records'),
    columns=map_data.columns,
    row_selectable=True,
    filterable=True,
    sortable=True,
    selected_row_indices=[],
    id='datatable',
    )], style=layout_right, className='six columns'),
        html.Div([dcc.Graph(id='histogram')], className='twelve columns'
                 )], className='row')],
        className='ten columns offset-by-one')


# Callbacks and functions

@app.callback(Output('datatable', 'rows'),
              [dash.dependencies.Input('Types', 'values'),
              dash.dependencies.Input('area_total', 'value'),
              dash.dependencies.Input('Crime', 'value'),
              dash.dependencies.Input('Obesity', 'value')])
def update_selected_row_indices(
    boroughs,
    doe,
    crime,
    obesity,
    ):
    map_aux = map_data.copy()

    # Boroughs filter

    map_aux = map_aux[map_aux['distrito'].isin(boroughs)]

    # area_total filter

    if doe == 'Low':
        map_aux = map_aux[map_aux['area_total'] <= 2.5]
    if doe == 'Medium':
        map_aux = map_aux[(map_aux['area_total'] > 2.5)
                          & (map_aux['area_total'] <= 5.0)]
    if doe == 'High':
        map_aux = map_aux[(map_aux['area_total'] > 5.0)
                          & (map_aux['area_total'] <= 7.5)]
    if doe == 'Very High':
        map_aux = map_aux[map_aux['area_total'] > 7.5]

    # Crime filter

    if crime == 'Low':
        map_aux = map_aux[map_aux['Crime'] <= 0.1]
    if crime == 'Medium':
        map_aux = map_aux[(map_aux['Crime'] > 0.1) & (map_aux['Crime']
                          <= 0.25)]
    if crime == 'High':
        map_aux = map_aux[(map_aux['Crime'] > 0.25) & (map_aux['Crime']
                          <= 0.4)]
    if crime == 'Very High':
        map_aux = map_aux[map_aux['Crime'] > 0.4]

    # Obesity filter

    if obesity == 'Low':
        map_aux = map_aux[map_aux['Obesity'] <= 15]
    if obesity == 'Medium':
        map_aux = map_aux[(map_aux['Obesity'] > 15) & (map_aux['Obesity'
                          ] <= 27.5)]
    if obesity == 'High':
        map_aux = map_aux[(map_aux['Obesity'] > 27.5)
                          & (map_aux['Obesity'] <= 35.0)]
    if obesity == 'Very High':
        map_aux = map_aux[map_aux['Obesity'] > 35.0]

    rows = map_aux.to_dict('records')
    return rows


@app.callback(Output('datatable', 'selected_row_indices'),
              [Input('histogram', 'selectedData')], [State('datatable',
              'selected_row_indices')])
def update_selected_row_indices(selectedData, selected_row_indices):
    if selectedData:
        selected_row_indices = []
        for point in selectedData['points']:
            selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(Output('histogram', 'figure'), [Input('datatable', 'rows'
              ), Input('datatable', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    layout = go.Layout(
        bargap=0.05,
        bargroupgap=0,
        barmode='group',
        margin=Margin(l=50, r=10, t=0, b=100),
        showlegend=False,
        height=250,
        dragmode='select',
        xaxis=dict(showgrid=False, nticks=50, fixedrange=False),
        yaxis=dict(showticklabels=True, showgrid=False,
                   fixedrange=False, rangemode='nonnegative',
                   zeroline='hidden'),
        )

    data = Data([go.Bar(x=dff['Location Name'], y=dff['Need Score'],
                marker={'color': color_scale(dff,
                selected_row_indices)}, hoverinfo=dff['Location Name'
                ])])

    return go.Figure(data=data, layout=layout)


@app.callback(Output('map-graph', 'figure'), [Input('datatable', 'rows'
              ), Input('datatable', 'selected_row_indices')])
def map_selection(rows, selected_row_indices):
    aux = pd.DataFrame(rows)
    temp_df = aux.ix[selected_row_indices, :]
    if len(selected_row_indices) == 0:
        return gen_map(aux)
    return gen_map(temp_df)

if __name__ == '__main__':
    app.run_server(debug=True)
