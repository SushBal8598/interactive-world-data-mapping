import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import altair as alt
from vega_datasets import data

#Initialize the WORLD dataset (general stuffs)
html_str_title = (f"<h1 style='text-align: center; color: black;'>Individual Regional Mapper</h1>")
st.html(html_str_title)

html_str_subtitle = (f"<h5 style='text-align: center; color: black;'>Explore the world of maps and visualization.</h1>")
st.html(html_str_subtitle)

col1, col2 = st.columns(2)

with col1:
    countries = alt.topo_feature(data.world_110m.url, 'countries')
    print(countries)

with col2:

    option = st.selectbox(
        "Pick a region to visualize.",
        ("Placeholder", "South America (Default)"),
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