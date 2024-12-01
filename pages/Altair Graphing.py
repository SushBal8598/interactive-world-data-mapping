import streamlit as st
import altair as alt
import global_variables

try:
        indiv_title = (f"<h1 style='text-align: center; color: black;margin-bottom: -50px;'>Individual Visualization:</h1>")
        st.html(indiv_title)

        named_title = (f"<h1 style='text-align: center; color: black; text-decoration: underline;'>{st.session_state.option}</h1>")
        st.html(named_title)

        col1,col2 = st.columns(2)

        with col1:
                st.html("<h6 style='text-align: center; color: black;margin-bottom: -25px;'>Step 1: Input Query</h6>")

                option_mapping = st.selectbox(
                "Select a pre-loaded statistics set, or continue with custom.",
                ("Custom", "Poverty", "Education","Land and Agriculture","Exports, Imports, and Trade", "War and Mortality", "Economy", "Health and Disease", "Politics and Aid"),
        )

                option_library = st.selectbox(
                "Select a plot to graph against.",
                ("Scatterplot", "Lineplot", 'Boxplot', 'Bubble Chart'),
        )
                option_independent = st.selectbox(
                "Select the independent variable.",
                ("Year (Time Series)"),
                )

        with col2:
                st.html("<h6 style='text-align: center; color: black;margin-bottom: -25px;'>Step 2: Validate Request</h6>")
                with st.container(height = 250):
                        selected_choices = []
                        if option_mapping == 'Custom':
                                selected_choices = []
                                for idx, element in enumerate(global_variables.all_indicators, start=1): #will only create element box once, with unique key
                                        is_checked = st.checkbox(element, key=idx)  
                                        if is_checked:
                                                selected_choices.append(element)
                        elif option_mapping == 'Poverty':
                                selected_choices = []
                                for idx, element in enumerate(global_variables.poverty_choices, start=1): #will only create element box once, with unique key
                                        is_checked = st.checkbox(element, key=idx)  
                                        if is_checked:
                                                selected_choices.append(element)
                        elif option_mapping == 'Education':
                                selected_choices = []
                                for idx, element in enumerate(global_variables.education_choices, start=1): #will only create element box once, with unique key
                                        is_checked = st.checkbox(element, key=idx)  
                                        if is_checked:
                                                selected_choices.append(element)
                        elif option_mapping == 'Land and Agriculture':
                                selected_choices = []
                                for idx, element in enumerate(global_variables.land_ag_choices, start=1): #will only create element box once, with unique key
                                        is_checked = st.checkbox(element, key=idx)  
                                        if is_checked:
                                                selected_choices.append(element)
                        elif option_mapping == 'Exports, Imports, and Trade':
                                selected_choices = []
                                for idx, element in enumerate(global_variables.exp_choices, start=1): #will only create element box once, with unique key
                                        is_checked = st.checkbox(element, key=idx)  
                                        if is_checked:
                                                selected_choices.append(element)
                        elif option_mapping == 'War and Mortality':
                                selected_choices = []
                                for idx, element in enumerate(global_variables.war_options, start=1): #will only create element box once, with unique key
                                        is_checked = st.checkbox(element, key=idx)  
                                        if is_checked:
                                                selected_choices.append(element)
                        elif option_mapping == 'Economy':
                                selected_choices = []
                                for idx, element in enumerate(global_variables.war_options, start=1): #will only create element box once, with unique key
                                        is_checked = st.checkbox(element, key=idx)  
                                        if is_checked:
                                                selected_choices.append(element)
                        elif option_mapping == 'Health and Disease':
                                selected_choices = []
                                for idx, element in enumerate(global_variables.health_options, start=1): #will only create element box once, with unique key
                                        is_checked = st.checkbox(element, key=idx)  
                                        if is_checked:
                                                selected_choices.append(element)
                        elif option_mapping == 'Politics and Aid':
                                selected_choices = []
                                for idx, element in enumerate(global_variables.politics_choices, start=1): #will only create element box once, with unique key
                                        is_checked = st.checkbox(element, key=idx)  
                                        if is_checked:
                                                selected_choices.append(element)

        #summary
        st.html("<h5 style='text-align: center; color: black;margin-top: 10px;'>Request Summary</h5>")

        col1, col2 = st.columns(2)
        with col1:
                
                st.html("<h6 style='text-align: center; color: black;margin-bottom: -15px;'>Selected Indicators</h6>")
                print(len(selected_choices))
                if len(selected_choices) > 0:
                        with st.container(height = 200):
                                
                                length_selected = (f'Count: {len(selected_choices)}')
                                length_selected = f"<h6 style='text-align: center; color: black;margin-bottom: -15px;'>{length_selected}</h6>"
                                st.html(length_selected)
                                for element in selected_choices:
                                        #element_count += 1
                                        #mark_str = element_count + ': ' + element
                                        st.markdown(element)
                                        st.write()
                else:
                        with st.container(height = 200):
                                st.info('Selected indicators above will appear here.')
        with col2:
                st.html("<h6 style='text-align: center; color: black;margin-bottom: -15px;'>Visualization Specifications</h6>")

                with st.container(height = 200):
                        st.html("<h6 style='text-align: center; color: black;margin-bottom: -30px;'>Plot type:</h6>")
                        option_library_str = f"<h6 style='text-align: center; color: black;margin-bottom: -10px;'>{option_library}</h6>"
                        st.html(option_library_str)

                        st.html("<h6 style='text-align: center; color: black;margin-bottom: -30px;'>Independent variable:</h6>")
                        independent_library_str = f"<h6 style='text-align: center; color: black;margin-bottom: -10px;'>{option_independent}</h6>"
                        st.html(independent_library_str)

                        if st.button("  Let's go!  "):
                                st.write('ok')

except:
        st.info('Navigate to Individual Mapper first.')