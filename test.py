import sqlite3



from serpapi import GoogleSearch
import plotly as plotly
import pandas as pd
import json
import plotly.express as px
from flask import Flask, render_template, request

conn = sqlite3.connect("Database.db")
cursor = conn.cursor()
cursor.execute("SELECT author_id from Citations ;")
rows = cursor.fetchall()

for row in rows:
    params = {
    "engine": "google_scholar_author",
    "author_id": (row[0]),
    "api_key": "5a3cc089aefdbfd432472a4fde28842a9f356532de5cb3e8801c777826992bec"
    }

cited_by = None

search = GoogleSearch(params)
results = search.get_dict()
results["cited_by"]['graph']
print((results))

   

def notdash(data=results):
  
    df = pd.DataFrame(data)
    fig = px.bar(df, x='year', y='citations',
                 barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    print(graphJSON)
    return graphJSON
    
  