# Taipei YouBike Info Collector

Data source: [Taipei Open Data Platform](https://data.taipei/dataset/detail?id=c6bc8aed-557d-41d5-bfb1-8da24f78f2fb&fbclid=IwZXh0bgNhZW0CMTAAAR0OHkwnVjiA6gp1TcKB3eOaRkE2Y_muk2TE4K8O9ntiiXeoRrRMbjGzFZY_aem_AYJnjcnXubcbUCy272pvoA95ZEArrcGdDEw4RSXbbknOtsib5f9pyWJ_PDPi610nsfHXH7wkvGDE1TgEu1FAbH1w)

Online Service: [YouBike Info Collector](https://youbike-info-collector.streamlit.app/)

## Program Pipeline
1. get current date
2. generate template
3. get data from API every 30 seconds
4. write data to csv

## Raw Data Description
- sno(站點代號)
- sna(場站中文名稱)
- tot(場站總停車格)
- sbi(場站目前車輛數量)
- sarea(場站區域)
- mday(資料更新時間)
- lat(緯度)
- lng(經度)
- ar(地點)
- sareaen(場站區域英文)
- snaen(場站名稱英文)
- aren(地址英文)
- bemp(空位數量)
- act(全站禁用狀態)
- srcUpdateTime(YouBike2.0系統發布資料更新的時間)
- updateTime(大數據平台經過處理後將資料存入DB的時間)
- infoTime(各場站來源資料更新時間)- infoDate(各場站來源資料更新時間)

## Output Format
Filename: `yyyy-mm-dd.csv`

|Station|Station Number|Station Area|Area|Latitude|Longitude|Total|00:00 Available Rent Bikes|00:1 Available Rent Bikes|...|23:59 Available Rent Bikes|
|---|---|---|---|---|---|---|---|---|---|---|
|捷運科技大樓站|500101001|大安區|復興南路二段235號前|25.02605|121.5436|28|6|10|...|5|
|復興南路二段273號前|500101002|大安區|復興南路二段273號前|25.02565|121.54357|21|2|9|...|5|
|...|...|...|...|...|...|...|...|...|...|...|

## APP
you can use the streamlit website to modify the data and extract the data you want.

run the following command to start the streamlit website locally, or visit the online website [here](https://youbike-info-collector.streamlit.app/)
```bash
streamlit run app.py
```