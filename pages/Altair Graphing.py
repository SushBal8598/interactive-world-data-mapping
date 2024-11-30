import streamlit as st
import altair as alt
import global_variables

try:
        indiv_title = (f"<h1 style='text-align: center; color: black;margin-bottom: -50px;'>Individual Visualization:</h1>")
        st.html(indiv_title)

        named_title = (f"<h1 style='text-align: center; color: black; text-decoration: underline;'>{st.session_state.option}</h1>")
        st.html(named_title)
except:
        st.info('Navigate to Individual Mapper first.')

col1,col2 = st.columns(2)

with col1:
        st.html("<h6 style='text-align: center; color: black;margin-bottom: -25px;'>Step 1: Input Query</h6>")

        option_mapping = st.selectbox(
        "Select a pre-loaded statistics set, or continue with custom.",
        ("Poverty", "Education","Agriculture","Custom"),
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

with col2:
        st.html("<h6 style='text-align: center; color: black;margin-bottom: -25px;'>Step 2: Validate Request</h6>")
#test global stuff      
#st.write(global_variables.df) #successful; should be able to initialize as necessary