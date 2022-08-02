# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 11:55:36 2022

@author: avery
"""

import dash

dash.register_page(__name__)

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.express as px
import dash_daq as daq
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




def prep_time_series(df, focus_col):
    df_temp = pd.DataFrame()
    df_temp[focus_col] = pd.to_datetime(df[focus_col])
    df_temp['day_of_week'] =  df_temp[focus_col].dt.day_name()
    df_temp['hours'] =  df_temp[focus_col].dt.hour
    df_temp['year'] =  df_temp[focus_col].dt.year
    df_temp['date'] =  df_temp[focus_col].dt.date
    df_temp['month'] =  df_temp[focus_col].dt.month
    df_temp['action'] = 1
    cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return df_temp




layout = html.Div(
    [
     
     html.H1('When Do Incomes & Outcomes Occur?',style={'textAlign': 'center'}),
     html.P('In this analysis, we will analyze what day of the week has the most action, what hour of the day, and also what day of the year.', style={'textAlign': 'center'}),
     
     
     daq.BooleanSwitch(
          on=True,
          label="Income or Outcome",
          labelPosition="top",
          id="income-switcher"
        ),
     
     daq.BooleanSwitch(
          on=True,
          label="Week or Year",
          labelPosition="top",
          id="time-switcher"
        ),

     html.H2("Intake", id="mode" ),
     
     dcc.Graph(id="time-graph")
     
     
    ]
)



@callback(
    Output("time-graph", "figure"),
    Output("mode","children"),
    Input("time-switcher", "on"),
    Input("income-switcher", "on"),
)
def display_color(position, income_switcher):
    
    if income_switcher == True:
        df_temp =  prep_time_series(df, "intake_datetime")
        mode = 'Intakes'
    else:
        df_temp =  prep_time_series(df, "outcome_datetime")
        mode = "Outcomes"
        
    
    
    if position == True:
        # Linechart
        df_pivot2 = df_temp.pivot_table(index="date", values="action", aggfunc="sum").reset_index()
        #df_pivot2['year'] =  pd.to_datetime(df_pivot2['date']).dt.year
        fig = px.line(df_pivot2, x="date", y="action")
        
    else:
        # Pivot
        cats = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        df_pivot = df_temp.pivot_table(index="day_of_week",columns="hours",values="action", aggfunc="sum").reindex(cats)
        # Heatmap
        fig = px.imshow(df_pivot, text_auto=True)
        
        
    return fig, mode
