# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 12:38:22 2022

@author: EDEME_D
"""

import os
import pandas as pd
from geopy.geocoders import Nominatim
import streamlit as st
import numpy as np
import time

uploaded_file = st.file_uploader('upload csv file')


n = 500
i = 0
missing = 0
if uploaded_file is not None:
    
    coal_plants = pd.read_csv(uploaded_file, encoding = 'unicode_escape')
    
    coal_plants = coal_plants[0:n]
    
    coal_plants_locations = [] 
    coal_plants_lat = [] 
    coal_plants_long = [] 
    
    geolocator = Nominatim(user_agent="example app")
    
    
    for index, row in coal_plants[0:n].iterrows():
        i += 1
        if row['B'] is not np.nan:
            sentence = row['B'] + ' ' + row['STATE'] + ' ' + row['COUNTRY']
        else:
            sentence = row['A'] + ' ' + row['STATE'] + ' ' + row['COUNTRY']
        location = geolocator.geocode(sentence)
        time.sleep(1)
# =============================================================================
#         st.write(i)
#         st.write(location)
#         st.write('-------')
# =============================================================================
        
        if location == None:
            if row['B'] is not np.nan:
                sentence = row['B'] + ' ' + row['COUNTRY']
            else:
                sentence = row['A'] + ' ' + row['COUNTRY']
            
            location = geolocator.geocode(sentence)
            time.sleep(1)
# =============================================================================
#             st.write(i)
#             st.write(location)
#             st.write('-------')
# =============================================================================
            
            if location == None:
                coal_plants_locations.append("Not Found")
                coal_plants_lat.append("Not Found")
                coal_plants_long.append("Not Found")
            else:
                coal_plants_locations.append(location)
                coal_plants_lat.append(location.latitude)
                coal_plants_long.append(location.longitude)
                
        else:
            coal_plants_locations.append(location)
            coal_plants_lat.append(location.latitude)
            coal_plants_long.append(location.longitude)
        
        if i%10==0:
            st.write(i)

    coal_plants['locations'] = coal_plants_locations
    coal_plants['latitude'] = coal_plants_lat
    coal_plants['longitude'] = coal_plants_long
    
# =============================================================================
#     if i%10==0:
#         coal_plants.to_csv('coal_plants.csv')
#         
#         
# =============================================================================
    
    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')
    
    
    coal_plants = convert_df(coal_plants)
    
    st.download_button(
        "Press to Download",
        coal_plants,
        "file.csv",
        "text/csv",
        key='download-csv'
    ) 
