import streamlit as st
import requests
import pandas
from streamlit.components.v1 import *
from io import BytesIO
import random
import altair as alt
import pandas as pd
import numpy as np

st.set_page_config(layout='wide')

st.markdown("<center><h1 style='align-text:center'><u>Dashboard</u></h1><center>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    col_a1, col_c1 = st.columns([1,1])
    with col_c1:
        st.header("Awesome Cat 1")
        data2 = requests.get("https://cataas.com/cat?height=500&width=400")
        kitty = st.image(BytesIO(data2.content))
with col2:
    col_a2, col_b2, col_c2 = st.columns([1,100,1])
    with col_b2:
        st.markdown("<center><h2 style='align-text:center'>U.S. Holidays</h2><center>", unsafe_allow_html=True)
        data = requests.get("https://date.nager.at/api/v2/publicholidays/2020/US").json()
        df = []
        for i in range(0, len(data)):
            df.append(data[i])

        st.dataframe(df, width=900, height=400)
with col3:
    col_a3, col_c3 = st.columns([1,1])
    with col_a3:
        st.header("Awesome Cat 2")
        data2 = requests.get("https://cataas.com/cat?height=500&width=400")
        kitty = st.image(BytesIO(data2.content))

st.divider()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.header("Wanted by FBI")
    data3 = requests.get("http://api.fbi.gov/wanted/v1/list").json()
    rando = random.randrange(0,int(data3["total"]),1)

    global pgCheck
    pgCheck = 0
    pg = 1
    for x in range(0,rando):
        pgCheck = pgCheck + 1
        if pgCheck == 19:
            pg = pg + 1
            pgCheck = 0
    data3 = requests.get("https://api.fbi.gov/wanted/v1/list?page={0}".format(pg)).json()

    ##st.write(pg)
    ##st.write(rando)
    ##st.write(pgCheck)

    #st.write(data3)
    try:
        st.image(data3["items"][pgCheck]["images"][0]["original"], width=270)
    except:
        pgCheck = 0
        st.image(data3["items"][pgCheck]["images"][0]["original"], width=270)

    with st.container(height=250, border=False):
        if data3["items"][pgCheck]["warning_message"] != None:
            try:
                st.markdown("<b style='color:red'>" + data3["items"][pgCheck]["warning_message"] + "</b>", unsafe_allow_html=True)
            except:
                pgCheck = 0
                st.markdown("<b style='color:red'>" + data3["items"][pgCheck]["warning_message"] + "</b>", unsafe_allow_html=True)

        if data3["items"][pgCheck]["title"] != None:
            st.markdown("<p>Name: " + data3["items"][pgCheck]["title"] + "</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p>Name: Unknown</p>", unsafe_allow_html=True)

        if data3["items"][pgCheck]["sex"] != None:
            st.markdown("<p>Gender: " + data3["items"][pgCheck]["sex"] + "</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p>Gender: Unknown</p>", unsafe_allow_html=True)

        if data3["items"][pgCheck]["race"] != None:
            st.markdown("<p>Race: " + data3["items"][pgCheck]["race"] + "</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p>Race: Unknown</p>", unsafe_allow_html=True)
        if data3["items"][pgCheck]["eyes"] != None:
            st.markdown("<p>Eye Color: " + data3["items"][pgCheck]["eyes"] + "</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p>Eye Color: Unknown</p>", unsafe_allow_html=True)
with col2:
    hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
    st.header(f'Map of Uber Pickups at {hour_to_filter}:00')

    DATE_COLUMN = 'date/time'
    DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

    @st.cache_data
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
        return data

    data = load_data(1000)

    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
    st.map(filtered_data)

with col3:
    st.header('NYC Uber Pickups (Bar Graph)')

    DATE_COLUMN = 'date/time'
    DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

    hist_values = np.histogram(
        data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

    st.bar_chart(hist_values)
with col4:
    st.header('NYC Uber Pickups (Scatter Plot)')

    DATE_COLUMN = 'date/time'
    DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

    hist_values = np.histogram(
        data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

    st.scatter_chart(hist_values)
