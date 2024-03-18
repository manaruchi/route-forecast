import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime
import os
import time
import numpy as np
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime, timedelta
import numpy as np
from scipy import interpolate

#Define Convenience Functions
def get_ecmwf_data(lat, lon):

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/ecmwf"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "precipitation", "weather_code", "surface_pressure", "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m", "surface_temperature", "temperature_1000hPa", "temperature_925hPa", "temperature_850hPa", "temperature_700hPa", "temperature_500hPa", "temperature_300hPa", "temperature_250hPa", "temperature_200hPa", "temperature_50hPa", "relative_humidity_1000hPa", "relative_humidity_925hPa", "relative_humidity_850hPa", "relative_humidity_700hPa", "relative_humidity_500hPa", "relative_humidity_300hPa", "relative_humidity_250hPa", "relative_humidity_200hPa", "relative_humidity_50hPa", "windspeed_1000hPa", "windspeed_925hPa", "windspeed_850hPa", "windspeed_700hPa", "windspeed_500hPa", "windspeed_300hPa", "windspeed_250hPa", "windspeed_200hPa", "windspeed_50hPa", "winddirection_1000hPa", "winddirection_925hPa", "winddirection_850hPa", "winddirection_700hPa", "winddirection_500hPa", "winddirection_300hPa", "winddirection_250hPa", "winddirection_200hPa", "winddirection_50hPa"],
        "wind_speed_unit": "kn"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(3).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(4).ValuesAsNumpy()
    hourly_surface_pressure = hourly.Variables(5).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(6).ValuesAsNumpy()
    hourly_cloud_cover_low = hourly.Variables(7).ValuesAsNumpy()
    hourly_cloud_cover_mid = hourly.Variables(8).ValuesAsNumpy()
    hourly_cloud_cover_high = hourly.Variables(9).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(10).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(11).ValuesAsNumpy()
    hourly_wind_gusts_10m = hourly.Variables(12).ValuesAsNumpy()
    hourly_surface_temperature = hourly.Variables(13).ValuesAsNumpy()
    hourly_temperature_1000hPa = hourly.Variables(14).ValuesAsNumpy()
    hourly_temperature_925hPa = hourly.Variables(15).ValuesAsNumpy()
    hourly_temperature_850hPa = hourly.Variables(16).ValuesAsNumpy()
    hourly_temperature_700hPa = hourly.Variables(17).ValuesAsNumpy()
    hourly_temperature_500hPa = hourly.Variables(18).ValuesAsNumpy()
    hourly_temperature_300hPa = hourly.Variables(19).ValuesAsNumpy()
    hourly_temperature_250hPa = hourly.Variables(20).ValuesAsNumpy()
    hourly_temperature_200hPa = hourly.Variables(21).ValuesAsNumpy()
    #hourly_temperature_50hPa = hourly.Variables(22).ValuesAsNumpy()
    hourly_relative_humidity_1000hPa = hourly.Variables(23).ValuesAsNumpy()
    hourly_relative_humidity_925hPa = hourly.Variables(24).ValuesAsNumpy()
    hourly_relative_humidity_850hPa = hourly.Variables(25).ValuesAsNumpy()
    hourly_relative_humidity_700hPa = hourly.Variables(26).ValuesAsNumpy()
    hourly_relative_humidity_500hPa = hourly.Variables(27).ValuesAsNumpy()
    hourly_relative_humidity_300hPa = hourly.Variables(28).ValuesAsNumpy()
    hourly_relative_humidity_250hPa = hourly.Variables(29).ValuesAsNumpy()
    hourly_relative_humidity_200hPa = hourly.Variables(30).ValuesAsNumpy()
    #hourly_relative_humidity_50hPa = hourly.Variables(31).ValuesAsNumpy()
    hourly_windspeed_1000hPa = hourly.Variables(32).ValuesAsNumpy()
    hourly_windspeed_925hPa = hourly.Variables(33).ValuesAsNumpy()
    hourly_windspeed_850hPa = hourly.Variables(34).ValuesAsNumpy()
    hourly_windspeed_700hPa = hourly.Variables(35).ValuesAsNumpy()
    hourly_windspeed_500hPa = hourly.Variables(36).ValuesAsNumpy()
    hourly_windspeed_300hPa = hourly.Variables(37).ValuesAsNumpy()
    hourly_windspeed_250hPa = hourly.Variables(38).ValuesAsNumpy()
    hourly_windspeed_200hPa = hourly.Variables(39).ValuesAsNumpy()
    #hourly_windspeed_50hPa = hourly.Variables(40).ValuesAsNumpy()
    hourly_winddirection_1000hPa = hourly.Variables(41).ValuesAsNumpy()
    hourly_winddirection_925hPa = hourly.Variables(42).ValuesAsNumpy()
    hourly_winddirection_850hPa = hourly.Variables(43).ValuesAsNumpy()
    hourly_winddirection_700hPa = hourly.Variables(44).ValuesAsNumpy()
    hourly_winddirection_500hPa = hourly.Variables(45).ValuesAsNumpy()
    hourly_winddirection_300hPa = hourly.Variables(46).ValuesAsNumpy()
    hourly_winddirection_250hPa = hourly.Variables(47).ValuesAsNumpy()
    hourly_winddirection_200hPa = hourly.Variables(48).ValuesAsNumpy()
    #hourly_winddirection_50hPa = hourly.Variables(49).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    d_vals, m_vals, y_vals, h_vals, date_vals = [],[],[],[], []
    for d in hourly_data['date'].values:
        cur_date = pd.Timestamp(d)
        cur_date_ist = cur_date + timedelta(hours=5, minutes=30)
        date_vals.append(cur_date_ist)
        d_vals.append(cur_date_ist.day)
        m_vals.append(cur_date_ist.month)
        y_vals.append(cur_date_ist.year)
        h_vals.append(cur_date_ist.hour)

    hourly_data['Date_IST'] = date_vals
    hourly_data['Day'] = d_vals
    hourly_data['Month'] = m_vals
    hourly_data['Year'] = y_vals
    hourly_data['Hour'] = h_vals
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["dew_point_2m"] = hourly_dew_point_2m
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["weather_code"] = hourly_weather_code
    hourly_data["surface_pressure"] = hourly_surface_pressure
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
    hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
    hourly_data["cloud_cover_high"] = hourly_cloud_cover_high
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
    hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
    hourly_data["surface_temperature"] = hourly_surface_temperature
    hourly_data["temperature_1000hPa"] = hourly_temperature_1000hPa
    hourly_data["temperature_925hPa"] = hourly_temperature_925hPa
    hourly_data["temperature_850hPa"] = hourly_temperature_850hPa
    hourly_data["temperature_700hPa"] = hourly_temperature_700hPa
    hourly_data["temperature_500hPa"] = hourly_temperature_500hPa
    hourly_data["temperature_300hPa"] = hourly_temperature_300hPa
    hourly_data["temperature_250hPa"] = hourly_temperature_250hPa
    hourly_data["temperature_200hPa"] = hourly_temperature_200hPa
    #hourly_data["temperature_50hPa"] = hourly_temperature_50hPa
    hourly_data["relative_humidity_1000hPa"] = hourly_relative_humidity_1000hPa
    hourly_data["relative_humidity_925hPa"] = hourly_relative_humidity_925hPa
    hourly_data["relative_humidity_850hPa"] = hourly_relative_humidity_850hPa
    hourly_data["relative_humidity_700hPa"] = hourly_relative_humidity_700hPa
    hourly_data["relative_humidity_500hPa"] = hourly_relative_humidity_500hPa
    hourly_data["relative_humidity_300hPa"] = hourly_relative_humidity_300hPa
    hourly_data["relative_humidity_250hPa"] = hourly_relative_humidity_250hPa
    hourly_data["relative_humidity_200hPa"] = hourly_relative_humidity_200hPa
    #hourly_data["relative_humidity_50hPa"] = hourly_relative_humidity_50hPa
    hourly_data["windspeed_1000hPa"] = hourly_windspeed_1000hPa
    hourly_data["windspeed_925hPa"] = hourly_windspeed_925hPa
    hourly_data["windspeed_850hPa"] = hourly_windspeed_850hPa
    hourly_data["windspeed_700hPa"] = hourly_windspeed_700hPa
    hourly_data["windspeed_500hPa"] = hourly_windspeed_500hPa
    hourly_data["windspeed_300hPa"] = hourly_windspeed_300hPa
    hourly_data["windspeed_250hPa"] = hourly_windspeed_250hPa
    hourly_data["windspeed_200hPa"] = hourly_windspeed_200hPa
    #hourly_data["windspeed_50hPa"] = hourly_windspeed_50hPa
    hourly_data["winddirection_1000hPa"] = hourly_winddirection_1000hPa
    hourly_data["winddirection_925hPa"] = hourly_winddirection_925hPa
    hourly_data["winddirection_850hPa"] = hourly_winddirection_850hPa
    hourly_data["winddirection_700hPa"] = hourly_winddirection_700hPa
    hourly_data["winddirection_500hPa"] = hourly_winddirection_500hPa
    hourly_data["winddirection_300hPa"] = hourly_winddirection_300hPa
    hourly_data["winddirection_250hPa"] = hourly_winddirection_250hPa
    hourly_data["winddirection_200hPa"] = hourly_winddirection_200hPa
    #hourly_data["winddirection_50hPa"] = hourly_winddirection_50hPa

    hourly_dataframe = pd.DataFrame(data = hourly_data, index = None)
    hourly_dataframe = hourly_dataframe.drop('date', axis = 1)
    return hourly_dataframe

def parsednt(df,d,t):
    day, month, year = d.split("-")
    day, month, year = int(day), int(month), int(year)
    hr = int(t.split(":")[0])
    minidf = df[(df['Day']==day)&(df['Month']==month)&(df['Year']==year)&(df['Hour']==hr)]
    return minidf, minidf['surface_pressure'].values[0]

def myround(x, base=5):
    x = int(x)
    return base * round(x/base)

def interp_for_levels(ht, vals, new_ht, is_wind_dir = False, round_to=5):
    if(is_wind_dir):
        wrapped_winds = np.unwrap(vals, period=360)
        f = interpolate.interp1d(ht, wrapped_winds ,kind="slinear")
        interpolated_vals = f(new_ht)
        actual_vals = []
        rounded_vals = []
        for w in interpolated_vals:
            if(w<0):
                actual_vals.append(w+360)
            else:
                actual_vals.append(w)
        for v in actual_vals:
            x = int(v)
            rounded_vals.append(10 * round(x/10))
        return rounded_vals
    else:
        f = interpolate.interp1d(ht, vals ,kind="slinear")
        interpolated_vals = f(new_ht)
        rounded_vals = []
        for v in interpolated_vals:
            x = int(v)
            rounded_vals.append(round_to * round(x/round_to))
        return rounded_vals

def prepdata(filter_df, new_ht):
    old_ht = [500,2500,5000,10000,18000,30000,35000,40000]
    upper_air_df = pd.DataFrame()
    upper_air_df['Levels'] = new_ht[::-1]
    wind_dir_list = []
    wind_speed_list = []
    temp_list = []
    for level in ['200hPa', '250hPa', '300hPa', '500hPa', '700hPa', '850hPa', '925hPa', '1000hPa'][::-1]:
        wind_dir_list.append(filter_df[f'winddirection_{level}'].values[0])
        wind_speed_list.append(filter_df[f'windspeed_{level}'].values[0])
        temp_list.append(int(filter_df[f'temperature_{level}'].values[0]))

    new_wind_dir = interp_for_levels(old_ht, wind_dir_list, new_ht, is_wind_dir = True)[::-1]
    new_wind_speed = interp_for_levels(old_ht, wind_speed_list, new_ht)[::-1]
    new_temp = interp_for_levels(old_ht, temp_list, new_ht, round_to = 1)[::-1]

    text_to_be_shown = []
    for y in range(len(new_wind_dir)):
        wwww = f"{new_wind_dir[y]:03d}/{new_wind_speed[y]:02d}({new_temp[y]:02d})"
        text_to_be_shown.append(wwww)


    return text_to_be_shown




st.set_page_config(initial_sidebar_state="collapsed", layout="wide", page_title='Route Planner')

if('route_name' in st.query_params.keys()):
    st.subheader(st.query_params['route_name'])
    route_df = pd.read_csv(os.path.join('routes', f'{st.query_params['route_name']}.csv'))
    route_df = route_df[route_df.columns[-6:]]

    levels = st.multiselect(
    'Levels to get data (ft): ',
    np.arange(1000,40000,500), [1000, 2000, 3000, 5000, 7000, 9000, 15000, 18000, 25000, 30000])

    finaldf = pd.DataFrame()
    pressuredf = pd.DataFrame()
    finaldf['Levels(ft)'] = levels[::-1]
    pressuredf['Levels(ft)'] = ['Min QNH']
    for i in range(len(route_df['Point Name'].values)):
        pt_name = route_df['Point Name'].values[i]
        lat, lon = route_df['Latitude'].values[i], route_df['Longitude'].values[i]


        minidf, qnh = parsednt(get_ecmwf_data(lat, lon), route_df['Date'].values[i], route_df['Time(IST)'].values[i])

        finaldf[f"{pt_name}({route_df['Date'].values[i]} {route_df['Time(IST)'].values[i]})"] = prepdata(minidf, levels)
        pressuredf[f"{pt_name}({route_df['Date'].values[i]} {route_df['Time(IST)'].values[i]})"] = [int(qnh)]

    st.dataframe(pd.concat([finaldf, pressuredf]))
