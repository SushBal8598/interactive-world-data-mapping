import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt

#Initialize the WORLD dataset (general stuffs)
'''url = "ne_110m_admin_0_countries.shp"

world = gpd.read_file(url)'''

st.title('Regional Mapper')

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