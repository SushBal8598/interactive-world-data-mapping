import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import altair as alt
from vega_datasets import data
import json
import requests
import global_variables
import pandas as pd
import plotly
import plotly.express as px

try:
    st.session_state['slider_value'] = st.session_state['slider_value']
except:
    st.session_state['slider_value'] = 2023

#Initialize the WORLD dataset (general stuffs)
html_str_title = (f"<h1 style='text-align: center; color: black;'>Regional Mapper</h1>")
st.html(html_str_title)

html_str_subtitle = (f"<h5 style='text-align: center; color: black;'>Explore the world of maps and visualization.</h1>")
st.html(html_str_subtitle)

sa_countries = ['Argentina', #argentina
    'Brazil', #brazil
    'Bolivia', #bolivia
    'Chile', #chile
    'Colombia', #colombia
    'Ecuador',
    'Guyana',
    'Paraguay',
    'Peru',
    'Venezuela',
    'Uruguay',
    'Suriname']

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
    
    slider_value = st.slider(label="", 
            min_value=1960, 
            max_value=2023,
            value= st.session_state['slider_value'])

    if slider_value == 2023:
        st.info('Choose a year to generate insights for.')

    if 'slider_value' not in st.session_state:
        st.session_state['slider_value'] = 2023

    if slider_value != st.session_state['slider_value']:
        st.session_state['slider_value'] = slider_value
        st.rerun()

    my_year = str(st.session_state['slider_value'])
    
with col2:

    if option_sel != []:

        south_american_countries_selected = []
        for element in option_sel:
            south_american_countries_selected.append(south_american_countries_dict[element])
        
        # Sample data
        data = {'country': ['United States', 'Canada', 'Mexico'],
        'value': [10, 8, 6]}
        df = pd.DataFrame(data)

        # Create the heatmap
        fig = px.choropleth(df, 
                            locations="country", 
                            locationmode="country names",
                            color="value",
                            color_continuous_scale="Viridis")

        fig.update_geos(
            scope="south america",  # Set the scope to Europe
            showland=True,   # Show land
            landcolor="lightgray",
            showcoastlines=True,
            coastlinecolor="white",
            projection_type="natural earth",
        )
        st.plotly_chart(fig)

    else:

        #acquire data

        countries_list = []
        countries_data = []

        for country in sa_countries:
            if country == 'Argentina':
                index = global_variables.argentina_dataset.loc[global_variables.argentina_dataset['Indicator Name'] == indicator_sel].index[0]
                val = global_variables.argentina_dataset.at[index, my_year]
                if val == '':
                    val = 0
                countries_list.append('Argentina')
                countries_data.append(val)
            elif country == 'Bolivia':
                index = global_variables.bolivia_dataset.loc[global_variables.bolivia_dataset['Indicator Name'] == indicator_sel].index[0]
                val = global_variables.bolivia_dataset.at[index, my_year]
                if val == '':
                    val = 0
                countries_list.append('Bolivia')
                countries_data.append(val)
            elif country == 'Brazil':
                index = global_variables.brazil_dataset.loc[global_variables.brazil_dataset['Indicator Name'] == indicator_sel].index[0]
                val = global_variables.brazil_dataset.at[index, my_year]
                if val == '':
                    val = 0
                countries_list.append('Brazil')
                countries_data.append(val)
            elif country == 'Colombia':
                index = global_variables.colombia_dataset.loc[global_variables.colombia_dataset['Indicator Name'] == indicator_sel].index[0]
                val = global_variables.colombia_dataset.at[index, my_year]
                if val == '':
                    val = 0
                countries_list.append('Colombia')
                countries_data.append(val)
            elif country == 'Chile':
                index = global_variables.chile_dataset.loc[global_variables.chile_dataset['Indicator Name'] == indicator_sel].index[0]
                val = global_variables.chile_dataset.at[index, my_year]
                if val == '':
                    val = 0
                countries_list.append('Chile')
                countries_data.append(val)
            elif country == 'Ecuador':
                index = global_variables.ecuador_dataset.loc[global_variables.ecuador_dataset['Indicator Name'] == indicator_sel].index[0]
                val = global_variables.ecuador_dataset.at[index, my_year]
                if val == '':
                    val = 0
                countries_list.append('Ecuador')
                countries_data.append(val)
            elif country == 'Guyana':
                index = global_variables.guyana_dataset.loc[global_variables.guyana_dataset['Indicator Name'] == indicator_sel].index[0]
                val = global_variables.guyana_dataset.at[index, my_year]
                if val == '':
                    val = 0
                countries_list.append('Guyana')
                countries_data.append(val)
            elif country == 'Paraguay':
                index = global_variables.paraguay_dataset.loc[global_variables.paraguay_dataset['Indicator Name'] == indicator_sel].index[0]
                val = global_variables.paraguay_dataset.at[index, my_year]
                if val == '':
                    val = 0
                countries_list.append('Paraguay')
                countries_data.append(val)
            elif country == 'Peru':
                index = global_variables.peru_dataset.loc[global_variables.peru_dataset['Indicator Name'] == indicator_sel].index[0]
                val = global_variables.peru_dataset.at[index, my_year]
                if val == '':
                    val = 0
                countries_list.append('Peru')
                countries_data.append(val)
            elif country == 'Suriname':
                index = global_variables.suriname_dataset.loc[global_variables.suriname_dataset['Indicator Name'] == indicator_sel].index[0]
                val = global_variables.suriname_dataset.at[index, my_year]
                if val == '':
                    val = 0
                countries_list.append('Suriname')
                countries_data.append(val)
            elif country == 'Uruguay':
                index = global_variables.uruguay_dataset.loc[global_variables.uruguay_dataset['Indicator Name'] == indicator_sel].index[0]
                val = global_variables.uruguay_dataset.at[index, my_year]
                if val == '':
                    val = 0
                countries_list.append('Uruguay')
                countries_data.append(val)
            elif country == 'Venezuela':
                index = global_variables.venezuela_dataset.loc[global_variables.venezuela_dataset['Indicator Name'] == indicator_sel].index[0]
                val = global_variables.venezuela_dataset.at[index, my_year]
                if val == '':
                    val = 0
                countries_list.append('Venezuela')
                countries_data.append(float(val))
        
        data_df = pd.DataFrame({'Country':countries_list, 'Data':countries_data})

        fig = px.choropleth(data_df, 
                            locations="Country", 
                            locationmode="country names",
                            color="Data",
                            color_continuous_scale="Viridis",)

        fig.update_geos(
            scope="south america",
            showland=True,   # Show land
            landcolor="lightgray",
            showcoastlines=True,
            coastlinecolor="white",
            projection_type="natural earth",
        )

        fig.update_layout(
            title={
            'text': "Generated Heatmap: South America",
            'x': 0.5,
            'xanchor': 'center'
            })
        
        st.plotly_chart(fig)
        
html_str_new_plot4 = (f"<h5 style='text-align: center; color: black;'>Compare and plot metrics between countries.</h1>")
st.html(html_str_new_plot4)