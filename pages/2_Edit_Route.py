import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime
import os
import time

st.set_page_config(initial_sidebar_state="collapsed", page_title='Edit Route - Route Planner')


if('route_name' in st.query_params.keys()):
    st.subheader(st.query_params['route_name'])

    if(os.path.exists(os.path.join('routes', f'{st.query_params['route_name']}.csv'))):
        route_df = pd.read_csv(os.path.join('routes', f'{st.query_params['route_name']}.csv'))
        route_df = route_df[route_df.columns[-6:]]
        route_data_editor = st.data_editor(route_df, num_rows="dynamic", use_container_width=True)

        if(st.button("Update Route")):
            with st.spinner("Saving route..."):
                route_data_editor.to_csv(os.path.join('routes', f'{st.query_params['route_name']}.csv'))
                time.sleep(2)
            st.toast('✅ Route Saved Successfully!')

        if(st.button("Delete Route")):
            with st.spinner("Deleting route..."):
                os.remove(os.path.join('routes', f'{st.query_params['route_name']}.csv'))
                time.sleep(2)
            st.toast('✅ Route Deleted Successfully!')
            st.rerun()




    else:
        st.error("❌ Route not found.")



else:
    st.error("❌ No Routes Defined!")
