from dash import html
from dash import dcc


def selectMap(df):
    return html.Div([
        html.Label(children=['Select all assets the map should display:'], style={
            'textDecoration': 'underline', 'fontSize': 20}),
        dcc.Checklist(id="recycling_type", value=[x for x in sorted(df['asset_type'].unique())],
                      options=[{'label': x, 'value': x}
                               for x in sorted(df['asset_type'].unique())],
                      labelClassName='mr-3 text-secondary')],
        style={'background': '#edede8', 'font-family': 'Gill Sans', 'textAlign': 'left', 'color': '#414744'}),
