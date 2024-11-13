import streamlit as st
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import pandas as pd

st.markdown("<h1 style='text-align: center; color: black;'>Individual Country Mapper</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: black;'>Explore top-down overviews of specific countries.</h1>", unsafe_allow_html=True)

bynames = {'Argentina': 'República Argentina', 
           'Bolivia':'Estado Plurinacional de Bolivia',
           'Brazil':'Estado do Brasil',
           'Chile':'República de Chile',
           'Colombia':'República de Colombia', 
           'Ecuador':'República del Ecuador',
           'Guyana':'Co-operative Republic of Guyana',
           'Peru':'República del Perú',
           'Paraguay':'República del Paraguay',
           'Suriname':'The Republic of Suriname',
           'Uruguay':'República Oriental del Uruguay',
           'Venezuela':'República Bolivariana de Venezuela'}

option = st.selectbox(
    "Pick a country to explore.",
    ("Placeholder", "Argentina", 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Peru', 'Paraguay', 'Suriname', 'Uruguay', 'Venezuela'),
)

if option != 'Placeholder':
    col1, col2, col3 , col4, col5 = st.columns(5)

    st.markdown(
    """
    <style>
    .stButton>button {
        width: 200px;
        height: 50px;
        font-size: 20px;
    }
    </style>
    """, 
    unsafe_allow_html=True
)
    columns = st.columns((2, 1, 2))
    button_pressed = columns[1].button('Generate insights!')

    if button_pressed:
        html_str = f"""<h2 style='text-align: center; color: black;'>{option}</h2>"""
        st.markdown(html_str, unsafe_allow_html=True)

        #italicize country name
        get_name = bynames[option]
        country_byname = f"""<h4 style='text-align: center; color: black;'><em>{get_name}</em></h4>"""
        st.markdown(country_byname, unsafe_allow_html=True)

else: 
    st.success('Select a country above to proceed.')


    