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
import time
from time import sleep

import global_variables

st.set_page_config(page_title="IWDM Individual Mapper",
    page_icon="🗺️",
)

#streamlit run streamlit_app.py

#Get statistics for all the indicators

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_sheets_credentials"], scope)
client = gspread.authorize(creds)

#Open the spreadsheet by its ID
spreadsheet = client.open_by_key(st.secrets["google_sheets"]["spreadsheet_id"])


# Read data from the specific worksheet
worksheet = spreadsheet.worksheet('IndicatorNames')
data = worksheet.get_all_values()

#intro dict
countries_intro_dict = {
    'Argentina': "Argentina, located in southern South America, is the eighth-largest country in the world and known for its diverse landscapes, from the vast plains of the Pampas to the rugged Andes mountains and the glaciers of Patagonia. Its capital, Buenos Aires, is a vibrant cultural center famous for its European-style architecture, tango music, and rich culinary traditions, including beef and wine. Argentina boasts a dynamic economy, with key industries such as agriculture, mining, and energy. With a history shaped by indigenous cultures, Spanish colonialism, and political change, Argentina is a country with deep cultural roots and a passion for football (soccer).",
    'Bolivia':"Bolivia, landlocked in central South America, is a country of stunning geographic diversity, from the high-altitude Altiplano plateau to the dense Amazon rainforest. Its capital, Sucre, is the constitutional seat of government, while La Paz serves as the administrative capital, situated at one of the world's highest elevations. Bolivia is rich in indigenous cultures, with a significant portion of its population identifying as indigenous, particularly Aymara and Quechua. Known for its natural resources, including lithium and natural gas, Bolivia also features cultural landmarks like the ancient ruins of Tiwanaku and the Uyuni Salt Flats. Its history is marked by political and social change.",
    'Brazil':"Brazil, the largest country in South America, is renowned for its vast landscapes, vibrant culture, and diverse ecosystems. Bordered by every South American country except Chile and Ecuador, it stretches from the Amazon rainforest in the north to beautiful beaches along the Atlantic coast. The capital, Brasília, is known for its modernist architecture, while Rio de Janeiro is famous for its Carnival, iconic Christ the Redeemer statue, and stunning beaches. Brazil has a dynamic economy driven by agriculture, mining, energy, and manufacturing. With its rich mix of indigenous, African, and European heritage, Brazil is a cultural and natural powerhouse.",
    'Chile': "Chile is a long, narrow country stretching along South America's western coast, bordered by the Pacific Ocean to the west, Argentina to the east, and Bolivia and Peru to the north. Known for its stunning natural landscapes, Chile offers everything from the driest desert in the world, the Atacama, to the glacial fjords of Patagonia. Its capital, Santiago, is a bustling cultural and economic hub. A stable democracy with a thriving economy, Chile is famous for its copper production, wine, and diverse cultural heritage, blending indigenous traditions with Spanish colonial influences. It's a top destination for nature lovers and adventurers.",
    'Colombia':"Colombia, located in the northwest corner of South America, is a country of vibrant culture, diverse landscapes, and rich history. It is bordered by the Caribbean Sea to the north, Venezuela and Brazil to the east, Peru and Ecuador to the south, and Panama to the northwest. Colombia is known for its stunning natural beauty, including Amazon rainforests, Andean mountains, and pristine beaches. Bogotá, the capital, is an economic and cultural hub, while cities like Medellín and Cartagena offer unique historical and modern attractions. Famous for its coffee, music, and warm-hearted people, Colombia is a country of resilience and growth.",
    'Ecuador':"Ecuador, located on the equator in northwestern South America, is a small but geographically diverse country. It boasts coastal plains, Andean highlands, and vast Amazon rainforest. The capital, Quito, is a UNESCO World Heritage site known for its well-preserved colonial architecture. Ecuador's natural beauty is matched by its biodiversity, with the Galápagos Islands, a world-renowned natural wonder, offering unique wildlife. The country's economy is driven by oil, agriculture (especially bananas and flowers), and tourism. Ecuador has a rich cultural heritage, blending indigenous traditions with Spanish colonial influences. Despite its size, Ecuador is a country of striking contrasts and vibrant culture.",
    'Guyana':"Guyana, located on the northeastern coast of South America, is a small but culturally rich country bordered by Venezuela, Brazil, and Suriname, with the Atlantic Ocean to the north. Its capital, Georgetown, is a bustling city known for its colonial architecture and diverse population. Guyana is unique in its mix of ethnic groups, including Afro-Guyanese, Indo-Guyanese, and indigenous peoples. The country's economy is driven by agriculture, mining (particularly gold and bauxite), and, more recently, oil exports. With vast rainforests, the mighty Essequibo River, and rich biodiversity, Guyana is a land of natural beauty and cultural diversity.",
    'Peru':"Peru, located on the western coast of South America, is a country rich in history, culture, and natural beauty. It is home to the ancient Inca civilization, with Machu Picchu being one of the most iconic archaeological sites in the world. Lima, the capital, is a bustling metropolis known for its gastronomy and colonial architecture. Peru's diverse geography includes the Andes mountains, the Amazon rainforest, and Pacific coastline, offering a wide range of ecosystems. The economy is based on mining, agriculture, and tourism. With its unique blend of indigenous, Spanish, and Afro-Peruvian influences, Peru is a country of vibrant traditions.",
    'Paraguay':"Paraguay, a landlocked country in the heart of South America, is bordered by Argentina, Brazil, and Bolivia. Its capital, Asunción, is the political and economic center of the country. Paraguay is known for its rich indigenous heritage and bilingual culture, with both Spanish and Guaraní widely spoken. The country’s landscape is characterized by grassy plains, forests, and the Paraguay River, which divides it into two regions. Agriculture plays a vital role in the economy, with soybeans, beef, and cotton being major exports. Despite its small size, Paraguay has a unique blend of traditions and a resilient, close-knit population.",
    'Suriname':"Suriname, located on the northeastern coast of South America, is the smallest country on the continent. It is bordered by the Atlantic Ocean to the north, French Guiana to the east, Brazil to the south, and Guyana to the west. The capital, Paramaribo, is a cultural and economic hub known for its colonial Dutch architecture and vibrant multicultural atmosphere. Suriname’s population is ethnically diverse, with a mix of Indigenous, African, East Indian, Javanese, and European descendants. The country’s economy is driven by mining (especially bauxite and gold), agriculture, and timber. Suriname's lush rainforests and biodiversity make it a unique ecological treasure.",
    'Uruguay':"Uruguay, located on the southeastern coast of South America, is known for its high quality of life, progressive social policies, and vibrant culture. It is bordered by Argentina to the west, Brazil to the north, and the Atlantic Ocean to the southeast. Montevideo, the capital, is a lively city with a rich cultural scene, from tango and candombe music to a thriving arts community. Uruguay has a stable economy, largely driven by agriculture, livestock, and renewable energy. Known for its beautiful beaches, lush countryside, and passionate football (soccer) culture, Uruguay is a small country with a big global reputation.",
    'Venezuela':"Venezuela, located on the northern coast of South America, is a country of dramatic natural beauty, from the Andes mountains to the vast plains of the Llanos and the tropical rainforests of the Amazon. Caracas, the capital, is a vibrant yet politically complex city. Known for its oil wealth, Venezuela's economy has faced significant challenges in recent years, leading to social and political unrest. Despite this, the country remains rich in natural resources, including vast petroleum reserves, gold, and diamonds. Venezuela also boasts stunning landscapes like Angel Falls, the world's highest uninterrupted waterfall, and a diverse mix of cultures and traditions."
}

# Convert the data into a DataFrame if needed
#df = pd.DataFrame(data)
df = pd.DataFrame(data, columns = ['Indicator Name'])
df = df.reset_index()

all_indicators = []

for index, row in df.iterrows():
    all_indicators.append(row['Indicator Name'])

all_indicators = all_indicators[1:] #remove the first row

worksheet = spreadsheet.worksheet('Indic_MetaData')
data = worksheet.get_all_values()

df_indic = pd.DataFrame(data, columns = ['Indicator Name', 'Indicator Description','Indicator Source'])
df_indic = df_indic.reset_index()

#begin web app

html_str_title = (f"<h1 style='text-align: center; color: black;'>Individual Country Mapper</h1>")
st.html(html_str_title)

html_str_subtitle = (f"<h5 style='text-align: center; color: black;'>Explore top-down overviews of specific countries.</h1>")
st.html(html_str_subtitle)

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

    if 'slider_value' not in st.session_state:
        st.session_state['slider_value'] = 2023

    my_year = str(st.session_state['slider_value'])
    
    #st.write(st.session_state['slider_value']) for debugging

    col1, col2, col3 , col4, col5 = st.columns(5)

    html_str = f"""<h2 style='text-align: center; color: black; margin-bottom: -50px;'>{option}</h2>"""
    st.html(html_str)#, unsafe_allow_html=True)
    #when usign HTML instead of md, don't need to include unsafe_html

    #italicize country name
    get_name = bynames[option]
    country_byname = f"""<h4 style='text-align: center; color: black;margin-bottom: -20px;'><em>{get_name}</em></h4>"""
    
    st.markdown("""
    <style>
    [data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{
        gap: 0.5rem; 
    }
    </style>
    """,unsafe_allow_html=True)

    #fix the spacing issue.

    st.html(country_byname)#, unsafe_allow_html=True)

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

        countries_info = countries_intro_dict.get(option)

        print_countries_info = f"""<div style="text-align: center;">{countries_info}</div>"""

        st.markdown(print_countries_info, unsafe_allow_html=True)
    
    images_dict = {
        'Argentina':"https://cdn.britannica.com/40/195440-050-B3859318/Congressional-Plaza-building-National-Congress-Buenos-Aires.jpg",
        'Bolivia':"https://mediaim.expedia.com/destination/1/170eb17de2d7bbf1ed92aed5e6b7ffca.jpg",
        'Brazil':"https://delivery.gfobcontent.com/api/public/content/74029628fb134f6a9fd4f93a31a2d35b?v=8f6a7999",
        'Chile':"https://www.state.gov/wp-content/uploads/2019/04/Chile-e1556024428830-2496x1406.jpg",
        'Colombia':"https://www.colombia-travels.com/wp-content/uploads/adobestock-266299444-1-1280x800.jpeg",
        'Ecuador':"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQZ_WS_IR_jbyEbEWaa42GYzFu8RholFJW0hQ&s",
        'Guyana':"https://i2.wp.com/photos.smugmug.com/photos/i-3gKgpFm/0/1be92393/O/i-3gKgpFm.jpg",
        'Peru':"https://esghu4h79kf.exactdn.com/wp-content/uploads/2021/05/travel-packages-to-cusco-peru.png?strip=all&lossy=1&w=2560&ssl=1",
        'Paraguay':"https://www.foyerglobalhealth.com/wp-content/uploads/2024/01/anton-lukin-_wBbSk2ffC4-unsplash-1568x882.jpg",
        'Suriname':"https://etichotels.com/journal/wp-content/uploads/2023/11/10-Best-Cities-to-Visit-in-Suriname-ETIC-Hotels.jpg",
        'Uruguay':"https://i.natgeofe.com/n/95f03509-126e-4daf-aa59-5d8990074619/cityscape-montevideo-uruguay.jpg?w=2560&h=1706",
        'Venezuela':"https://www.state.gov/wp-content/uploads/2023/07/shutterstock_611942573v2.jpg"
    }

    captions_dict = {
        'Argentina':"Congressional Plaza with the National Congress building at rear left, Buenos Aires. (Britannica)",
        'Bolivia':"Sucre, Bolivia with view of the Cathedral Basilica of Our Lady of Guadalupe. (Expedia)",
        'Brazil':"View of Rio de Janeiro, with Sugarloaf Mountain in the background. (Cosmos)",
        'Chile':"Overhead of the Carretera Austral, or Chilean Route 7 through Patagonia. (U.S. Dept. of State)",
        'Colombia':"Street view of colorful houses within a neighborhood in Bogota. (Terra Colombia)",
        'Ecuador':"Aerial view of Quito. (Go Galapagos)",
        'Guyana':'View of Kaieteur Falls, the "largest single-drop waterfall in the world." (Wild Junket)',
        'Peru':"Llamas in the frame of the historic Incan city of Machu Picchu. (Treehouse Lodge)",
        'Paraguay':"Aerial view of Asunción. (Foyer Global)",
        'Suriname':"Waterfront homes of Paramaribo, located adjactent to the Suriname River. (ETIC Hotels)",
        'Uruguay':"Montevideo sunset skyline. (National Geographic)",
        'Venezuela':"Caracas, with view of Avila National Park in the distance. (Alejandro Solo / Shutterstock)"
    }

    caption_check = captions_dict[option]

    with col2:
        with st.container(height = 340, border=True):
            get_link = images_dict[option]

            # Add custom CSS to center the image
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

            # Image URL
            image_url = get_link

            # Caption text
            caption_text = caption_check

            # Display the image and caption
            st.markdown(f'<img src="{image_url}" class="centered-image" style="border: 4px solid black;margin-bottom: 10px;">', unsafe_allow_html=True)

            caption_fp = (f'<p style="text-align: center; color:Black;">{caption_text}</p>')

            st.markdown(caption_fp, unsafe_allow_html=True)


            #st.image(get_link, caption=caption_check)

    columns = st.columns((1))
    with col1:
        st.markdown('<div style="text-align: center;"></div>', unsafe_allow_html=True)

    #columns = st.columns((1, 1, 1))
    #button_pressed = columns[1].button('Generate insights!')

    #The most pressing statistics to highlight here, 2023:
    #population size, GDP (Gross Domestic Product), per capita income (often measured as Gross National Income per capita), life expectancy, infant mortality rate, literacy rate, unemployment rate, poverty rate, CO2 emissions, and economic inequality levels

    st.write()
    st.write()

    def format_number(num): #from streamlit blog: https://blog.streamlit.io/crafting-a-dashboard-app-in-python-using-streamlit/
        
        if num > 1000000000000:
            if not num % 1000000000000:
                return f'{num // 1000000000000}T'
            return f'{round(num / 1000000000000, 3)}T'
        
        if num > 1000000000:
            if not num % 1000000000:
                return f'{num // 1000000000}B'
            return f'{round(num / 1000000000, 3)}B'
        
        if num > 1000000:
            if not num % 1000000:
                return f'{num // 1000000}M'
            return f'{round(num / 1000000, 3)}M'
        return f'{num // 1000}K'
    
    col1, col2, col3, col4 = st.columns(4)

    #Poverty headcount ratio at societal poverty line (% of population)

    def make_general_sheet(data, name):
        name = pd.DataFrame(data, columns = ['Country Name','Country Code','Indicator Name','Indicator Code',	'1960',
    '1961',	'1962','1963',	'1964', '1965','1966','1967','1968','1969','1970','1971','1972','1973','1974',
    '1975',	'1976',	'1977','1978','1979','1980','1981','1982','1983','1984','1985', '1986',	'1987',	'1988',	
    '1989',	'1990',	'1991',	'1992',	'1993',	'1994',	'1995',	'1996',	'1997',	'1998',	'1999',	'2000',	'2001',	'2002',	
    '2003',	'2004',	'2005',	'2006',	'2007',	'2008',	'2009',	'2010',	'2011',	'2012',	'2013',	'2014',	'2015',	'2016',	
    '2017',	'2018','2019','2020','2021','2022','2023'])
        return name

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_sheets_credentials"], scope)
    client = gspread.authorize(creds)

    with col1:

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
        population = format_number(int(country_df.at[country_df_index, (my_year)]))
        
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
            gdp = format_number(int(my_data.at[gdp_df_index, (my_year)]))
        except:
            gdp = '---'

        gdp_safe = html.escape(str(gdp))

        gdp_html = f'''
        <div style="background-color: #f0f0f0; padding: 4px 12px; border-radius: 10px; display: flex; justify-content: center; align-items: center; width: fit-content; margin: 0 auto; text-align: center;">
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <div style="font-weight: bold; font-size: 1.5em; margin: 0; padding: 0; text-decoration: none; cursor: default;">Nominal GDP</div>
                <p style="font-size: 2em; margin: 0; padding: 0; text-decoration: none; cursor: default; pointer-events: none;">${gdp_safe}</p>
            </div>
        </div>
        '''

        st.markdown(gdp_html, unsafe_allow_html=True)

    with col3:
        spreadsheet = client.open_by_key(st.secrets["google_sheets"]["spreadsheet_id"])
        worksheet = spreadsheet.worksheet(option)
        data = worksheet.get_all_values()

        capita_data = (make_general_sheet(data, 'per_capita_df')[make_general_sheet(data, 'per_capita_df')['Indicator Name'] == 'GDP per capita (current US$)'])
        capita_index = (make_general_sheet(data, 'per_capita_df')[make_general_sheet(data, 'per_capita_df')['Indicator Name'] == 'GDP per capita (current US$)'].index[0])

        try:
            per_capita = (float(capita_data.at[capita_index, my_year]))
            escape_str = str((f'${per_capita:.2f}'))
        except:
            per_capita = '--.--'
            escape_str = per_capita

        capita_safe = html.escape(escape_str)

        capita_html = f'''
        <div style="background-color: #f0f0f0; padding: 4px 12px; border-radius: 10px; display: flex; justify-content: center; align-items: center; width: fit-content; margin: 0 auto; text-align: center;">
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <div style="font-weight: bold; font-size: 1.5em; margin: 0; padding: 0; text-decoration: none; cursor: default;">Per Capita</div>
                <p style="font-size: 2em; margin: 0; padding: 0; text-decoration: none; cursor: default; pointer-events: none;">{capita_safe}</p>
            </div>
        </div>
        '''

        st.markdown(capita_html, unsafe_allow_html=True)  

    with col4:
        spreadsheet = client.open_by_key(st.secrets["google_sheets"]["spreadsheet_id"])
        worksheet = spreadsheet.worksheet(option)
        data = worksheet.get_all_values()    

        name = 'SI.POV.SOPO'

        poverty_data = (make_general_sheet(data, 'poverty_df')[make_general_sheet(data, 'poverty_df')['Indicator Code'] == name])            #poverty_index = (make_general_sheet(data, 'poverty_line_df')[make_general_sheet(data, 'poverty_line_df')['Indicator Code'] == name].index[0])
        poverty_index = (make_general_sheet(data, 'poverty_df')[make_general_sheet(data, 'poverty_df')['Indicator Code'] == name].index[0])

        if poverty_data.at[poverty_index, my_year] == '':
            poverty_capita = '--.--'
        else:
            poverty_capita = (float(poverty_data.at[poverty_index, my_year]))

        try:
            poverty_safe = html.escape(str((f'{poverty_capita:.2f}%')))
        except:
            poverty_safe = html.escape(str((f'{poverty_capita}%')))

        poverty_html = f'''
        <div style="background-color: #f0f0f0; padding: 4px 12px; border-radius: 10px; display: flex; justify-content: center; align-items: center; width: fit-content; margin: 0 auto; text-align: center;">
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <div style="font-weight: bold; font-size: 1.5em; margin: 0; padding: 0; text-decoration: none; cursor: default;">Poverty Rate</div>
                <p style="font-size: 2em; margin: 0; padding: 0; text-decoration: none; cursor: default; pointer-events: none;">{poverty_safe}</p>
            </div>
        </div>
        '''
        
        st.markdown(poverty_html, unsafe_allow_html=True)  

        #tackle Venezuela, RB issue tmrw

        #st.markdown(make_gdp_tag,
        #unsafe_allow_html=True)

    col1 = st.columns(1)[0]

    slider_value = st.slider(label="", 
            min_value=1960, 
            max_value=2023, 
            value= st.session_state['slider_value'])

    if slider_value == 2023:
        st.info('Choose a year to generate insights for.')

    if slider_value != st.session_state['slider_value']:
        st.session_state['slider_value'] = slider_value
        st.rerun()

    #add a wait
    time.sleep(2)

    st.html("<h5 style='text-align: center; color: black;'>Ready to start plotting?</h5>")

    df = pd.DataFrame(data, columns = ['Country Name','Country Code','Indicator Name','Indicator Code',	'1960',
    '1961',	'1962','1963',	'1964', '1965','1966','1967','1968','1969','1970','1971','1972','1973','1974',
    '1975',	'1976',	'1977','1978','1979','1980','1981','1982','1983','1984','1985', '1986',	'1987',	'1988',	
    '1989',	'1990',	'1991',	'1992',	'1993',	'1994',	'1995',	'1996',	'1997',	'1998',	'1999',	'2000',	'2001',	'2002',	
    '2003',	'2004',	'2005',	'2006',	'2007',	'2008',	'2009',	'2010',	'2011',	'2012',	'2013',	'2014',	'2015',	'2016',	
    '2017',	'2018','2019','2020','2021','2022','2023'])

    #st.write(df)  # Display the data in the Streamlit app
    #st.write(df.columns)

    col1, col2 = st.columns(2)

    with col1:

        st.html("<h6 style='text-align: center; color: black;margin-bottom: -31px;'>What statistics are available to you?</h6>")

        with col1:

            st.markdown("""
                <style>
                    .custom-button {
                        display: inline-block;
                        background-color: #FFFFFF;
                        color: black;
                        text-align: center;
                        padding: 10px 20px;
                        margin: 5px;
                        border-radius: 5px;
                        width: auto;
                        font-size: 14px;
                        max-width: 400px;
                        white-space: normal;
                        word-wrap: break-word;
                    }
                    .custom-container {
                        margin-bottom: 20px;
                    }
                </style>
            """, unsafe_allow_html=True)

    # Header for the section

            with st.container(height = 200):
                for element in all_indicators:
                    button_html = f'<button class="custom-button">{element}</button>'
                    st.html(button_html)
    
    with col2:

        st.html("<h6 style='text-align: center; color: black;margin-bottom: -15px;'>What does each statistic mean?</h6>")

        with st.container(height = 200):
        
            options = st.multiselect(
            "",
            all_indicators
        ) 
            if options == []:
                st.info('Input an indicator name for more details.')
            else:
                for element in options:
                    #indicator name
                    indicator_name = f"<p style='text-align: center; color: black; margin-bottom: -15px;font-weight:bold;'>{'Indicator Name'}</p>"
                    st.html(indicator_name)

                    curr_element = (df_indic.loc[df_indic['Indicator Name'] == element])
                    curr_element_index = curr_element.index[0]

                    #name of element
                    write_element = (curr_element.at[curr_element_index, 'Indicator Name'])
                    make_string = f"<p style='text-align: center; color: black;'>{write_element}</p>"
                    #indicator name
                    st.html(make_string) #get name of indic -- get it as text next.

                    indicator_desc = f"<p style='text-align: center; color: black; margin-bottom: -15px;font-weight:bold;'>{'Indicator Description'}</p>"
                    st.html(indicator_desc)

                    #origin of element
                    desc_element = (curr_element.at[curr_element_index, 'Indicator Description'])
                    make_string_desc = f"<p style='text-align: center; color: black;'>{desc_element}</p>"
                    #indicator name
                    st.html(make_string_desc) #get name of indic -- get it as text next.
                    
                    indicator_origin = f"<p style='text-align: center; color: black; margin-bottom: -15px;font-weight:bold;'>{'Indicator Source'}</p>"
                    st.html(indicator_origin)

                    #origin of element
                    origin_element = (curr_element.at[curr_element_index, 'Indicator Source'])
                    make_string_origin = f"<p style='text-align: center; color: black; margin-bottom: -20px;'>{origin_element}</p>"
                    #indicator name
                    st.html(make_string_origin) #get name of indic -- get it as text next.

                    st.divider()

    st.markdown("""
        <style>
        .stContainer {
            margin-bottom: 500px; 
        }
        </style>
    """, unsafe_allow_html=True)

    #st.write(global_variables.my_test)
    #we should be able to instance dataframes once, then work off of that

    col1, col2 = st.columns(2)

    #custom mapping, move to alternate page -- need altair plots

    col1, col2, col3 = st.columns(3)

    with col2:
        if st.button("  Let's go!  "):
            st.switch_page("pages/Altair Graphing.py")

else: 
    st.info('Select a country above to proceed.')