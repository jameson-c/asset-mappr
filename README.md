# AssetMappr

## About this app
This is a web application developed by Carnegie Mellon University students, for use in community asset mapping. Asset mapping is a systematic process of cataloging key services, benefits, and resources within the community. This includes institutions such as schools/hospitals, physical space, key local businesses, and anything else the community might consider an "asset". Communities need asset mapping in order to plan smartly for their future sustainability and growth. 

AssetMappr is organized by each community, and has three broad functions:
1. Populate a base set of assets to the database by querying several online sources (e.g. Google Maps API, national education and healthcare facility datasets)
2. Take community input through the app on various aspects. E.g., what is missing in the community, what do people really value, etc.
3. Make this information easily usable for planners in their decision-making and proposal-writing processes

We are currently piloting the app with town planners and municipalities in Southwestern Pennsylvania.

You can view its current state at this link: https://asset-mappr.onrender.com/

## Tech setup
This app is built using Dash, by Plotly. Dash apps have **layout** components that create the user interface, and **callbacks** that define interactivity (i.e., what happens when a button is clicked). We modularized the components into functions, which all get pulled into the main ```app.py``` file to build the app.

The cloud PostgreSQL database and server are hosted on [https://render.com/](Render). 

## Repo organization

The application follows a three-tier architecture:
1. **Database**: contains all the functions that read/write to the database. This includes both functions that initially populate the database from online sources, and functions needed for the app's real-time usage
2. **Application**: contains all callback functions
3. **Presentation**: contains all layout functions

Standardized naming has been used where possible. For example, the feature that allows users to submit new assets is comprised of:
- submitNewAsset.py in the presentation folder which has the layout components (the button that users click, the form where users add specific details)
- submitNewAsset_cb.py in the application folder which the callbacks (how the form changes as users click buttons, prompts and error messages)
- submitNewAsset_db.py in the database folder which has the function that takes submitted info and sends it to the database

Each code file has additional details and comments in the header. 

## Additional background

AssetMappr was started by a team of 5 students at Heinz College in January 2022: Mihir Bhaskar, Anna (Qi) Wang, Jameson Carter, Sara Maillacheruvu, and Michaela Marincic. Under the supervision of Professor Rick Stafford, the team built version 1 of this web and associated mobile application, working closely with communities in Southwestern PA to pilot the application.






