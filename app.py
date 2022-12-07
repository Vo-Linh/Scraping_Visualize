from importlib.resources import path
from flask import Flask, request
from flask import render_template

from scraping import getRawData, getUrl
from convert2DF import convert2DF
from visualize import statisticsWeather, correlationWeather

from datetime import datetime

import os

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def getDate():
    if request.method == 'POST':
        month = request.form['month']
        year, month = month.split("-")

    else:
        current_dateTime = datetime.now()
        year = current_dateTime.year
        month = current_dateTime.month
        date = current_dateTime.day

        if date < 7:
            month -= 1

    url = getUrl(year, month)
    raw_data = getRawData(url)
    df, date = convert2DF(raw_data)

    # ========== Get Data ===================
    url = getUrl(year, month)  # year, month
    raw_data = getRawData(url)
    df, date = convert2DF(raw_data)

    # ========== Visualize ===================
    avg_humi_path = statisticsWeather(df, date, "Average humidity")
    avg_temp_path = statisticsWeather(df, date, "Average temperature")
    avg_wind_path = statisticsWeather(df, date, "Average windspeed")

    corr_hum_temp = correlationWeather(
        df, "Average humidity", "Average temperature")
    corr_wind_temp = correlationWeather(
        df, "Average windspeed", "Average temperature")
    corr_wind_hum = correlationWeather(
        df, "Average windspeed", "Average humidity")

    sta = [avg_humi_path, avg_temp_path, avg_wind_path]
    corr = {
        "humidity_temperature": corr_hum_temp,
        "windspeed_temperature": corr_wind_temp,
        "windspeed_humidity": corr_wind_hum
    }
    return render_template("index.html", path_sta=sta, path_corr=corr, month = month, year = year)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
