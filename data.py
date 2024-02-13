# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Red Zone Drone Racing Twilight
#
# > This workbook is an analysis of racing data from the Twilight series from Red Zone Drone Racing
#
# Twilight Round 16 2023/24
# https://rzdr.livefpv.com/results/?p=view_points&id=5270705
#
# Twilight Round 15 2023/24
# https://rzdr.livefpv.com/results/?p=view_points&id=5246600
#
# Twilight Round 14 2023/24
# https://rzdr.livefpv.com/results/?p=view_points&id=5246503
#
# Twilight Round 13 2023/24
# https://rzdr.livefpv.com/results/?p=view_points&id=5203513
#
# Twilight Round 12 2023/24
# https://rzdr.livefpv.com/results/?p=view_points&id=5152914
#
# Twilight Round 11 2023/24
# https://rzdr.livefpv.com/results/?p=view_points&id=5130105
#
# Twilight Round 10 2023/24
# https://rzdr.livefpv.com/results/?p=view_points&id=5107607
#
# Twilight Round 09 2023/24
# https://rzdr.livefpv.com/results/?p=view_points&id=5085695
#
# Twilight Round 08 2023/24
# https://rzdr.livefpv.com/results/?p=view_points&id=5065545
#
# Twilight Round 07 2023/24
# https://rzdr.livefpv.com/results/?p=view_points&id=5043260
#
# Twilight Round 06 2023/24
# https://rzdr.livefpv.com/results/?p=view_points&id=5021027
#
# Twilight Round 05 2023/24
# https://rzdr.livefpv.com/results/?p=view_points&id=4998045
#
# Twilight Round 04 2023/24
# https://rzdr.livefpv.com/results/?p=view_points&id=4977906
#
# Twilight Round 03 2023/24
# https://rzdr.livefpv.com/results/?p=view_points&id=4956897
#
# Twilight Round 02 2023/24
# https://rzdr.livefpv.com/results/?p=view_points&id=4939903
#
# Twilight Round 01 2023/24
# https://rzdr.livefpv.com/results/?p=view_points&id=4922251
#

import csv

# %% _uuid="8f2839f25d086af736a60e9eeb907d3b93b6e0e5" _cell_guid="b1076dfc-b9ad-4769-8c92-a6c4dae69d19"
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


def extract_rows(table_rows, date_th, date_th2, date, date_td2):
    fortune = []
    for tr in table_rows:
        if tr.find("th"):
            td = tr.find_all("th")
            td.append(date_th)
            td.append(date_th2)
            row = [i.text.replace("\t", "").replace("\n", "") for i in td]
            fortune.append(row)
        if tr.find("td"):
            td = tr.find_all("td")
            td.append(date)
            td.append(date_td2)
            row = [i.text.replace("\t", "").replace("\n", "") for i in td]
            fortune.append(row)
    return fortune


def parse_url(url):
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    date_th = soup.new_tag("th")
    date_th.string = "Date"
    date_td = soup.new_tag("td")
    date_th2 = soup.new_tag("th")
    date_th2.string = "Round"
    date_td2 = soup.new_tag("td")

    date = soup.find("h5", class_="page-header text-nowrap pull-left")

    round = soup.find("h3", class_="page-header").text.strip()
    round = round.split()[2]  # Assuming the date format is always after the icon
    date_td2.string = round

    table = soup.find("table").find("tbody")
    table_rows = table.find_all("tr")
    data = extract_rows(table_rows, date_th, date_th2, date, date_td2)
    columns = extract_rows(
        soup.find("table").find("thead").find_all("tr"),
        date_th,
        date_th2,
        date,
        date_td2,
    )

    fortune = pd.DataFrame(data)
    fortune.columns = columns[-1]
    return fortune


data = []
for url in [
    "https://rzdr.livefpv.com/results/?p=view_points&id=5270705",
    "https://rzdr.livefpv.com/results/?p=view_points&id=5246503",
    "https://rzdr.livefpv.com/results/?p=view_points&id=5246600",
    "https://rzdr.livefpv.com/results/?p=view_points&id=5270705",
    "https://rzdr.livefpv.com/results/?p=view_points&id=5246600",
    "https://rzdr.livefpv.com/results/?p=view_points&id=5246503",
    "https://rzdr.livefpv.com/results/?p=view_points&id=5203513",
    "https://rzdr.livefpv.com/results/?p=view_points&id=5152914",
    "https://rzdr.livefpv.com/results/?p=view_points&id=5130105",
    "https://rzdr.livefpv.com/results/?p=view_points&id=5107607",
    "https://rzdr.livefpv.com/results/?p=view_points&id=5085695",
    "https://rzdr.livefpv.com/results/?p=view_points&id=5065545",
    "https://rzdr.livefpv.com/results/?p=view_points&id=5043260",
    "https://rzdr.livefpv.com/results/?p=view_points&id=5021027",
    "https://rzdr.livefpv.com/results/?p=view_points&id=4998045",
    "https://rzdr.livefpv.com/results/?p=view_points&id=4977906",
    "https://rzdr.livefpv.com/results/?p=view_points&id=4956897",
    "https://rzdr.livefpv.com/results/?p=view_points&id=4939903",
    "https://rzdr.livefpv.com/results/?p=view_points&id=4922251",
]:
    data.append(parse_url(url))

data = pd.concat(data, axis=0)
data.to_csv("dataset.csv")
