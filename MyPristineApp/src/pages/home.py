# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 11:55:51 2022

@author: avery
"""

import dash

dash.register_page(__name__, path="/")

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
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
df['intake_date'] = pd.to_datetime(df['intake_datetime']).dt.date
pets_per_day = round(len(df)/len(df['intake_date'].unique()),0)

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}


card1 = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5(pets_per_day, className="card-title"),
                    html.P("Number of animals left at center daily", className="card-text",),
                ]
            )
        ),
        dbc.Card(
            html.Div(className="fa fa-cat", style=card_icon),
            className="bg-info",
            style={"maxWidth": 90},
        ),
    ],className="mt-4 shadow",
)


average_days_in_shelter = round(df['time_in_shelter_days'].mean(),1)

card2 = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5(average_days_in_shelter, className="card-title"),
                    html.P("Average # of days spent in shelter", className="card-text",),
                ]
            )
        ),
        dbc.Card(
            html.Div(className="fa fa-calendar-day", style=card_icon),
            className="bg-info",
            style={"maxWidth": 90},
        ),
    ],className="mt-4 shadow",
)


adoption_rate = round(df['outcome_type'].value_counts()*100/len(df),0)['Adoption']

card3 = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5(str(adoption_rate) + "%", className="card-title"),
                    html.P("Adroption Rate", className="card-text",),
                ]
            )
        ),
        dbc.Card(
            html.Div(className="fa fa-heart", style=card_icon),
            className="bg-info",
            style={"maxWidth": 90},
        ),
    ],className="mt-4 shadow",
)



animal_type_pie = px.pie(df['animal_type'].value_counts().reset_index(), values='animal_type', names='index', title='Animals Received', 
                         labels={'index':'Animal', 'animal_type': 'Animals Recieved'})
outcomes = df['outcome_type'].value_counts().reset_index()
outcome_bar = px.bar(df['outcome_type'].value_counts().reset_index().sort_values(by = 'outcome_type', ascending=True), x='outcome_type', y='index',
                     title='Outcome Type', labels={'outcome_type':'Numbers Of Outcome', 'index':'Outcome Type'})
age_histogram = px.scatter(df, x="age_upon_intake_(years)", y="time_in_shelter_days", color="animal_type", title='Age Histogram',
                           labels={'age_upon_intake_(years)':'Age Upon Intake (in Years)', 'time_in_shelter_days':'Time in Shelter (in Days)', 'animal_type':'Animals Category'})



layout = html.Div(
    [
        html.H1("😸" + " Austin Animal Shelter App" + "🐶"),
        html.P('''The Austin Animal Center in Austin, Texas is the largest no-kill animal shelter in the United States.
               Every year, they provide care and shelter for over 18,000 animals. Their goals is to place all adoptable animals in forever homes.
               ''',style={'textAlign': 'center'}),
               
        html.Div(dbc.Row([dbc.Col(card1),dbc.Col(card2),dbc.Col(card3)])),
        
        html.Div(dbc.Row([
            dbc.Col(dcc.Graph(id="pie-graph", figure = animal_type_pie, style={'width': '40vh', 'height': '50vh'})),
            dbc.Col(dcc.Graph(id="bar-graph", figure = outcome_bar,style={'width': '70vh', 'height': '50vh'})),
            dbc.Col(dcc.Graph(id="age-graph", figure = age_histogram, style={'width': '70vh', 'height': '50vh'}))
            ])),
        
        html.A("If you'd like to donate to their cause, click here",href="https://www.austintexas.gov/department/support-animal-center", 
               target ="_blank", style={'textAlign': 'center'}),
        
        html.Br(),
        
        html.Div(
            html.Img(src="https://npr.brightspotcdn.com/dims4/default/5376171/2147483647/strip/true/crop/800x420+0+67/resize/1200x630!/quality/90/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2Flegacy%2Fsites%2Fkut%2Ffiles%2F1-IMG_1530.JPG",
                     style={'height': '15%','width': '25%'}
                     ),
            ),
        
        
        html.P("Future Additions to Project: Add Favicon logo, give an estimators till adopted prediction model and, add more pages"),
        html.H2('Produly made with Dash from plotly'),
        html.Div(
            html.Img(src="https://images.prismic.io/plotly-marketing-website/b91638ab-80b7-446d-8a83-b6d911bd1519_Plotly_logo.png?auto=compress,format",
                     style={'height': '15%','width': '25%'}
                     ),
            ),
        

        
    ]
,style={'textAlign': 'center'})

