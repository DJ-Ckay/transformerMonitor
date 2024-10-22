import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# prompt: write a code that plots an histogram in plotly

import plotly.express as px
import joblib

model = joblib.load('rndReg.joblib')
scaler = joblib.load('scaler.joblib')
# Set the page title and layout
st.set_page_config(page_title="Transformer Dashboard", layout="wide")
st.markdown("<p style='text-align: right;'>Contact Us: Kehinde Clement, Phone No: 08121111830</p>", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center;'>Transformer 00001</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Welcome back to Transformer Dashboard 🌩️</p>", unsafe_allow_html=True)

# File uploader widget
age = st.number_input('Transformer age as at Measurement start', 0.0)
year = int(age)
month = int((age-year)*12)
uploaded_file = st.file_uploader("Choose a file", type=["csv", "txt"])

def calculateHealthindex(current_value, min_value, max_value, thresh = 0.1):
    if current_value < min_value: current_value = min_value; hid = thresh
    elif current_value > max_value: current_value = max_value; hid = 1
    else: hid = max((current_value - min_value) / (max_value - min_value), thresh)
    return round(hid,2)
def healthStatus(val):
    if val<=0.3:return '<span style="color: green;">Normal.</span>'
    elif val<=0.6:return '<span style="color: #F79421;">Watch.</span>'
    else:return '<bold><span style="color: red;">Danger.</span></bold>'
# prompt: write a code that converts a range of min1 - max1 to min2-max2

def convert_range(value, min1, max1, min2, max2):
  """Converts a value from one range to another.

  Args:
    value: The value to convert.
    min1: The minimum value of the original range.
    max1: The maximum value of the original range.
    min2: The minimum value of the new range.
    max2: The maximum value of the new range.

  Returns:
    The converted value.
  """
  if value>max1: value = max1
  return ((value - min1) / (max1 - min1)) * (max2 - min2) + min2

if uploaded_file is not None:
    # Load dataset
    df = pd.read_csv(uploaded_file, index_col="DATE")
    # pd.to_datetime(df['Date'])
    try: df.index = pd.to_datetime(df.index, dayfirst=True); df['Carbon Monoxide (ppm)'] = df['Carbon Monoxide (ppm)'].apply(lambda x: x*2)
    except: df.index = pd.to_datetime(df.index)
    first_date = df.index.min()
    last_date = df.index.max()
    time_difference = last_date - first_date
    new_age = last_date + pd.DateOffset(years=year, months=month) 
    newAge = (new_age-first_date).days/365
    oilTemp = 'Oil Temperature' if 'Oil Temperature' in df.columns else 'Oil Temperature (?C)'
    df['Carbon Monoxide (ppm)'] = df['Carbon Monoxide (ppm)'].apply(lambda x: x*2)
    df['Oil Temperature S2'] = df[oilTemp] + np.random.uniform(-0.6, 0.8, df.shape[0])
    df['Oil Temperature Avg'] = np.mean(df[['Oil Temperature S2', oilTemp]].values, axis = 1)
    oilTemp = 'Oil Temperature Avg'
    X = df[['Ambient Temperature', 'Load (kVA)', 'Hydrogen (ppm)','Carbon Monoxide (ppm)', 'Oil Temperature Avg']].values
    X = scaler.transform(X)
    pred = np.round(model.predict(X)[-5000:].mean()/100,2)
    pred = round(convert_range(pred, 0, 85, 0, 0.65),2)
    oilTempHID = calculateHealthindex(df[oilTemp].values[-1], 62.779347, 92.364736+15, 0.15)
    oilTempSta = healthStatus(oilTempHID)
    loadKVAHID = calculateHealthindex(df['Load (kVA)'].values[-1], 141.195798, 300, 0.1)
    loadKVASta = healthStatus(loadKVAHID)
    carbonCHID = calculateHealthindex(df['Carbon Monoxide (ppm)'].values[-1], 20, 300, 0.15)
    carbonCSta = healthStatus(carbonCHID)
    hydroCoHID = calculateHealthindex(df['Hydrogen (ppm)'].values[-1], 99.642377, 250, 0.15)
    hydrogenSt = healthStatus(hydroCoHID)
    predStatus = healthStatus(pred)
    
    dateRange = st.radio('SELECT DATE RANGE',['LAST YEAR','LAST 6MONTH', 'LAST 3MONTH', 'LAST 1MONTH','LAST 1WEEK', 'LAST 1DAY'],horizontal = True)
    if dateRange == 'LAST YEAR':
        # Filter data for the last year
        last_year = df.last("1Y")
        
        # Resample data to get monthly averages
        monthly_avg = last_year.resample('M').mean()
        
        # Extract oil temperature, ambient temperature, and load for the last year
        oil_temp = monthly_avg['Oil Temperature Avg']
        ambient_temp = monthly_avg['Ambient Temperature']
        load = monthly_avg['Load (kVA)']
        months = oil_temp.index.strftime("%b")
        # fig = px.bar(months, oil_temp, nbins=20, title="Histogram of Oil Temperature")
        # st.plotly_chart(fig)
        # Simulate the Temperature Graph
        col1, col2 = st.columns((2, 1))
        with col1:
            st.subheader("🌡️ TEMPERATURE")
            
            # Plot monthly average temperatures
            
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.plot(months, oil_temp, label='Oil Temperature', color='purple', marker='o')
            ax.plot(months, ambient_temp, label='Ambient Temperature', color='lightpink', marker='o')
            ax.set_ylabel('Temperature (°C)')
            ax.legend()
            ax.set_yticks(np.arange(0, max(oil_temp) + 30, 10))
            plt.yticks(fontsize = 8)
            plt.xticks(fontsize = 8,rotation=45)
            st.pyplot(fig)

        # Simulate the Load Chart
        with col2:
            st.subheader("🔋 LOAD")
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.bar(months, load, color='purple')
            ax.set_ylabel('Load (Kva)')
            ax.set_yticks(np.arange(0, max(load) + 50, 50))
            plt.yticks(fontsize = 8)
            plt.xticks(fontsize = 8,rotation=45)
            st.pyplot(fig)
        
        carbonCo = monthly_avg['Carbon Monoxide (ppm)']
        hydrogen = monthly_avg['Hydrogen (ppm)']
        fig = plt.figure()
        plt.subplot(121)
        plt.plot(months, carbonCo, label='Carbon Contents (ppm)', color='purple', marker='o')
        plt.title('Hydrogen Contents')
        plt.yticks(fontsize = 8)
        plt.xticks(fontsize = 8,rotation=45)
        plt.subplot(122)
        plt.plot(months, hydrogen, label='Hydrogen Contents (ppm)', color='lightpink', marker='o')
        plt.title('Hydrogen Contents')
        plt.xticks(fontsize = 8,rotation=45)
        plt.yticks(fontsize = 8)
        st.pyplot(fig)

    elif dateRange == 'LAST 6MONTH':
        # Get data for the last 6 months
        last_six_months = df.last("6M")

        # Resample data to get monthly averages for the last 6 months
        monthly_avg = last_six_months.resample('M').mean()

        # Extract oil temperature, ambient temperature, and load for the last 6 months
        oil_temp = monthly_avg[oilTemp]
        ambient_temp = monthly_avg['Ambient Temperature']
        load = monthly_avg['Load (kVA)']

        # Plot for the last 6 months
        months = oil_temp.index.strftime("%b")

        col1, col2 = st.columns((2, 1))
        with col1:
            st.subheader("🌡️ TEMPERATURE")
            
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.plot(months, oil_temp, label='Oil Temperature', color='purple', marker='o')
            ax.plot(months, ambient_temp, label='Ambient Temperature', color='lightpink', marker='o')
            ax.set_ylabel('Temperature (°C)')
            ax.legend()
            ax.set_yticks(np.arange(0, max(oil_temp) + 30, 10))
            plt.xticks(fontsize = 8,rotation=45)
            plt.yticks(fontsize = 8)
            st.pyplot(fig)

        # Simulate the Load Chart
        with col2:
            st.subheader("🔋 LOAD")
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.bar(months, load, color='purple')
            ax.set_ylabel('Load (Kva)')
            ax.set_yticks(np.arange(0, max(load) + 50, 50))
            plt.xticks(fontsize = 8,rotation=45)
            plt.yticks(fontsize = 8)
            st.pyplot(fig)
        carbonCo = monthly_avg['Carbon Monoxide (ppm)']
        hydrogen = monthly_avg['Hydrogen (ppm)']
        fig = plt.figure()
        plt.subplot(121)
        plt.plot(months, carbonCo, label='Carbon Contents (ppm)', color='purple', marker='o')
        plt.title('Hydrogen Contents')
        plt.xticks(fontsize = 8,rotation=45)
        plt.yticks(fontsize = 8)
        plt.subplot(122)
        plt.plot(months, hydrogen, label='Hydrogen Contents (ppm)', color='lightpink', marker='o')
        plt.title('Hydrogen Contents')
        plt.xticks(fontsize = 8,rotation=45)
        plt.yticks(fontsize = 8)
        st.pyplot(fig)


    elif dateRange == 'LAST 3MONTH':
        # Get data for the last 3 months
        last_three_months = df.last("3M")

        # Resample data to get monthly averages for the last 3 months
        monthly_avg = last_three_months.resample('M').mean()

        # Extract oil temperature, ambient temperature, and load for the last 3 months
        oil_temp = monthly_avg[oilTemp]
        ambient_temp = monthly_avg['Ambient Temperature']
        load = monthly_avg['Load (kVA)']

        # Plot for the last 3 months
        months = oil_temp.index.strftime("%b")

        col1, col2 = st.columns((2, 1))
        with col1:
            st.subheader("🌡️ TEMPERATURE")
            
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.plot(months, oil_temp, label='Oil Temperature', color='purple', marker='o')
            ax.plot(months, ambient_temp, label='Ambient Temperature', color='lightpink', marker='o')
            ax.set_ylabel('Temperature (°C)')
            ax.set_yticks(np.arange(0, max(oil_temp) + 30, 10))
            ax.legend()
            plt.xticks(fontsize = 8,rotation=45)
            plt.yticks(fontsize = 8)
            st.pyplot(fig)

        # Simulate the Load Chart
        with col2:
            st.subheader("🔋 LOAD")
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.bar(months, load, color='purple')
            ax.set_ylabel('Load (Kva)')
            ax.set_yticks(np.arange(0, max(load) + 50, 50))
            plt.xticks(fontsize = 8,rotation=45)
            plt.yticks(fontsize = 8)
            st.pyplot(fig)
        carbonCo = monthly_avg['Carbon Monoxide (ppm)']
        hydrogen = monthly_avg['Hydrogen (ppm)']
        fig = plt.figure()
        plt.subplot(121)
        plt.plot(months, carbonCo, label='Carbon Contents (ppm)', color='purple', marker='o')
        plt.title('Hydrogen Contents')
        plt.xticks(fontsize = 8,rotation=45)
        plt.yticks(fontsize = 8)
        plt.subplot(122)
        plt.plot(months, hydrogen, label='Hydrogen Contents (ppm)', color='lightpink', marker='o')
        plt.title('Hydrogen Contents')
        plt.xticks(fontsize = 8,rotation=45)
        plt.yticks(fontsize = 8)
        st.pyplot(fig)

    elif dateRange == 'LAST 1MONTH':
        last_month = df.last("1M")

        # Resample data to get daily averages for the last month
        daily_avg = last_month.resample('W').mean()

        # Extract oil temperature, ambient temperature, and load for the last month
        oil_temp = daily_avg[oilTemp]
        ambient_temp = daily_avg['Ambient Temperature']
        load = daily_avg['Load (kVA)']

        # Simulate the Temperature Graph
        col1, col2 = st.columns((2, 1))
        with col1:
            st.subheader("🌡️ TEMPERATURE")
            
            # Plot daily average temperatures for the last month
            weeks = oil_temp.index.strftime("%d-%b")  # Format to display days in "Day-Month" format
            
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.plot(weeks, oil_temp, label='Oil Temperature', color='purple', marker='o')
            ax.plot(weeks, ambient_temp, label='Ambient Temperature', color='lightpink', marker='o')
            ax.set_ylabel('Temperature (°C)')
            ax.set_yticks(np.arange(0, max(oil_temp) + 30, 10))
            ax.legend()
            plt.xticks(fontsize = 8,rotation=45)
            plt.yticks(fontsize = 8)
            st.pyplot(fig)

        # Simulate the Load Chart
        with col2:
            st.subheader("🔋 LOAD")
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.bar(weeks, load, color='purple')
            ax.set_ylabel('Load (Kva)')
            ax.set_yticks(np.arange(0, max(load) + 50, 50))
            plt.xticks(fontsize = 8,rotation=45)
            plt.yticks(fontsize = 8)
            st.pyplot(fig)
        carbonCo = daily_avg['Carbon Monoxide (ppm)']
        hydrogen = daily_avg['Hydrogen (ppm)']
        fig = plt.figure()
        plt.subplot(121)
        plt.plot(weeks, carbonCo, label='Carbon Contents (ppm)', color='purple', marker='o')
        plt.title('Hydrogen Contents')
        plt.xticks(fontsize = 8,rotation=45)
        plt.yticks(fontsize = 8)
        plt.subplot(122)
        plt.plot(weeks, hydrogen, label='Hydrogen Contents (ppm)', color='lightpink', marker='o')
        plt.title('Hydrogen Contents')
        plt.xticks(fontsize = 8,rotation=45)
        plt.yticks(fontsize = 8)
        st.pyplot(fig)

    elif dateRange == 'LAST 1WEEK':
        last_week = df.last("7D")

        # Resample data to get daily averages for the last week
        daily_avg = last_week.resample('D').mean()

        # Extract oil temperature, ambient temperature, and load for the last week
        oil_temp = daily_avg[oilTemp]
        ambient_temp = daily_avg['Ambient Temperature']
        load = daily_avg['Load (kVA)']

        # Plot for the last week
        days = oil_temp.index.strftime("%d-%b")
        # Simulate the Temperature Graph
        col1, col2 = st.columns((2, 1))
        with col1:
            st.subheader("🌡️ TEMPERATURE")
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.plot(days, oil_temp, label='Oil Temperature', color='purple', marker='o')
            ax.plot(days, ambient_temp, label='Ambient Temperature', color='lightpink', marker='o')
            ax.set_ylabel('Temperature (°C)')
            ax.set_yticks(np.arange(0, max(oil_temp) + 30, 10))
            ax.legend()
            plt.xticks(fontsize = 8,rotation=45)
            plt.yticks(fontsize = 8)
            st.pyplot(fig)
        # Simulate the Load Chart
        with col2:
            st.subheader("🔋 LOAD")
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.bar(days, load, color='purple')
            ax.set_ylabel('Load (Kva)')
            ax.set_yticks(np.arange(0, max(load) + 50, 50))
            plt.xticks(fontsize = 8,rotation=45)
            plt.yticks(fontsize = 8)
            st.pyplot(fig)
        
        carbonCo = daily_avg['Carbon Monoxide (ppm)']
        hydrogen = daily_avg['Hydrogen (ppm)']
        fig = plt.figure()
        plt.subplot(121)
        plt.plot(days, carbonCo, label='Carbon Contents (ppm)', color='purple', marker='o')
        plt.title('Hydrogen Contents')
        plt.xticks(fontsize = 8,rotation=45)
        plt.yticks(fontsize = 8)
        plt.subplot(122)
        plt.plot(days, hydrogen, label='Hydrogen Contents (ppm)', color='lightpink', marker='o')
        plt.title('Hydrogen Contents')
        plt.xticks(fontsize = 8,rotation=45)
        plt.yticks(fontsize = 8)
        st.pyplot(fig)

    elif dateRange == 'LAST 1DAY':
        # Get data for the last 1 day
        last_day = df.last("1D")

        # Resample data to get hourly averages for the last day
        hourly_avg = last_day.resample('2H').mean()

        # Extract oil temperature, ambient temperature, and load for the last day
        oil_temp = hourly_avg[oilTemp]
        ambient_temp = hourly_avg['Ambient Temperature']
        load = hourly_avg['Load (kVA)']

        # Plot for the last day
        hours = oil_temp.index.strftime("%H:%M")
        col1, col2 = st.columns((2, 1))
        with col1:
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.plot(hours, oil_temp, label='Oil Temperature', color='purple', marker='o')
            ax.plot(hours, ambient_temp, label='Ambient Temperature', color='lightpink', marker='o')
            ax.set_ylabel('Temperature (°C)')
            ax.legend()
            ax.set_yticks(np.arange(0, max(oil_temp) + 30, 10))
            plt.xticks(fontsize = 8,rotation=45)
            plt.yticks(fontsize = 8)
            st.pyplot(fig)
        with col2:
            st.subheader("🔋 LOAD")
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.bar(hours, load, color='purple')
            ax.set_ylabel('Load (Kva)')
            ax.set_yticks(np.arange(0, max(load) + 50, 50))
            plt.xticks(fontsize = 8,rotation=45)
            plt.yticks(fontsize = 8)
            st.pyplot(fig)
        carbonCo = hourly_avg['Carbon Monoxide (ppm)']
        hydrogen = hourly_avg['Hydrogen (ppm)']
        fig = plt.figure()
        plt.subplot(121)
        plt.plot(hours, carbonCo, label='Carbon Contents (ppm)', color='purple', marker='o')
        plt.title('Hydrogen Contents')
        plt.xticks(fontsize = 8,rotation=45)
        plt.yticks(fontsize = 8)
        plt.subplot(122)
        plt.plot(hours, hydrogen, label='Hydrogen Contents (ppm)', color='lightpink', marker='o')
        plt.title('Hydrogen Contents')
        plt.xticks(fontsize = 8,rotation=45)
        plt.yticks(fontsize = 8)
        st.pyplot(fig)

    # Middle Section: Result Summary, Prediction Analysis, Correlation Tool
    st.markdown("""
        <style>
        .custom-box {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            height: 600px;
            color: purple;
        }
        .corrPlot{
            color:black;
        }
        table {
            font-family: Arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        h3 {
            color: black;
        }

        th, td {
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
        }

        th {
            background-color: #f2f2f2;
            color: #333;
        }

        tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        tr:hover {
            background-color: #f1f1f1;
        }

        caption {
            caption-side: top;
            padding: 10px;
            font-size: 1.2em;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    # Result Summary in col1
    with col1:
        st.markdown("""<div class='custom-box'>
                    <h3> Result Summary </h3>
                    <ul>
                    <li><b> Transformer's Age</b>: {:.2f} Years</li>
                    <li><b> Period of Data Measurement</b>: {} days</li>
                    <li><b> Average Ambient Temperature</b>: {:.2f}°C</li>
                    <li><b> Average Oil Temperature</b>: {:.2f}°C</li>
                    <li><b> Average Load</b>: {:.2f} Kva</li>
                    </ul>
                    </div>
                    """.format(newAge, time_difference.days, ambient_temp.mean(), oil_temp.mean(), load.mean()), unsafe_allow_html=True)

    # Prediction Analysis in col2
    with col2:
        st.markdown("""<div class='custom-box'> 
                    <h3> Prediction Analysis </h3>
        <table>
            <caption>Transformer Prediction Analysis</caption>
            <tr>
                <th>Parameter</th>
                <th>Value</th>
                <th>Status</th>
            </tr>
            <tr>
                <td>Oil Temperature</td>
                <td>{}</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Transformer Load</td>
                <td>{}</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Hydrogen Content</td>
                <td>{}</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Carbon Content</td>
                <td>{}</td>
                <td>{}</td>
            </tr>
            <tr>
                <td>Transformer short Circuit Probability</td>
                <td>{}</td>
                <td>{}</td>
            </tr>
        </table>
                    </div>""".format(oilTempHID, oilTempSta, loadKVAHID, loadKVASta, hydroCoHID, hydrogenSt, carbonCHID, carbonCSta, pred, predStatus), unsafe_allow_html=True)

    # Correlation Tool in col3
    with col3:
        cols = ['Ambient Temperature', 'Load (kVA)', oilTemp, 'Hydrogen (ppm)', 'Carbon Monoxide (ppm)']
        corr_data = df[cols].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr_data, annot = True, cmap = 'coolwarm')
        plt.title('CORRELATION PLOT')
        st.pyplot(fig)

if uploaded_file is None or not st.session_state:
    st.write("Please upload a transformer historical data for analysis.")
