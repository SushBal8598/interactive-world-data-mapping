import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import altair as alt
from vega_datasets import data
import json
import requests
import global_variables

#Initialize the WORLD dataset (general stuffs)
html_str_title = (f"<h1 style='text-align: center; color: black;'>Individual Regional Mapper</h1>")
st.html(html_str_title)

html_str_subtitle = (f"<h5 style='text-align: center; color: black;'>Explore the world of maps and visualization.</h1>")
st.html(html_str_subtitle)

south_american_countries_dict = {
    'Argentina':32, #argentina
    'Brazil':76, #brazil
    'Bolivia':68, #bolivia
    'Chile': 152, #chile
    'Colombia': 170, #colombia
    'Ecuador': 218,
    'Guyana': 328,
    'Paraguay': 600,
    'Peru': 604,
    'Venezuela': 862,
    'Uruguay': 858,
    'Suriname': 740
} #fill with exact IDs

num_reverse = {
    32:'Argentina', #argentina
    76:'Brazil', #brazil
    68:'Bolivia', #bolivia
    152:'Chile', #chile
    170:'Colombia', #colombia
    218:'Ecuador',
    328:'Guyana',
    600:'Paraguay',
    604:'Peru',
    862:'Venezuela',
    858:'Uruguay',
    740:'Suriname'
} 

south_american_countries_selected = [
    32, #argentina
    76, #brazil
    68, #bolivia
    152, #chile
    170, #colombia
    218, #ecuador
    328, #guyana 
    600, #paraguay
    604, #peru
    862, #venezuela
    858, #uruguay,
    740 #suriname
 ]

countries = alt.topo_feature(data.world_110m.url, 'countries')
    
# Load the world map data

prelim_chart = alt.Chart(countries).transform_filter(
        alt.FieldOneOfPredicate(field='id', oneOf=south_american_countries_selected) #https://altair-viz.github.io/user_guide/generated/core/altair.FieldOneOfPredicate.html
    ).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project(
    "naturalEarth1"
).interactive() #encode

col1, col2 = st.columns(2)

with col1:
     
     option_sel = st.multiselect(
        "Pick countries to compare or visualize.",
        ('Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru','Suriname','Uruguay', 'Venezuela'),
    )
     
     indicator_sel = st.selectbox(
        "Pick indicator to visualize.",
        global_variables.all_indicators,
    )
    
with col2:

    if option_sel != []:
        south_american_countries_selected = []
        for element in option_sel:
            south_american_countries_selected.append(south_american_countries_dict[element])
        
        prelim_chart = alt.Chart(countries).transform_filter(
                alt.FieldOneOfPredicate(field='id', oneOf=south_american_countries_selected) #https://altair-viz.github.io/user_guide/generated/core/altair.FieldOneOfPredicate.html
            ).mark_geoshape(
            fill='lightgray',
            stroke='white'
        ).project(
            "naturalEarth1"
        ).interactive() #encode

        st.altair_chart(prelim_chart, use_container_width=True)

    else:
        prelim_chart = alt.Chart(countries).transform_filter(
                alt.FieldOneOfPredicate(field='id', oneOf=south_american_countries_selected) #https://altair-viz.github.io/user_guide/generated/core/altair.FieldOneOfPredicate.html
            ).mark_geoshape(
            fill='lightgray',
            stroke='white'
        ).project(
            "naturalEarth1"
        )

        print(countries)
        st.altair_chart(prelim_chart, use_container_width=True)