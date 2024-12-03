import streamlit as st
import pandas as pd
import plotly.express as px

backgroundColor="#FFFFFF"

st.set_page_config(page_title="Welcome to IWDM!",
    page_icon="🌐",
)

st.title("Welcome to Interactive World Data Mapping!")
st.sidebar.success('Select a page above, or navigate using buttons on screen.')

st.write(
    "Demo test main view, with buttons linking to single-country and multi-country view."
)

if st.button("Single View"):
    st.switch_page("pages/Individual Mapper.py")
elif st.button("Multi-View"):
    st.switch_page("pages/Regional Mapper.py")