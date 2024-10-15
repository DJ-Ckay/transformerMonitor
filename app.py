import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set the page title and layout
st.set_page_config(page_title="Transformer Dashboard", layout="wide")
st.markdown("<p style='text-align: right;'>Contact Us: Kehinde Clement, Phone No: 08121111830</p>", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center;'>Transformer 00001</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Welcome back to Transformer Dashboard 🌩️</p>", unsafe_allow_html=True)

# File uploader widget
uploaded_file = st.file_uploader("Choose a file", type=["csv", "txt"])

if uploaded_file is not None:
    # Load dataset
    df = pd.read_csv(uploaded_file, index_col="DATE")
    # pd.to_datetime(df['Date'])

    df.index = pd.to_datetime(df.index, dayfirst=True)
    oilTemp = 'Oil Temperature' if 'Oil Temperature' in df.columns else 'Oil Temperature (?C)'
    df['Carbon Monoxide (ppm)'] = df['Carbon Monoxide (ppm)'].apply(lambda x: x*2)
    df['Oil Temperature S2'] = df[oilTemp] + np.random.uniform(-0.6, 0.8, df.shape[0])
    df['Oil Temperature Avg'] = np.mean(df[['Oil Temperature S2', oilTemp]].values, axis = 1)

    dateRange = st.radio('SELECT DATE RANGE',['LAST YEAR','LAST 6MONTH', 'LAST 3MONTH', 'LAST 1MONTH','LAST 1WEEK', 'LAST 1DAY'],horizontal = True)
    if dateRange == 'LAST YEAR':
        # Filter data for the last year
        last_year = df.last("1Y")
        
        # Resample data to get monthly averages
        monthly_avg = last_year.resample('M').mean()
        
        # Extract oil temperature, ambient temperature, and load for the last year
        oil_temp = monthly_avg[oilTemp]
        ambient_temp = monthly_avg['Ambient Temperature']
        load = monthly_avg['Load (kVA)']
        months = oil_temp.index.strftime("%b")

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
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Simulate the Load Chart
        with col2:
            st.subheader("🔋 LOAD")
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.bar(months, load, color='purple')
            ax.set_ylabel('Load (Kva)')
            ax.set_yticks(np.arange(0, max(load) + 50, 50))
            plt.xticks(rotation=45)
            st.pyplot(fig)
        

    elif dateRange == 'LAST 6MONTH':
        # Get data for the last 6 months
        last_six_months = df.last("6M")

        # Resample data to get monthly averages for the last 6 months
        monthly_avg = last_six_months.resample('M').mean()

        # Extract oil temperature, ambient temperature, and load for the last 6 months
        oil_temp = monthly_avg['Oil Temperature (?C)']
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
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Simulate the Load Chart
        with col2:
            st.subheader("🔋 LOAD")
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.bar(months, load, color='purple')
            ax.set_ylabel('Load (Kva)')
            ax.set_yticks(np.arange(0, max(load) + 50, 50))
            plt.xticks(rotation=45)
            st.pyplot(fig)

    elif dateRange == 'LAST 3MONTH':
        # Get data for the last 3 months
        last_three_months = df.last("3M")

        # Resample data to get monthly averages for the last 3 months
        monthly_avg = last_three_months.resample('M').mean()

        # Extract oil temperature, ambient temperature, and load for the last 3 months
        oil_temp = monthly_avg['Oil Temperature (?C)']
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
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Simulate the Load Chart
        with col2:
            st.subheader("🔋 LOAD")
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.bar(months, load, color='purple')
            ax.set_ylabel('Load (Kva)')
            ax.set_yticks(np.arange(0, max(load) + 50, 50))
            plt.xticks(rotation=45)
            st.pyplot(fig)

    elif dateRange == 'LAST 1MONTH':
        last_month = df.last("1M")

        # Resample data to get daily averages for the last month
        daily_avg = last_month.resample('W').mean()

        # Extract oil temperature, ambient temperature, and load for the last month
        oil_temp = daily_avg['Oil Temperature (?C)']
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
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Simulate the Load Chart
        with col2:
            st.subheader("🔋 LOAD")
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.bar(weeks, load, color='purple')
            ax.set_ylabel('Load (Kva)')
            ax.set_yticks(np.arange(0, max(load) + 50, 50))
            plt.xticks(rotation=45)
            st.pyplot(fig)
    elif dateRange == 'LAST 1WEEK':
        last_week = df.last("7D")

        # Resample data to get daily averages for the last week
        daily_avg = last_week.resample('D').mean()

        # Extract oil temperature, ambient temperature, and load for the last week
        oil_temp = daily_avg['Oil Temperature (?C)']
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
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)
        # Simulate the Load Chart
        with col2:
            st.subheader("🔋 LOAD")
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.bar(days, load, color='purple')
            ax.set_ylabel('Load (Kva)')
            ax.set_yticks(np.arange(0, max(load) + 50, 50))
            plt.xticks(rotation=45)
            st.pyplot(fig)

    elif dateRange == 'LAST 1DAY':
        # Get data for the last 1 day
        last_day = df.last("1D")

        # Resample data to get hourly averages for the last day
        hourly_avg = last_day.resample('2H').mean()

        # Extract oil temperature, ambient temperature, and load for the last day
        oil_temp = hourly_avg['Oil Temperature (?C)']
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
            plt.xticks(rotation=45)
            st.pyplot(fig)
        with col2:
            st.subheader("🔋 LOAD")
            fig, ax = plt.subplots(figsize=(4, 2))
            ax.bar(hours, load, color='purple')
            ax.set_ylabel('Load (Kva)')
            ax.set_yticks(np.arange(0, max(load) + 50, 50))
            plt.xticks(rotation=45)
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
                    <li><b> Transformer's Age</b>: 12 Years</li>
                    <li><b> Period of Data Measurement</b>: 15 days</li>
                    <li><b> Average Ambient Temperature</b>: {:.2f}°C</li>
                    <li><b> Average Oil Temperature</b>: {:.2f}°C</li>
                    <li><b> Average Load</b>: {:.2f} Kva</li>
                    </ul>
                    </div>
                    """.format(ambient_temp.mean(), oil_temp.mean(), load.mean()), unsafe_allow_html=True)

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
                <td>0.6</td>
                <td>At Risk</td>
            </tr>
            <tr>
                <td>Transformer Load</td>
                <td>0.3</td>
                <td>Watch</td>
            </tr>
            <tr>
                <td>Moisture Content</td>
                <td>0.1</td>
                <td>Watch</td>
            </tr>
            <tr>
                <td>Transformer short Circuit Probability</td>
                <td>0.3</td>
                <td>Watch</td>
            </tr>
        </table>
                    </div>""", unsafe_allow_html=True)

    # Correlation Tool in col3
    with col3:
        corr_data = np.random.rand(4, 4)
        fig, ax = plt.subplots()
        cax = ax.matshow(corr_data, cmap="Purples")
        fig.colorbar(cax)
        ax.set_xticks(np.arange(4))
        ax.set_yticks(np.arange(4))
        ax.set_xticklabels(['Oil', 'Temp', 'Load', 'Moist'])
        ax.set_yticklabels(['Moist', 'Load', 'Temp', 'Oil'])
        plt.savefig('corrFigure.png')
        st.markdown("<h3 class = 'corrPlot'>CORRELATION PLOT</h3>", unsafe_allow_html=True)
        st.pyplot(fig)

if uploaded_file is None or not st.session_state:
    st.write("Please upload a transformer historical data for analysis.")
