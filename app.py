import datetime

import pandas as pd
import streamlit as st

data = pd.read_csv("dataset.csv")
data["Date"] = pd.to_datetime(data["Date"])

data["Round"] = data["Round"].astype(int)

data = data.sort_values("Round")


def parse_result(x):
    if isinstance(x["Result"], float):
        return x["Result"]
    else:
        if ":" in x["Result"]:
            fmt = "%M:%S.%f"
        else:
            fmt = "%S.%f"
        start = datetime.datetime(year=1900, day=1, month=1)
        return (datetime.datetime.strptime(x["Result"], fmt) - start).total_seconds()


data["Result"] = data.apply(parse_result, axis=1)


options = data["Driver"].tolist()
driver = st.sidebar.selectbox("driver", options, index=options.index("BUGLISH"))
subset = data[data["Driver"] == driver]
st.dataframe(subset)

st.bar_chart(subset, x="Date", y="Result")

avg_time = data["Result"].mean()
driver_time = subset["Result"].mean()

st.text(f"Average time: {avg_time}, Driver time: {driver_time}")

# this is broken!
# shouldn't be using the subset["Round"] in .loc
subset["avg-score"] = (
    data[["Result", "Round"]].groupby("Round").mean().loc[subset["Round"]].values
)
subset["difference"] = subset["Result"] - subset["avg-score"]
st.bar_chart(subset, x="Date", y="difference")

st.dataframe(subset[["Round", "Result", "avg-score", "difference"]])
