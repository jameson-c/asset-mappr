# AssetMappr

## About this app
This is a web application developed by Carnegie Mellon University students, for use in community asset mapping. Asset mapping is a systematic process of cataloging key services, benefits, and resources within the community. This includes institutions such as schools/hospitals, physical space, key local businesses, and anything else the community might consider an "asset". Communities need asset mapping in order to plan smartly for their future sustainability and growth. 

AssetMappr is organized by each community, and has three broad functions:
1. For a given community, populate a base set of assets to the database by querying several online sources (e.g. feeding keywords to Google Maps API, national education and healthcare facility datasets)
2. Take community input through the app on various aspects. E.g., what is missing in the community, what do people really value about the existing assets, etc.
3. Make this information easily usable for planners in their decision making and proposal-writing processes

We are currently piloting the app with town planners and municipalities in Southwestern Pennsylvania.

You can view its current state at this link: https://asset-mappr.onrender.com/

## Tech setup
This app is built using Dash, by Plotly. Dash apps have **layout** components that create the user interface, and **callbacks** that define interactivity (i.e., what happens when a button is clicked). We modularized the components into functions, which all get pulled into the main ```app.py``` file to build the app.

The cloud PostgreSQL database and server are hosted on [https://render.com/](Render). 

## Repo organization

The application follows a three-tier architecture:
1. Database: contains all the functions that read/write to the database. This includes both functions that populate the database from online sources, and functions that read/write from the database in real-time for the app's purposes
2. Application: contains all callback functions
3. Presentation: contains all UI/layout functions

Standardized naming has been used where possible. Take for example the feature that allows users to submit new assets to the database:
- submitNewAsset.py in the presentation folder has the layout components. I.e., the button that users click, the form where users add info about the new asset
- submitNewAsset_cb.py in the application folder has the callbacks that react as users navigate through the form
- submitNewAsset_db.py in the database folder has the function that takes the info users submitted and sends it to the database. This is used in the callback.

Each code file has additional details and comments in the header. 






