import requests
import pandas as pd
import time
from datetime import datetime
import os
import pytz

api_url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
time_interval = 30  # 30 minutes
time_sleep = 30 * 60  # 30 minutes
candidate_time = [f"{hour:02d}:{minute:02d}" for hour in range(0, 24) for minute in range(0, 60, time_interval)]
destination_folder = "result"
template_csv = "src/template.csv"
# create a timezone object for GMT+8
gmt8 = pytz.timezone("Asia/Taipei")


def generate_template(time_str: str):

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # read template
    df = pd.read_csv(template_csv)
    # write data to csv
    write_data(df, f"{destination_folder}/{time_str}.csv")

    # data = get_data()
    # station_name = []  # 站名
    # station_number = []  # 站點編號
    # station_area = []  # 站點區域
    # area = []  # 站點行政區
    # latitude = []  # 緯度
    # longitude = []  # 經度
    # total = []  # 總停車格

    # for i in range(len(data)):
    #     station_name.append(data[i]["sna"].replace("YouBike2.0_", ""))
    #     station_number.append(data[i]["sno"])
    #     station_area.append(data[i]["sarea"])
    #     area.append(data[i]["ar"])
    #     latitude.append(data[i]["latitude"])
    #     longitude.append(data[i]["longitude"])
    #     total.append(data[i]["total"])

    # available_rent_bikes_names = [f"{str(hh).zfill(2)}:{str(mm).zfill(2)} Available Rent Bikes" for hh in range(0, 24) for mm in range(0, 60, time_interval)]

    # # |Station|Station Number|Station Area|Area|Latitude|Longitude|Total|hh:mm Available Rent Bikes|...|
    # column_headers = ["Station", "Station Number", "Station Area", "Area", "Latitude", "Longitude", "Total"]

    # df = pd.DataFrame(
    #     list(zip(station_name, station_number, station_area, area, latitude, longitude, total)),
    #     columns=column_headers,
    # )

    # # add columns for available rent bikes
    # for name in available_rent_bikes_names:
    #     df[name] = 0

    # # write data to csv
    # write_data(df, f"result/{time_str}.csv")


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
    print(f"Time interval: {time_interval} minutes")

    while True:
        # get current date
        # current_date = time.strftime("%Y-%m-%d", time.localtime())
        current_date = datetime.now(gmt8).strftime("%Y-%m-%d")
        print(f"Current date: {current_date}")

        # generate template if not exist
        if not os.path.exists(f"{destination_folder}/{current_date}.csv"):
            print(f"Generate template for {current_date}")
            generate_template(current_date)

        # get the df
        df = pd.read_csv(f"{destination_folder}/{current_date}.csv")

        # get current time
        # current_time = time.strftime("%H:%M", time.localtime())
        current_time = datetime.now(gmt8).strftime("%H:%M")
        print(f"Current time: {current_time}")
        rest_time = candidate_time.copy()
        for time_str in candidate_time:
            # compare the current time with the candidate time
            if current_time > time_str:
                # print(f"current_time: {current_time} > time_str:{time_str}")
                print(f"Remove {time_str}")
                rest_time.remove(time_str)
        # print(f"Rest time: {rest_time}")

        # sleep until the next candidate time
        print(f"Sleep until: {rest_time[0]}")
        # parse the time
        current_time = datetime.strptime(current_time, "%H:%M")
        target_time = datetime.strptime(rest_time[0], "%H:%M")
        # subtract the time
        sleep_time = target_time - current_time
        sleep_time = sleep_time.total_seconds()
        print(f"Sleep time: {sleep_time}")

        # sleep
        time.sleep(sleep_time)

        # request data from api for every 30 minutes
        for time_str in rest_time:
            print(f"Current time: {time_str}")
            data = get_data()
            available_bikes = []  # 目前車輛數量
            for i in range(len(data)):
                available_bikes.append(data[i]["available_rent_bikes"])
            print(available_bikes)
            # update the df
            df[f"{time_str} Available Rent Bikes"] = available_bikes
            time.sleep(time_sleep)

        # write data to csv
        print(f"Finish collecting data for {current_date}")
        print(f"Write data to {destination_folder}/{current_date}.csv")
        write_data(df, f"{destination_folder}/{current_date}.csv")
        print()
        # Sleep for 30 minutes...
        time.sleep(time_sleep)
