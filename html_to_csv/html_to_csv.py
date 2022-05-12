# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 15:49:54 2022

@author: apickett
"""

import pandas as pd
import re
import numpy as np

#read html and convert to pandas dataframe
website = 'https://www.notmar.gc.ca/publications/list-lights/inland-waters/i1082-en'

df = pd.read_html(website)

#separate latitude and longitude
df = df[0]
temp_col = df[3].str.split(r'\s{2,}')


#split string to save to something meaningful
location = re.split("list-lights/", website)
location1 = re.split("/n", location[1])

#create filename including todays date for recency purposes
from datetime import date
today = date.today()
todaysdate = today.strftime("%y%m%d")
filename = location1[0] + todaysdate + ".csv"

#create empty lists for notes, lats and longs
note = [] 
lat = [] 
lon = []

#loop through temp_col to extract notes, lats and longs and append them to lists
for i in range(len(temp_col)):
    if len(temp_col[i]) == 3: 
        note.append(temp_col[i][0])
        lat.append(temp_col[i][1])
        lon.append(temp_col[i][2])
    else:
        note.append(np.nan)
        lat.append(temp_col[i][0])
        lon.append(temp_col[i][1])

#create new lists for lat/longs in decimal degrees
new_lon = []
new_lat = []

#define a function to convert lats/longs to decmial degrees and then loop through
def conversion(old):
    new = old.split()
    return(float(new[0])+float(new[1])/60+float(new[2])/3600)

for i in range(len(lon)):
    new_lon.append(conversion(lon[i]))
    new_lat.append(conversion(lat[i]))
    
#replace old lat and long columns(df[2] is an empty column for some reason, df[3] contains lat and long
#info and notes) and add note column at end
df[2] = new_lat
df[3] = new_lon
df[11] = note

#multiply longitude values by negative 1
df[3] = -1 * df[3]

#find keywords and create new columns for aton identification
df.loc[df[1].str.contains('buoy', regex = True), 'aton'] = 'buoy'
df.loc[df[1].str.contains('light', regex = True), 'light'] = 'lighted'
df.loc[df[9].str.contains('tower', regex = True), 'aton'] = 'tower'
df.loc[df[9].str.contains('mast', regex = True), 'aton'] = 'mast'
df.loc[df[9].str.contains('Red', regex = True), 'buoy color'] =  'R'
df.loc[df[9].str.contains('Red and white', regex = True), 'buoy color'] =  'RW'
df.loc[df[9].str.contains('Green', regex = True), 'buoy color'] =  'G'
df.loc[df[9].str.contains('Yellow', regex = True), 'buoy color'] =  'Y'
df.loc[df[9].str.contains('Black, and yellow', regex = True), 'buoy color'] =  'BY'
df.loc[df[9].str.contains('Black and yellow', regex = True), 'buoy color'] =  'BY'
df.loc[df[9].str.contains('Black and red', regex = True), 'buoy color'] =  'BRB'

#df['buoy color'][df['buoy color'].isna()] = 'W' 

#combine into identifying column
df['combined'] = df['light'] + ' ' + df[5] + ' ' + df['aton'] + df['buoy color']

df.to_csv(filename)