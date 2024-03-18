import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime
import os
import time

st.set_page_config(initial_sidebar_state="collapsed", layout="wide", page_title='Route Planner')

st.header("Route Plotter")
st.caption("Add line feature on the map to plot the route")

col1, col2 = st.columns(2)

m = folium.Map(location=[24.57, 76.89], zoom_start=4)


Draw(export=True).add_to(m)

with col1:
    output = st_folium(m, width=700, height=500)
col2.subheader('Route Information')

if(output["last_active_drawing"]):
    coordinates = output["last_active_drawing"]['geometry']['coordinates']




    if(len(coordinates)>0):
        lat_list = []
        lon_list = []
        routedf = pd.DataFrame()
        routedf['Point Name'] = [f"Point {x}" for x in range(1, len(coordinates)+1)]
        for c in coordinates:
            lat_list.append(c[1])
            lon_list.append(c[0])

        today = datetime.now()
        routedf['Latitude'] = lat_list
        routedf['Longitude'] = lon_list
        routedf['Date'] = [f"{today.day:02d}-{today.month:02d}-{today.year}"] * len(coordinates)
        routedf['Time(IST)'] = ["00:00"] * len(coordinates)
        routedf['Remarks'] = ["Waypoint"] * len(coordinates)

        route_name = col2.text_input("Route Name:")
        route_data_editor = col2.data_editor(routedf, num_rows="dynamic", use_container_width=True)

        if(col2.button('Save Route Information')):
            if(os.path.exists(os.path.join('routes', f'{route_name}.csv'))):
                st.toast("❌ Route of same name already exists!!")
            elif(route_name==""):
                st.toast("❌ Route Name can not be blank.")
            else:
                with st.spinner("Saving route..."):
                    route_data_editor.to_csv(os.path.join('routes', f'{route_name.replace(" ", "_")}.csv'))
                    time.sleep(2)
                st.toast('✅ Route Saved Successfully!')


else:

    col2.info("No routes added.")
