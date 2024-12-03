import streamlit as st
import pandas as pd
import plotly.express as px

backgroundColor="#FFFFFF"

#World development data, all at your fingertips.

st.set_page_config(page_title="Welcome to IWDM!",
    page_icon="🌐",
)

html_str_title = (f"<h1 style='text-align: center; color: black;'>World development indicators,</h1>")
html_str_title2 = (f"<h1 style='text-align: center; color: black;margin-top:-40px;'>all at your fingertips.</h1>")
st.html(html_str_title)
st.html(html_str_title2)

st.sidebar.success('Select a page above, or navigate using buttons on screen.')

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
                """
                <style>
                .centered-image {
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                }
                .caption {
                    text-align: center;
                    font-style: italic;
                    color: gray;
                }
                </style>
                """, 
                unsafe_allow_html=True
            )

    image_url = 'https://media.istockphoto.com/id/935746242/photo/mata-atlantica-atlantic-forest-in-brazil.jpg?s=612x612&w=0&k=20&c=NqE6m2Q8J2w6M7x7Pi8VxnMzLzq-HJQvCt5EMuvMU5o='

    st.markdown(f'<img src="{image_url}" class="centered-image" style="border: 4px solid black;margin-bottom: 10px;">', unsafe_allow_html=True)

    print_map_info = f"""<div style="text-align: center;">Graph and visualize an extensive database of individual sovereign development indicators against a time series or axis of your choosing.</div>"""

    st.markdown(print_map_info, unsafe_allow_html=True)

with col2:

    st.markdown(
                """
                <style>
                .centered-image {
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                }
                .caption {
                    text-align: center;
                    font-style: italic;
                    color: gray;
                }
                </style>
                """, 
                unsafe_allow_html=True
            )

    image_url = 'https://a.storyblok.com/f/53624/612x408/c5baf9c83b/iguassu-falls-brazil_500x400.jpg'

    st.markdown(f'<img src="{image_url}" class="centered-image" style="border: 4px solid black;margin-bottom: 10px;">', unsafe_allow_html=True)

    print_map_info = f"""<div style="text-align: center;">Compare parameter distributions with an interactive heatmap and time series display. Build your own testing block with countries of your choosing.</div>"""

    st.markdown(print_map_info, unsafe_allow_html=True)

with col3:

    st.markdown(
                """
                <style>
                .centered-image {
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                }
                .caption {
                    text-align: center;
                    font-style: italic;
                    color: gray;
                }
                </style>
                """, 
                unsafe_allow_html=True
            )

    image_url = 'https://bw.tokioschool.com/wp-content/uploads/2020/10/deep-learning-vs-machine-learning-612x408.jpg.webp'

    st.markdown(f'<img src="{image_url}" class="centered-image" style="border: 4px solid black;margin-bottom: 10px;">', unsafe_allow_html=True)

    print_map_info = f"""<div style="text-align: center;">Explore machine learning projections with synthetic data. Construct and train your own forecasting model, then deploy with predictions.</div>"""

    st.markdown(print_map_info, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    html_str_title3 = (f"<h2 style='text-align: center; color: black;margin-top:30px;'>Ready to get started?</h2>")
    st.html(html_str_title3)

col1, col2, col3, col4, col5 = st.columns(5)

with col2:
    if st.button("Single View"):
            st.switch_page("pages/Individual Mapper.py")
with col3:
     if st.button("Multi-View"):
        st.switch_page("pages/Regional Mapper.py")
with col4:
     if st.button("Sandbox"):
        st.switch_page("pages/ML_sandbox.py")