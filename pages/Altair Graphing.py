import streamlit as st
import altair as alt
import global_variables
import numpy as np
import pandas as pd
from scipy import stats

can_go = False

try:
        named_title = (f"<h1 style='text-align: center; color: black; text-decoration: underline;'>{st.session_state.option}</h1>")

        indiv_title = (f"<h1 style='text-align: center; color: black;margin-bottom: -50px;'>Individual Visualization:</h1>")
        st.html(indiv_title)

        st.html(named_title)
        
        get_option_title = st.session_state.option

        can_go = True

        col1,col2 = st.columns(2)

        with col1:
                st.html("<h6 style='text-align: center; color: black;margin-bottom: -25px;'>Step 1: Input Query</h6>")

                option_mapping = st.selectbox(
                "Select a pre-loaded statistics set, or continue with custom.",
                ("Custom", "Poverty", "Education","Land and Agriculture","Exports, Imports, and Trade", "War and Mortality", "Economy", "Health and Disease", "Politics and Aid"),
        )

                option_library = st.selectbox(
                "Select a plot to graph against.",
                ("Scatterplot", "Lineplot", 'Boxplot', 'Bar Chart'),
        )
                option_independent = st.selectbox(
                "Select the independent variable.",
                ("Year (Time Series)", 'Custom'),
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
                        option_library_str = f"<p style='text-align: center; color: black;margin-bottom: -10px;'>{option_library}</p>"
                        st.html(option_library_str)

                        st.html("<h6 style='text-align: center; color: black;margin-bottom: -30px;'>Independent variable:</h6>")
                        independent_library_str = f"<p style='text-align: center; color: black;margin-bottom: 3px;'>{option_independent}</p>"
                        st.html(independent_library_str)
                        
                        if len(selected_choices) == 0:
                                st.info('You need to select metrics first!')
                        else:
                                col1, col2, col3 = st.columns(3)
                                continue_to_plot = False
                                with col2:
                                        if st.button("Generate"):
                                                continue_to_plot = True
                                                #format data: year, value, 

        if continue_to_plot == True:
                if option_independent == 'Year (Time Series)':
                        years = global_variables.years_list
                        choices_to_plot = selected_choices
                        resulting_values = []
                        indicators = []
                        resulting_frame = pd.DataFrame()
                        if get_option_title == 'Argentina':
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
                                                indicators.append(element)
                                        merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Indicator': indicators})
                                        resulting_frame = pd.concat([resulting_frame, merge_frame])
                                
                        elif get_option_title == 'Bolivia':
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
                                                indicators.append(element)
                                        merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Indicator': indicators})
                                        resulting_frame = pd.concat([resulting_frame, merge_frame])
                        elif get_option_title == 'Brazil':
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
                                                indicators.append(element)
                                        merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Indicator': indicators})
                                        resulting_frame = pd.concat([resulting_frame, merge_frame])
                        elif get_option_title == 'Chile':
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
                                                indicators.append(element)
                                        merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Indicator': indicators})
                                        resulting_frame = pd.concat([resulting_frame, merge_frame])
                        elif get_option_title == 'Colombia':
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
                                                indicators.append(element)
                                        merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Indicator': indicators})
                                        resulting_frame = pd.concat([resulting_frame, merge_frame])
                        elif get_option_title == 'Ecuador':
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
                                                indicators.append(element)
                                        merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Indicator': indicators})
                                        resulting_frame = pd.concat([resulting_frame, merge_frame])
                        elif get_option_title == 'Guyana':
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
                                                indicators.append(element)
                                        merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Indicator': indicators})
                                        resulting_frame = pd.concat([resulting_frame, merge_frame])
                        elif get_option_title == 'Paraguay':
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
                                                indicators.append(element)
                                        merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Indicator': indicators})
                                        resulting_frame = pd.concat([resulting_frame, merge_frame])
                        elif get_option_title == 'Peru':
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
                                                indicators.append(element)
                                        merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Indicator': indicators})
                                        resulting_frame = pd.concat([resulting_frame, merge_frame])
                        elif get_option_title == 'Suriname':
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
                                                indicators.append(element)
                                        merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Indicator': indicators})
                                        resulting_frame = pd.concat([resulting_frame, merge_frame])
                        elif get_option_title == 'Uruguay':
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
                                                indicators.append(element)
                                        merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Indicator': indicators})
                                        resulting_frame = pd.concat([resulting_frame, merge_frame])
                        elif get_option_title == 'Venezuela':
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
                                                indicators.append(element)
                                        merge_frame = pd.DataFrame({'Year': years, 'Value': resulting_values, 'Indicator': indicators})
                                        resulting_frame = pd.concat([resulting_frame, merge_frame])
                        
                        resulting_frame['Year'] = pd.to_numeric(resulting_frame['Year'], errors='coerce') 
                        resulting_frame['Value'] = pd.to_numeric(resulting_frame['Value'], errors='coerce')

                        col1, col2, col3 = st.columns(3)
                        with col2:
                                st.html("<h6 style='text-align: center; color: black;margin-bottom: -10px;margin-top: 10px;'>Indicator Data</h6>")
                        
                        #mark_line()
                        if option_library == 'Scatterplot':
                                chart = alt.Chart(resulting_frame).mark_circle(size=60).encode(
                                        x=alt.X('Year', title='Year', sort='ascending', scale=alt.Scale(domain=[1960, resulting_frame['Year'].max()])),
                                        y=alt.Y('Value', title='Value', axis=alt.Axis(tickCount=5)),
                                        color='Indicator',
                                        tooltip=['Year', 'Value', 'Indicator']
                                        ).interactive()

                                st.altair_chart(chart, use_container_width = True)
                        
                        elif option_library == 'Lineplot':
                                chart = alt.Chart(resulting_frame).mark_line().encode(
                                        x=alt.X('Year', title='Year', sort='ascending', scale=alt.Scale(domain=[1960, resulting_frame['Year'].max()])),
                                        y=alt.Y('Value', title='Value', axis=alt.Axis(tickCount=5)),
                                        color='Indicator',
                                        tooltip=['Year', 'Value', 'Indicator']
                                        ).interactive()
                        
                                st.altair_chart(chart, use_container_width = True)

                        elif option_library == 'Boxplot':
                                chart = alt.Chart(resulting_frame).mark_boxplot(extent="min-max").encode(
                                        alt.X('Value:Q', title='Value').scale(zero=False),
                                        alt.Y("Indicator:N"),
                                        ).interactive()

                                st.altair_chart(chart, use_container_width = True)

                        elif option_library == 'Bar Chart': 
                                chart = alt.Chart(resulting_frame).mark_bar().encode(
                                        x='Year',
                                        y='Value',
                                        color='Indicator',
                                        tooltip=['Year', 'Value', 'Indicator']
                                ).interactive()
                                
                                st.altair_chart(chart, use_container_width = True)
                        
                        if len(selected_choices) > 25:
                                st.html("<p style='text-align: center; color: black;margin-bottom: -10px;margin-top: -20px;'>Indicator overload! Some data may not be shown.</p>")

                        st.html("<h5 style='text-align: center; color: black;margin-bottom: -10px;margin-top: 10px;'>Statistical Summary</h5>")
                        col1, col2 = st.columns([1.7,1.3])

                        with col1:
                                with st.container(height = 250):
                                        st.dataframe(resulting_frame)
                        
                        with col2:
                                with st.container(height = 250):
                                        #resulting_frame['Value'] = resulting_frame['Value'].replace({None: 0})
                                        uniques = list(resulting_frame['Indicator'].unique())
                                        slopes = []
                                        intercepts = []
                                        r_squareds = []

                                        means = []
                                        stds = []
                                        medians = []
                                        inters = []

                                        for i in range(len(uniques)):
                                                #st.write(uniques[i])
                                                data_df_edit = resulting_frame[resulting_frame['Indicator'] == str(uniques[i])]
                                                data_df_edit.dropna(inplace=True)
                                                eq_edit = stats.linregress(data_df_edit['Year'].to_numpy(), data_df_edit['Value'].to_numpy())
                                                #st.write(f'Slope: {eq_edit.slope}')

                                                indicator_name = f"<p style='text-align: center; color: black; margin-bottom: -15px;font-weight:bold;'>{'Indicator Name'}</p>"
                                                st.html(indicator_name)

                                                make_string = f"<p style='text-align: center; color: black;'>{uniques[i]}</p>"
                                                #indicator name
                                                st.html(make_string)

                                                slope = f'LoBF, slope:'
                                                indicator_slope = f"<p style='text-align: center; color: black; margin-bottom: -15px;font-weight:bold;'>{slope}</p>"
                                                st.html(indicator_slope)

                                                real_slope = f'{eq_edit.slope}'
                                                make_string = f"<p style='text-align: center; color: black;'>{real_slope}</p>"
                                                #indicator name
                                                st.html(make_string)

                                                slopes.append(eq_edit.slope)

                                                intercept = f'LoBF, intercept:'
                                                indicator_intercept = f"<p style='text-align: center; color: black; margin-bottom: -15px;font-weight:bold;'>{intercept}</p>"
                                                st.html(indicator_intercept)

                                                real_intercept = f'{eq_edit.intercept}'
                                                make_string = f"<p style='text-align: center; color: black;'>{real_intercept}</p>"
                                                #indicator name
                                                st.html(make_string)

                                                intercepts.append(eq_edit.intercept)

                                                r_squared = f'LoBF, r-squared:'
                                                indicator_slope = f"<p style='text-align: center; color: black; margin-bottom: -15px;font-weight:bold;'>{r_squared}</p>"
                                                st.html(indicator_slope)

                                                real_r = f'{eq_edit.rvalue ** 2}'
                                                make_string = f"<p style='text-align: center; color: black;'>{real_r}</p>"
                                                #indicator name
                                                st.html(make_string)

                                                r_squareds.append(eq_edit.rvalue ** 2)

                                                st.divider()

                                                col1_data_bank = data_df_edit['Value'].to_numpy()
                                                mean = col1_data_bank.mean()
                                                means.append(mean)
                                                std = col1_data_bank.std()
                                                stds.append(std)
                                                med = stats.median_abs_deviation(col1_data_bank)
                                                medians.append(med)
                                                iqr = stats.iqr(col1_data_bank)
                                                inters.append(iqr)
                        
                        
                        st.divider()
                        
                        stats_df = pd.DataFrame({'Indicator Name':uniques, 'LoBF Slope': slopes, 'LoBF Intercept': intercepts, 'LoBF R-Squared': r_squareds,
                                                 'Mean': means, 'Standard Deviation': stds, 'Median': medians, 'IQR': inters})
                        
                        st.html("<h5 style='text-align: center; color: black;margin-bottom: -10px;margin-top: 10px;'>Statistical Output</h5>")
                        st.dataframe(stats_df)

                        col1, col2, col3 = st.columns([2, 1, 2])

                        with col2:
                                if st.button("Back to Main"):
                                        st.switch_page("streamlit_app.py")
                                  

                else:
                        option_independent = option_independent
except:
        if can_go == False:
                st.info('Navigate to Individual Mapper first.')