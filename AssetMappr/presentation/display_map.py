from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dash.dependencies import Input, Output, State
import dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.offline as py
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash
import numpy as np
import pandas as pd

def display_map():

    return html.Div(id='graph')