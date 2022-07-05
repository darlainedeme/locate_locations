# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:02:55 2022

@author: EDEME_D
"""

import requests
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
from urllib.parse import quote
import streamlit as st

# uploaded_file = 'All_coal_plant_OPR_processed.csv'
uploaded_file = st.file_uploader('upload csv file')
if uploaded_file is not None:
    coal_plants = pd.read_csv(uploaded_file, encoding = 'unicode_escape')
    n = 10
    i = 0
    #wb = load_workbook(filepath)
    #sheet = wb["Envision"]
    #wb["Elec_Sub"]
    #cell = sheet.cell(2,20)
    for index, row in coal_plants[0:n].iterrows():
        i += 1
        if row['B'] is not np.nan:
            sentence = row['B'] + ' ' + row['STATE'] + ' ' + row['COUNTRY']
        else:
            sentence = row['A'] + ' ' + row['STATE'] + ' ' + row['COUNTRY']
        url = 'https://nominatim.openstreetmap.org/search?query=' + quote(sentence)
        resp = requests.request("Get",url)
        if (resp.status_code != 404) :
            strRes = resp.text
            st.write(i)
            st.write(strRes)
            st.write('-------')
            root = ET.fromstring(strRes)
