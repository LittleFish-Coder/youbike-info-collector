import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import os

# icon
icon = Image.open("src/favicon.ico")

# Set page config
st.set_page_config(
    page_title="YouBike Collector",
    page_icon=icon,
    layout="centered",
)

# Title
st.title("YouBike Collector")


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8-sig")


date_list = os.listdir("result")
date_list = [date.replace(".csv", "") for date in date_list]

# selectbox for existing dates
selected_date = st.selectbox(
    "Select a date",
    date_list,
    index=0,
)

# selectbox for time interval: 1min, 5min, 15min, 30min, 60min, 120
seletecd_time_interval = st.selectbox(
    "Select a time interval",
    ["1 min", "5 min", "15 min", "30 min", "60 min"],
    index=0,
)

# read data
if selected_date:
    df = pd.read_csv(f"result/{selected_date}.csv")
    st.dataframe(df)

# download button
if seletecd_time_interval:
    time_interval = int(seletecd_time_interval.split(" ")[0])
    if time_interval == 1:
        # convert the data to csv
        csv = convert_df(df)
        st.download_button(
            "Press to Download",
            csv,
            f"{selected_date}.csv",
            "text/csv",
            key="download-csv",
        )
    else:
        # prepare the data
        with st.spinner("Wait for it..."):
            df = pd.read_csv(f"result/{selected_date}.csv")
            candidate_time = [f"{hour:02d}:{minute:02d} Available Rent Bikes" for hour in range(0, 24) for minute in range(0, 60, time_interval)]

            # the original data will contain the time in the format of "hh:mm" and with the interval of 1 minute
            # we need to filter the data to match the selected time interval

            attributes = df.columns[:7].to_list()
            for attr in df.columns[7:]:
                if attr in candidate_time:
                    attributes.append(attr)
            df = df[attributes]

            # convert the data to csv
            csv = convert_df(df)

            st.download_button(
                "Press to Download",
                csv,
                f"{selected_date}_{time_interval}min.csv",
                "text/csv",
                key="download-csv",
            )
