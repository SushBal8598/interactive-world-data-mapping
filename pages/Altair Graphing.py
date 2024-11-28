import streamlit as st
import altair as alt
import global_variables

try:
        st.title(st.session_state.option)
except:
        st.info('Navigate to Individual Mapper first.')

col1,col2 = st.columns(2)

with col1:
        option_mapping = st.selectbox(
        "Select a pre-loaded statistics set, or continue with custom.",
        ("Poverty", "Custom"),
)
        
        if option_mapping == 'Custom':
            option_stats = st.selectbox(
        "Select custom statistics to plot.",
        ("Num1", "Num2"),
)

        option_library = st.selectbox(
        "Select a plot to graph against.",
        ("Scatterplot", "Lineplot", 'Boxplot', 'Bubble Chart'),
)

#test global stuff      
st.write(global_variables.df) #successful; should be able to initialize as necessary