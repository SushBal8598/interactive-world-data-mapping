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


    