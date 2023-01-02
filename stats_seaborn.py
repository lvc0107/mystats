#!/usr/bin/env python3
"""
Created on Sat Dec 31 04:34:31 2022

@author: luisvargas
"""

from csv import writer
from datetime import date

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sbn

# Start and end of the date range to extract
start_date = "2020-06"
end_date = date.today()
end_date_input_format = end_date.strftime("%d-%m-%y")
end_date_output_format = end_date.strftime("%Y-%m")
data_columns = ["weight", "ave", "sp"]


DATA_FILE = "data.csv"


def load_data():
    sbn.set(rc={"figure.figsize": (20, 6)})

    daily_data = pd.read_csv(
        DATA_FILE, usecols=[0, 1, 2, 3], index_col=0, parse_dates=True
    )

    monthly_mean = daily_data[data_columns].resample("M").mean(numeric_only=True)

    return daily_data, monthly_mean


def append_currrent_day():

    with open(DATA_FILE, "r+") as f_object:
        final_line = f_object.readlines()[-1]

        if not end_date_input_format in final_line:
            # Pass this file object to csv.writer()
            # and get a writer object
            today_data = (end_date_input_format, "", "", "")
            writer_object = writer(f_object)
            writer_object.writerow(today_data)

        f_object.close()


def plot_data(daily_data, monthly_mean):
    # Plot daily and monthly resampled time series together
    fig, ax = plt.subplots()
    ax.plot(
        daily_data.loc[start_date:end_date_output_format, "weight"],
        marker="o",
        markersize=5,
        linestyle="-",
        linewidth=0.5,
        label="Daily",
        color="blue",
    )

    ax.plot(
        monthly_mean.loc[start_date:end_date_output_format, "weight"],
        marker="o",
        markersize=5,
        linestyle="-",
        label="Montlhy Mean",
        color="red",
    )

    trend_line = (
        daily_data[data_columns]
        .rolling(window=365, center=True, min_periods=1)
        .mean(numeric_only=True)
    )

    ax.plot(
        trend_line.loc[start_date:end_date_output_format, "weight"],
        color="orange",
        linewidth=3,
        label="Trend",
    )

    ax.set_ylabel("Weight")
    ax.legend()


def main():
    append_currrent_day()
    daily_data, monthly_mean = load_data()
    plot_data(daily_data, monthly_mean)


main()
