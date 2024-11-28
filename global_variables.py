import pandas as pd
from streamlit_gsheets import GSheetsConnection
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import streamlit as st

my_test = 'hi'

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_sheets_credentials"], scope)
client = gspread.authorize(creds)

spreadsheet = client.open_by_key(st.secrets["google_sheets"]["spreadsheet_id"])

worksheet = spreadsheet.worksheet('IndicatorNames')
data = worksheet.get_all_values()

df = pd.DataFrame(data, columns = ['Indicator Name'])

all_indicators = []

for index, row in df.iterrows():
    all_indicators.append(row['Indicator Name'])

all_indicators = all_indicators[1:] #remove the first row

worksheet = spreadsheet.worksheet('Indic_MetaData')
data = worksheet.get_all_values()

df_indic = pd.DataFrame(data, columns = ['Indicator Name', 'Indicator Description','Indicator Source'])
df_indic = df_indic.reset_index() #indicators_dataset

#poverty indicators
spreadsheet_2 = client.open_by_key(st.secrets["google_sheets"]["spreadsheet_id"])
pop_sheet_2 = spreadsheet_2.worksheet('TotPop')
pop_data_2 = pop_sheet_2.get_all_values()

pop_df = pd.DataFrame(pop_data_2, columns = ['Country Name','Country Code','Indicator Name','Indicator Code',	'1960',
    '1961',	'1962','1963',	'1964', '1965','1966','1967','1968','1969','1970','1971','1972','1973','1974',
    '1975',	'1976',	'1977','1978','1979','1980','1981','1982','1983','1984','1985', '1986',	'1987',	'1988',	
    '1989',	'1990',	'1991',	'1992',	'1993',	'1994',	'1995',	'1996',	'1997',	'1998',	'1999',	'2000',	'2001',	'2002',	
    '2003',	'2004',	'2005',	'2006',	'2007',	'2008',	'2009',	'2010',	'2011',	'2012',	'2013',	'2014',	'2015',	'2016',	
    '2017',	'2018','2019','2020','2021','2022','2023'])

#GDP
spreadsheet_gdp = client.open_by_key(st.secrets["google_sheets"]["spreadsheet_id"])
gdp_sheet = spreadsheet_gdp.worksheet('GDP_Data')
gdp_data = gdp_sheet.get_all_values()



