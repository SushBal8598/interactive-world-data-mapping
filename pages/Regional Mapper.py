import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import altair as alt
from vega_datasets import data
import json
import requests

#Initialize the WORLD dataset (general stuffs)
html_str_title = (f"<h1 style='text-align: center; color: black;'>Individual Regional Mapper</h1>")
st.html(html_str_title)

html_str_subtitle = (f"<h5 style='text-align: center; color: black;'>Explore the world of maps and visualization.</h1>")
st.html(html_str_subtitle)

south_american_countries_dict = {
    32: 'Argentina', #argentina
    76: 'Brazil', #brazil
    68: 'Bolivia', #bolivia
    152: 'Chile', #chile
    170: 'Colombia', #colombia

} #fill with exact IDs

south_american_countries = [
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
 ] #fill with exact IDs

countries = alt.topo_feature(data.world_110m.url, 'countries')
    
# Load the world map data

prelim_chart = alt.Chart(countries).transform_filter(
        alt.FieldOneOfPredicate(field='id', oneOf=south_american_countries) #https://altair-viz.github.io/user_guide/generated/core/altair.FieldOneOfPredicate.html
    ).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project(
    "naturalEarth1"
)

col1, col2 = st.columns(2)

with col1:
    st.altair_chart(prelim_chart, use_container_width=True)
    
with col2:

    option = st.multiselect(
        "Pick countries to compare or visualize.",
        ('Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru','Suriname','Uruguay', 'Venezuela'),
    )

    if option == 'South America (Default)':
        st.write('Visualizing South America...')

        '''# Plot the world map
        world.plot(figsize=(10, 6))

        # Customize the plot (optional)
        plt.title('World Map')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')

        # Show the plot
        plt.show()'''