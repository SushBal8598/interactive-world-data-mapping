import streamlit as st
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import pandas as pd
import vertexai
from vertexai.generative_models import GenerativeModel

from streamlit_gsheets import GSheetsConnection

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import html

#streamlit run streamlit_app.py

st.markdown("<h1 style='text-align: center; color: black;'>Individual Country Mapper</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: black;'>Explore top-down overviews of specific countries.</h1>", unsafe_allow_html=True)

bynames = {'Argentina': 'República Argentina', 
           'Bolivia':'Estado Plurinacional de Bolivia',
           'Brazil':'Estado do Brasil',
           'Chile':'República de Chile',
           'Colombia':'República de Colombia', 
           'Ecuador':'República del Ecuador',
           'Guyana':'Co-operative Republic of Guyana',
           'Peru':'República del Perú',
           'Paraguay':'República del Paraguay',
           'Suriname':'The Republic of Suriname',
           'Uruguay':'República Oriental del Uruguay',
           'Venezuela':'República Bolivariana de Venezuela'}

option = st.selectbox(
    "Pick a country to explore.",
    ("Placeholder", "Argentina", 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Peru', 'Paraguay', 'Suriname', 'Uruguay', 'Venezuela'),
)

if option != 'Placeholder':
    col1, col2, col3 , col4, col5 = st.columns(5)

    html_str = f"""<h2 style='text-align: center; color: black;'>{option}</h2>"""
    st.markdown(html_str, unsafe_allow_html=True)

    #italicize country name
    get_name = bynames[option]
    country_byname = f"""<h4 style='text-align: center; color: black;'><em>{get_name}</em></h4>"""
    
    st.markdown("""
    <style>
    [data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{
        gap: 0.5rem; 
    }
    </style>
    """,unsafe_allow_html=True)

    #fix the spacing issue.

    st.markdown(country_byname, unsafe_allow_html=True)

    st.markdown(
    """
    <style>
    .stButton>button {
        width: 200px;
        height: 50px;
        font-size: 20px;
    }
    </style>
    """, 
    unsafe_allow_html=True
)
    
    col1, col2 = st.columns(2)

    with col1:
        #def generate(prompt):
            #vertexai.init(project="<YOUR_PROJECT_ID>", location="us-central1")
            #model = GenerativeModel("gemini-1.5-flash-001")

            #responses = model.generate_content(
            #prompt,
            #generation_config=generation_config,
            #stream=False,
            #)

        st.markdown('<div style="text-align: center;">This section will be updated with an overview of the country!</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div style="text-align: center;">This section will be updated with a carousel of images!</div>', unsafe_allow_html=True)

    columns = st.columns((1))
    with col1:
        st.markdown('<div style="text-align: center;"></div>', unsafe_allow_html=True)

    columns = st.columns((1, 1, 1))
    button_pressed = columns[1].button('Generate insights!')

    if button_pressed:

        #The most pressing statistics to highlight here, 2023:
        #population size, GDP (Gross Domestic Product), per capita income (often measured as Gross National Income per capita), life expectancy, infant mortality rate, literacy rate, unemployment rate, poverty rate, CO2 emissions, and economic inequality levels

        def format_number(num): #from streamlit blog: https://blog.streamlit.io/crafting-a-dashboard-app-in-python-using-streamlit/
            
            if num > 1000000000000:
                if not num % 1000000000000:
                    return f'{num // 1000000000000} T'
                return f'{round(num / 1000000000000, 3)} T'
            
            if num > 1000000000:
                if not num % 1000000000:
                    return f'{num // 1000000000} B'
                return f'{round(num / 1000000000, 3)} B'
            
            if num > 1000000:
                if not num % 1000000:
                    return f'{num // 1000000} M'
                return f'{round(num / 1000000, 3)} M'
            return f'{num // 1000} K'
        
        col1, col2 = st.columns(2)

        def make_general_sheet(data, name):
            name = pd.DataFrame(data, columns = ['Country Name','Country Code','Indicator Name','Indicator Code',	'1960',
        '1961',	'1962','1963',	'1964', '1965','1966','1967','1968','1969','1970','1971','1972','1973','1974',
        '1975',	'1976',	'1977','1978','1979','1980','1981','1982','1983','1984','1985', '1986',	'1987',	'1988',	
        '1989',	'1990',	'1991',	'1992',	'1993',	'1994',	'1995',	'1996',	'1997',	'1998',	'1999',	'2000',	'2001',	'2002',	
        '2003',	'2004',	'2005',	'2006',	'2007',	'2008',	'2009',	'2010',	'2011',	'2012',	'2013',	'2014',	'2015',	'2016',	
        '2017',	'2018','2019','2020','2021','2022','2023'])
            return name

        with col1:
            
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_sheets_credentials"], scope)
            client = gspread.authorize(creds)

            spreadsheet = client.open_by_key(st.secrets["google_sheets"]["spreadsheet_id"])
            pop_sheet = spreadsheet.worksheet('TotPop')
            pop_data = pop_sheet.get_all_values()

            pop_df = pd.DataFrame(pop_data, columns = ['Country Name','Country Code','Indicator Name','Indicator Code',	'1960',
        '1961',	'1962','1963',	'1964', '1965','1966','1967','1968','1969','1970','1971','1972','1973','1974',
        '1975',	'1976',	'1977','1978','1979','1980','1981','1982','1983','1984','1985', '1986',	'1987',	'1988',	
        '1989',	'1990',	'1991',	'1992',	'1993',	'1994',	'1995',	'1996',	'1997',	'1998',	'1999',	'2000',	'2001',	'2002',	
        '2003',	'2004',	'2005',	'2006',	'2007',	'2008',	'2009',	'2010',	'2011',	'2012',	'2013',	'2014',	'2015',	'2016',	
        '2017',	'2018','2019','2020','2021','2022','2023'])

            country_df = pop_df[pop_df['Country Name'] == option]
            country_df_index = int((pop_df[pop_df['Country Name'] == option].index)[0])
            population = format_number(int(country_df.at[country_df_index, '2023']))
            
            population_safe = html.escape(str(population))

            #make_population_tag = '<div style="display: flex; flex-direction: column; justify-content: center; align-items: center;"><h4>' + 'Population' + '</h4><p style="font-size: 2em;">' + str(population) + '</p></div>'

            population_html = f'''
            <div style="background-color: #f0f0f0; padding: 4px 12px; border-radius: 10px; display: flex; justify-content: center; align-items: center; width: fit-content; margin: 0 auto; text-align: center;">
                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center;">
                    <div style="font-weight: bold; font-size: 1.5em; margin: 0; padding: 0; text-decoration: none; cursor: default;">Population</div>
                    <p style="font-size: 2em; margin: 0; padding: 0; text-decoration: none; cursor: default; pointer-events: none;">{population_safe}</p>
                </div>
            </div>
            '''

            st.markdown(population_html, unsafe_allow_html=True)
        
        with col2:
            spreadsheet = client.open_by_key(st.secrets["google_sheets"]["spreadsheet_id"])
            gdp_sheet = spreadsheet.worksheet('GDP_Data')
            gdp_data = gdp_sheet.get_all_values()

            my_data = make_general_sheet(gdp_data, 'gdp_df')[make_general_sheet(gdp_data, 'gdp_df')['Country Name'] == option]
            gdp_df_index = int(make_general_sheet(gdp_data, 'gdp_df')[make_general_sheet(gdp_data, 'gdp_df')['Country Name'] == option].index[0])
            try:
                gdp = format_number(int(my_data.at[gdp_df_index, '2023']))
            except:
                gdp = format_number(int(my_data.at[gdp_df_index, '2022']))
            
            def hide_anchor_link():
                st.markdown("""
                    <style>
                    .<path d="M15 7h3a5 5 0 0 1 5 5 5 5 0 0 1-5 5h-3m-6 0H6a5 5 0 0 1-5-5 5 5 0 0 1 5-5h3"></path> {display: none}
                    </style>
                    """, unsafe_allow_html=True)

            gdp_safe = html.escape(str(gdp))

            gdp_html = f'''
            <div style="background-color: #f0f0f0; padding: 4px 12px; border-radius: 10px; display: flex; justify-content: center; align-items: center; width: fit-content; margin: 0 auto; text-align: center;">
                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center;">
                    <div style="font-weight: bold; font-size: 1.5em; margin: 0; padding: 0; text-decoration: none; cursor: default;">Nominal GDP</div>
                    <p style="font-size: 2em; margin: 0; padding: 0; text-decoration: none; cursor: default; pointer-events: none;">{gdp_safe}</p>
                </div>
            </div>
            '''

            st.markdown(gdp_html, unsafe_allow_html=True)

#tackle Venezuela, RB issue tmrw

            #st.markdown(make_gdp_tag,
            #unsafe_allow_html=True)


        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_sheets_credentials"], scope)
        client = gspread.authorize(creds)

        # Open the spreadsheet by its ID
        spreadsheet = client.open_by_key(st.secrets["google_sheets"]["spreadsheet_id"])


        # Read data from the specific worksheet
        worksheet = spreadsheet.worksheet(option)
        data = worksheet.get_all_values()

        # Convert the data into a DataFrame if needed
        import pandas as pd
        #df = pd.DataFrame(data)
        df = pd.DataFrame(data, columns = ['Country Name','Country Code','Indicator Name','Indicator Code',	'1960',
        '1961',	'1962','1963',	'1964', '1965','1966','1967','1968','1969','1970','1971','1972','1973','1974',
        '1975',	'1976',	'1977','1978','1979','1980','1981','1982','1983','1984','1985', '1986',	'1987',	'1988',	
        '1989',	'1990',	'1991',	'1992',	'1993',	'1994',	'1995',	'1996',	'1997',	'1998',	'1999',	'2000',	'2001',	'2002',	
        '2003',	'2004',	'2005',	'2006',	'2007',	'2008',	'2009',	'2010',	'2011',	'2012',	'2013',	'2014',	'2015',	'2016',	
        '2017',	'2018','2019','2020','2021','2022','2023'])

        st.write(df)  # Display the data in the Streamlit app
        st.write(df.columns)

else: 
    st.success('Select a country above to proceed.')


    