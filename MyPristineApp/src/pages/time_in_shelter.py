# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 11:56:08 2022

@author: avery
"""

import dash

dash.register_page(__name__)

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import numpy as np
import pandas as pd
from natsort import natsorted
import pathlib

def get_pandas_data(csv_filename: str) -> pd.DataFrame:
   '''
   Load data from /data directory as a pandas DataFrame
   using relative paths. Relative paths are necessary for
   data loading to work in Heroku.
   '''
   PATH = pathlib.Path(__file__).parent
   DATA_PATH = PATH.joinpath("data").resolve()
   return pd.read_csv(DATA_PATH.joinpath(csv_filename))


df = get_pandas_data("aac_intakes_outcomes.csv")



layout = html.Div(
    [
     html.H1('Analyzing Time Spent in Shelter', style={'textAlign': 'center'}),
     html.P('In this analysis, we will analyze what factors may lead to an animal being in the shelter longer than others.', style={'textAlign': 'center'}),
     html.P('Graph takes a second to load!!!', style={'textAlign': 'center'}),
     
     
    html.P("Choose an 'x' Variable:"),
    dcc.Dropdown([{'label': 'Age Group Upon Intake', 'value': 'age_upon_intake_age_group'},
                {'label': 'Animal Type', 'value': 'animal_type'},
                {'label': 'Intake Type', 'value': 'intake_type'},
                {'label': 'Intake Condition', 'value': 'intake_condition'},
                {'label': 'Sex Upon Intake', 'value': 'sex_upon_intake'}
            ],'animal_type', id='y-dropdown'),
    dcc.Graph(id="histograms-graph"),
    ]
)


@callback(
    Output("histograms-graph", "figure"),
    Input("y-dropdown", "value"),
)
def display_color(category):
    order = df.groupby(by = category, level=0).mean().sort_values(by='time_in_shelter_days',ascending=False).index.to_list()
    fig = px.violin(df, y="time_in_shelter_days", points='all', box=True, x = category, category_orders={category: order},
                    labels={'animal_type':'Animal Type', 'time_in_shelter_days': 'Time in Shelter (in Days)',
                            'age_upon_intake_age_group':'Age Group Upon Intake', 'intake_type':'Intake Type',
                            'intake_condition': 'Intake Condition', 'sex_upon_intake': 'Sex Upon Intake'})
    return fig