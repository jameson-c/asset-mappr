# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 19:59:39 2022

@author: mihir
"""

            ),
            dcc.Dropdown(
                id='choose-the-stat',
                options=[
                    {"label": "count_number", "value": 'count_number'}],
                value='count_number',
                multi=False
            ),

        ]),
        dbc.Row([
            ),
            dcc.Graph(id='bar-chart-for-planner')

        ]),