import pandas as pd
from streamlit_gsheets import GSheetsConnection
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import streamlit as st

my_test = 'hi'

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_sheets_credentials"], scope)
client = gspread.authorize(creds)

#Open the spreadsheet by its ID
spreadsheet = client.open_by_key(st.secrets["google_sheets"]["spreadsheet_id"])

# Read data from the specific worksheet
worksheet = spreadsheet.worksheet('IndicatorNames')
data = worksheet.get_all_values()

df = pd.DataFrame(data, columns = ['Indicator Name'])
