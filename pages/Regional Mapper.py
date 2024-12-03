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
from scipy import stats
import numpy as np

try:
    st.session_state['slider_value'] = st.session_state['slider_value']
except:
    st.session_state['slider_value'] = 2023

years = global_variables.years_list

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
     
    placeholder = f"<p style='text-align: center; color: black; margin-bottom: 15px;'>{''}</p>"
    st.html(placeholder)

    option_sel = st.multiselect(
        "Pick countries to compare or visualize.",
        ('Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru','Suriname','Uruguay', 'Venezuela'),
    )
     
    indicator_sel = st.selectbox(
        "Pick indicator to visualize.",
        global_variables.all_indicators,
    )
    
    #rfind units
    unit = 'None'

    if indicator_sel.rfind('(') != -1:
        unit = indicator_sel[indicator_sel.rfind('(') + 1:-1]

    indicator_unit = f"<p style='text-align: center; color: black; margin-bottom: -15px;font-weight:bold;'>{'Indicator Unit:'}</p>"
    st.html(indicator_unit)

    indicator_unit_2 = f"<p style='text-align: center; color: black; margin-bottom: -15px;'>{unit}</p>"
    st.html(indicator_unit_2)

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
            south_american_countries_selected.append(element)
        
        countries_list = []
        countries_data = []

        for country in south_american_countries_selected:
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
        data_df['Data'] = data_df['Data'].astype(float)

        fig = px.choropleth(data_df, 
                            locations="Country", 
                            locationmode="country names",
                            color="Data",
                            color_continuous_scale="Viridis",
                            )

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
            },
            coloraxis_colorbar=dict(
                title="Data Values",))
        
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
        data_df['Data'] = data_df['Data'].astype(float)

        fig = px.choropleth(data_df, 
                            locations="Country", 
                            locationmode="country names",
                            color="Data",
                            color_continuous_scale="Viridis",
                            )

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
            },
            coloraxis_colorbar=dict(
                title="Data Values",))
        
        st.plotly_chart(fig)

html_str_new_plot4 = (f"<h5 style='text-align: center; color: black;margin-top:-40px;'>Summary Statistics</h1>")
st.html(html_str_new_plot4)

col1, col2, col3, col4= st.columns(4)

with col1: #mean
    html_str_new_plot5 = (f"<h6 style='text-align: center; color: black;'>Mean:</h6>")
    st.html(html_str_new_plot5)
    
    col1_data_bank = data_df['Data'].to_numpy()
    mean = col1_data_bank.mean()

    html_str_new_plot5 = (f"<p style='text-align: center; color: black;margin-top:-20px'>{mean:.4f}</p>")
    st.html(html_str_new_plot5)

with col2: #std
    html_str_new_plot5 = (f"<h6 style='text-align: center; color: black;'>STD:</h6>")
    st.html(html_str_new_plot5)

    col2_data_bank = data_df['Data'].to_numpy()
    std = col2_data_bank.std()

    html_str_new_plot5 = (f"<p style='text-align: center; color: black;margin-top:-20px'>{std:.4f}</p>")
    st.html(html_str_new_plot5)

with col3: #median
    html_str_new_plot5 = (f"<h6 style='text-align: center; color: black;'>Median:</h6>")
    st.html(html_str_new_plot5)

    col4_data_bank = data_df['Data'].to_numpy()
    med = stats.median_abs_deviation(col4_data_bank)

    html_str_new_plot5 = (f"<p style='text-align: center; color: black;margin-top:-20px'>{med:.4f}</p>")
    st.html(html_str_new_plot5)


with col4: #iqr
    html_str_new_plot5 = (f"<h6 style='text-align: center; color: black;'>IQR:</h6>")
    st.html(html_str_new_plot5)

    col5_data_bank = data_df['Data'].to_numpy()
    iqr = stats.iqr(col5_data_bank)

    html_str_new_plot5 = (f"<p style='text-align: center; color: black;margin-top:-20px'>{iqr:.4f}</p>")
    st.html(html_str_new_plot5)

#html_str_new_plot4 = (f"<h5 style='text-align: center; color: black;'>Compare and plot metrics between countries.</h1>")
#st.html(html_str_new_plot4)

selected_choices = [indicator_sel]
resulting_values = []
indicators = []
resulting_frame = pd.DataFrame()
if 'Argentina' in countries_list:
        for element in selected_choices:
                resulting_values = []
                indicators = []
                index = global_variables.argentina_dataset.loc[global_variables.argentina_dataset['Indicator Name'] == element].index[0]
                for year in years:
                        val = global_variables.argentina_dataset.at[index, year]
                        if val == '':
                                resulting_values.append('N/A')
                        else:
                                resulting_values.append(global_variables.argentina_dataset.at[index, year])
                        indicators.append('Argentina')
                merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Country': indicators})
                resulting_frame = pd.concat([resulting_frame, merge_frame])
        
if 'Bolivia' in countries_list:
        for element in selected_choices:
                resulting_values = []
                indicators = []
                index = global_variables.bolivia_dataset.loc[global_variables.bolivia_dataset['Indicator Name'] == element].index[0]
                for year in years:
                        val = global_variables.bolivia_dataset.at[index, year]
                        if val == '':
                                resulting_values.append('N/A')
                        else:
                                resulting_values.append(global_variables.bolivia_dataset.at[index, year])
                        indicators.append('Bolivia')
                merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Country': indicators})
                resulting_frame = pd.concat([resulting_frame, merge_frame])
if 'Brazil' in countries_list:
        for element in selected_choices:
                resulting_values = []
                indicators = []
                index = global_variables.brazil_dataset.loc[global_variables.brazil_dataset['Indicator Name'] == element].index[0]
                for year in years:
                        val = global_variables.brazil_dataset.at[index, year]
                        if val == '':
                                resulting_values.append('N/A')
                        else:
                                resulting_values.append(global_variables.brazil_dataset.at[index, year])
                        indicators.append('Brazil')
                merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Country': indicators})
                resulting_frame = pd.concat([resulting_frame, merge_frame])
if 'Chile' in countries_list:
        for element in selected_choices:
                resulting_values = []
                indicators = []
                index = global_variables.chile_dataset.loc[global_variables.chile_dataset['Indicator Name'] == element].index[0]
                for year in years:
                        val = global_variables.chile_dataset.at[index, year]
                        if val == '':
                                resulting_values.append('N/A')
                        else:
                                resulting_values.append(global_variables.chile_dataset.at[index, year])
                        indicators.append('Chile')
                merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Country': indicators})
                resulting_frame = pd.concat([resulting_frame, merge_frame])
if 'Colombia' in countries_list:
        for element in selected_choices:
                resulting_values = []
                indicators = []
                index = global_variables.colombia_dataset.loc[global_variables.colombia_dataset['Indicator Name'] == element].index[0]
                for year in years:
                        val = global_variables.colombia_dataset.at[index, year]
                        if val == '':
                                resulting_values.append('N/A')
                        else:
                                resulting_values.append(global_variables.colombia_dataset.at[index, year])
                        indicators.append('Colombia')
                merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Country': indicators})
                resulting_frame = pd.concat([resulting_frame, merge_frame])
if 'Ecuador' in countries_list:
        for element in selected_choices:
                resulting_values = []
                indicators = []
                index = global_variables.ecuador_dataset.loc[global_variables.ecuador_dataset['Indicator Name'] == element].index[0]
                for year in years:
                        val = global_variables.ecuador_dataset.at[index, year]
                        if val == '':
                                resulting_values.append('N/A')
                        else:
                                resulting_values.append(global_variables.ecuador_dataset.at[index, year])
                        indicators.append('Ecuador')
                merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Country': indicators})
                resulting_frame = pd.concat([resulting_frame, merge_frame])
if 'Guyana' in countries_list:
        for element in selected_choices:
                resulting_values = []
                indicators = []
                index = global_variables.guyana_dataset.loc[global_variables.guyana_dataset['Indicator Name'] == element].index[0]
                for year in years:
                        val = global_variables.guyana_dataset.at[index, year]
                        if val == '':
                                resulting_values.append('N/A')
                        else:
                                resulting_values.append(global_variables.guyana_dataset.at[index, year])
                        indicators.append('Guyana')
                merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Country': indicators})
                resulting_frame = pd.concat([resulting_frame, merge_frame])
if 'Paraguay' in countries_list:
        for element in selected_choices:
                resulting_values = []
                indicators = []
                index = global_variables.paraguay_dataset.loc[global_variables.paraguay_dataset['Indicator Name'] == element].index[0]
                for year in years:
                        val = global_variables.paraguay_dataset.at[index, year]
                        if val == '':
                                resulting_values.append('N/A')
                        else:
                                resulting_values.append(global_variables.paraguay_dataset.at[index, year])
                        indicators.append('Paraguay')
                merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Country': indicators})
                resulting_frame = pd.concat([resulting_frame, merge_frame])
if 'Peru' in countries_list:
        for element in selected_choices:
                resulting_values = []
                indicators = []
                index = global_variables.peru_dataset.loc[global_variables.peru_dataset['Indicator Name'] == element].index[0]
                for year in years:
                        val = global_variables.peru_dataset.at[index, year]
                        if val == '':
                                resulting_values.append('N/A')
                        else:
                                resulting_values.append(global_variables.peru_dataset.at[index, year])
                        indicators.append('Peru')
                merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Country': indicators})
                resulting_frame = pd.concat([resulting_frame, merge_frame])
if 'Suriname' in countries_list:
        for element in selected_choices:
                resulting_values = []
                indicators = []
                index = global_variables.suriname_dataset.loc[global_variables.suriname_dataset['Indicator Name'] == element].index[0]
                for year in years:
                        val = global_variables.suriname_dataset.at[index, year]
                        if val == '':
                                resulting_values.append('N/A')
                        else:
                                resulting_values.append(global_variables.suriname_dataset.at[index, year])
                        indicators.append('Suriname')
                merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Country': indicators})
                resulting_frame = pd.concat([resulting_frame, merge_frame])
if 'Uruguay' in countries_list:
        for element in selected_choices:
                resulting_values = []
                indicators = []
                index = global_variables.uruguay_dataset.loc[global_variables.uruguay_dataset['Indicator Name'] == element].index[0]
                for year in years:
                        val = global_variables.uruguay_dataset.at[index, year]
                        if val == '':
                                resulting_values.append('N/A')
                        else:
                                resulting_values.append(global_variables.uruguay_dataset.at[index, year])
                        indicators.append('Uruguay')
                merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Country': indicators})
                resulting_frame = pd.concat([resulting_frame, merge_frame])
if 'Venezuela' in countries_list:
        for element in selected_choices:
                resulting_values = []
                indicators = []
                index = global_variables.venezuela_dataset.loc[global_variables.venezuela_dataset['Indicator Name'] == element].index[0]
                for year in years:
                        val = global_variables.venezuela_dataset.at[index, year]
                        if val == '':
                                resulting_values.append('N/A')
                        else:
                                resulting_values.append(global_variables.venezuela_dataset.at[index, year])
                        indicators.append('Venezuela')
                merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Country': indicators})
                resulting_frame = pd.concat([resulting_frame, merge_frame])

resulting_frame['Year'] = pd.to_numeric(resulting_frame['Year'], errors='coerce') 
resulting_frame['Value'] = pd.to_numeric(resulting_frame['Value'], errors='coerce')
resulting_frame['Country'] = (resulting_frame['Country']).astype(str)


#plot data
chart = alt.Chart(resulting_frame).mark_line().encode(
    x=alt.X('Year', title='Year', sort='ascending', scale=alt.Scale(domain=[1960, 2023])),
    y=alt.Y('Value', title='Value', axis=alt.Axis(tickCount=5)),
    color='Country',
    tooltip=['Year', 'Value', 'Country']
    ).interactive()

st.altair_chart(chart, use_container_width = True)