import streamlit as st
import pandas as pd
import numpy as np
import sdv
from sdv.multi_table import HMASynthesizer
import global_variables

from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KernelDensity

from statsmodels.tsa.arima.model import ARIMA

html_str_title = (f"<h1 style='text-align: center; color: black;'>Machine Learning Sandbox</h1>")
st.html(html_str_title)

html_str_subtitle = (f"<h5 style='text-align: center; color: black;'>Test machine learning capabilities on a number of different indicators.</h1>")
st.html(html_str_subtitle)

argentina_test_data = global_variables.argentina_dataset
years = global_variables.years_list
values = []

arg_test_2 = argentina_test_data[argentina_test_data['Indicator Name'] == 'Computer, communications and other services (% of commercial service exports)']
arg_test_2 = arg_test_2.drop(['Country Name', 'Country Code', 'Indicator Code'], axis=1).reset_index()

for year in years:
    if arg_test_2.at[0, year] != '':
        values.append(arg_test_2.at[0, year])
    else:
        values.append(0)

arg_test_2 = pd.DataFrame({'Indicator Name': 'Computer, communications and other services (% of commercial service exports)', 'Year': years, 'Values': values})

arg_test_2 = arg_test_2.set_index('Year')

arg_test_2 = arg_test_2.fillna(method='ffill', inplace=True)

p, d, q = 1, 0, 1
model = ARIMA(arg_test_2["Values"].astype(float), order=(p, d, q))
model_fit = model.fit()
model_summary = model_fit.summary()
model_summary

#data = arg_test_2['Values']
#train_size = int(len(data) * 0.8)
#train, test = data[:train_size], data[train_size:]

# Fit the model to training data. Replace p, d, q with our ARIMA parameters
#model = ARIMA(train.astype(float), order=(p, d, q))  

# Forecast
#forecast = model_fit.forecast(steps=len(test))

#st.write(forecast)


#st.dataframe(arg_test_2)


