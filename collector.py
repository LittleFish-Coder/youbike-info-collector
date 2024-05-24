import requests
import pandas as pd
import time
from datetime import datetime
import os
import pytz

api_url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
time_sleep = 30  # 30 seconds
destination_folder = "result"
# create a timezone object for GMT+8
gmt8 = pytz.timezone("Asia/Taipei")


def generate_template(time_str: str):

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    data = get_data()
    station_name = []  # 站名
    station_number = []  # 站點編號
    station_area = []  # 站點區域
    area = []  # 站點行政區
    latitude = []  # 緯度
    longitude = []  # 經度
    total = []  # 總停車格

    for i in range(len(data)):
        station_name.append(data[i]["sna"].replace("YouBike2.0_", ""))
        station_number.append(data[i]["sno"])
        station_area.append(data[i]["sarea"])
        area.append(data[i]["ar"])
        latitude.append(data[i]["latitude"])
        longitude.append(data[i]["longitude"])
        total.append(data[i]["total"])

    # |Station|Station Number|Station Area|Area|Latitude|Longitude|Total|
    column_headers = ["Station", "Station Number", "Station Area", "Area", "Latitude", "Longitude", "Total"]

    df = pd.DataFrame(
        list(zip(station_name, station_number, station_area, area, latitude, longitude, total)),
        columns=column_headers,
    )

    # write data to csv
    write_data(df, f"result/{time_str}.csv")


def get_data():
    response = requests.get(api_url)
    return response.json()


def write_data(df: pd.DataFrame, file_path: str = "output.csv"):
    df.to_csv(file_path, index=False, encoding="utf-8-sig")


if "__main__" == __name__:

    """
    pipeline
    1. get current date
    2. generate template
    3. get data from API every 30 minutes
    4. write data to csv
    """

    print("Start collecting data...")

    while True:
        # get current date
        current_date = datetime.now(gmt8).strftime("%Y-%m-%d")
        print(f"Current date: {current_date}")

        # generate template if not exist
        if not os.path.exists(f"{destination_folder}/{current_date}.csv"):
            print(f"Generate template for {current_date}")
            generate_template(current_date)

        # get the df
        df = pd.read_csv(f"{destination_folder}/{current_date}.csv")

        # keep requesting data from api until 23:59
        # if the current time is 23:59, then start the next day
        while True:
            # get current time
            current_time = datetime.now(gmt8).strftime("%H:%M")
            print(f"Current time: {current_time}")

            try:
                # get data from API
                data = get_data()

                # get the data returned time ("srcUpdateTime": "YYYY-MM-DD HH:MM:SS")
                src_update_time = data[0]["srcUpdateTime"]
                src_date, src_time = src_update_time.split(" ")

                # if the src_date is not equal to current_date, then break the loop
                if src_date != current_date:
                    break
                else:
                    HH, MM, SS = src_time.split(":")
                    time_str = f"{HH}:{MM}"

                available_bikes = []  # current available bikes
                station_names = []  # station names
                for i in range(len(data)):
                    station_names.append(data[i]["sna"].replace("YouBike2.0_", ""))
                    available_bikes.append(data[i]["available_rent_bikes"])

                # create a new DataFrame with the available bikes
                new_df = pd.DataFrame(
                    {
                        "Station": station_names,
                        f"{time_str} Available Rent Bikes": available_bikes,
                    }
                )

                # merge the new_df with the original df and drop the duplicated columns
                df = pd.merge(df, new_df, on="Station", how="left")

                # write data to csv
                write_data(df, f"{destination_folder}/{current_date}.csv")

                time.sleep(time_sleep)
            except Exception as e:
                print(f"Error: {e}")
                continue

        # write data to csv
        print(f"Finish collecting data for {current_date}")
        print(f"Write data to {destination_folder}/{current_date}.csv")
        write_data(df, f"{destination_folder}/{current_date}.csv")
        print()
