from dash import html

def showAssetInfo():
    return html.Div([
                
                html.H6('Name:'),
                html.H6(id='display-asset-name'),
                
                html.H6('Description:'),
                html.H6(id='display-asset-desc'),
                                
                html.H6('Website:'),
                html.Pre(id='web_link'),
            
            ])
