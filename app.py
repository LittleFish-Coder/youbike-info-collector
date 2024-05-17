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
st.title("YouBike Info Collector")


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8-sig")


def rent_to_return(df):
    df = df.copy()
    for i in range(7, len(df.columns)):
        if "Available Rent Bikes" in df.columns[i]:
            diff = df["Total"] - df[df.columns[i]]
            df[df.columns[i].replace("Available Rent Bikes", "Available Return Bikes")] = diff
    return df


date_list = os.listdir("result")
date_list.sort()
date_list = [date.replace(".csv", "") for date in date_list]
date_list.remove("template")
date_list.insert(0, "template")  # make the template as the first option

expander = st.expander("說明")
with expander:
    st.write("- GitHub: https://github.com/LittleFish-Coder/youbike-info-collector")
    st.write("- 本專案為台北市YouBike即時資訊服務，此服務可以收集指定日期的YouBike站點即時資訊")
    st.markdown(
        "- 資料來源: [台北市資料大平台](https://data.taipei/dataset/detail?id=c6bc8aed-557d-41d5-bfb1-8da24f78f2fb&fbclid=IwZXh0bgNhZW0CMTAAAR0OHkwnVjiA6gp1TcKB3eOaRkE2Y_muk2TE4K8O9ntiiXeoRrRMbjGzFZY_aem_AYJnjcnXubcbUCy272pvoA95ZEArrcGdDEw4RSXbbknOtsib5f9pyWJ_PDPi610nsfHXH7wkvGDE1TgEu1FAbH1w)"
    )


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

# selectbox for showing available rent/return bikes
selected_bike = st.selectbox(
    "Select a bike type",
    ["Available Rent Bikes", "Available Return Bikes"],
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

            # if user choose to show available return bikes
            if selected_bike == "Available Return Bikes":
                df = rent_to_return(df)

            # convert the data to csv
            csv = convert_df(df)

            st.download_button(
                "Press to Download",
                csv,
                f"{selected_date}_{time_interval}min.csv",
                "text/csv",
                key="download-csv",
            )
