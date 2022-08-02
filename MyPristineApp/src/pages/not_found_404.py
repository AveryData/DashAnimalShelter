# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 11:54:34 2022

@author: avery
"""

from dash import html
import dash

dash.register_page(__name__, path="/404")


layout = html.H1("Custom 404")