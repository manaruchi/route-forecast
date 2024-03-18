import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime
import os
import time
from glob import glob

st.set_page_config(initial_sidebar_state="collapsed", page_title='Route Planner')

st.header("Route Plotter")

with st.container(border=True):
    col1, col2, col3 = st.columns([4,9,3])
    col1.caption('Want to add a new route?')
    col3.page_link("pages/1_New_Route.py", label="Add Route", icon="🛫")


st.subheader("Available Routes")

#List of available routes
routes_list = glob(os.path.join('routes', '*.csv'))

route_list_table = "<table id='newtable'><th class='first_header'>Route Name</th><th class='second_header'>Edit/Delete</th><th class='third_header'>Report</th>"

for route in routes_list:
    new_row = f"<tr><td>{os.path.basename(route).split(".")[0]}</td><td><a href='/Edit_Route?route_name={os.path.basename(route).split(".")[0].replace(" ", "_")}'>📝</a>️</td><td>️<a href='/Report?route_name={os.path.basename(route).split(".")[0].replace(" ", "_")}'>🌩</a></td></tr>"
    route_list_table = route_list_table + new_row


tablemd = route_list_table + "</table>"


st.markdown(tablemd, unsafe_allow_html=True)

#Apply Styles
st.markdown(
    """
<style>
    div[class="st-emotion-cache-1xw8zd0 e1f1d6gn0"]{
        border: 2px solid #438DDC;
        display: flex;

    }
    .st-emotion-cache-pe5sya e1nzilvr5 > p{
    font-size: 20px;
    }

    #newtable{
        width: 100%;
    }

    .first_header{
        width: 80%;
    }
    .second_header, .third_header{
    width: 10%;
    text-align: center;
    }
    th{
    background-color: #1d3e57;
    }
    a{
    text-decoration: none;
    }
</style>
""",
    unsafe_allow_html=True,
)
