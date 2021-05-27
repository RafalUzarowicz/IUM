import pandas as pd
import numpy as np


def apply(df: pd.DataFrame) -> pd.DataFrame:
    df = __preprocess_time(df)
    df = __transform_columns(df)
    df = __encode_cyclical(df)
    return df


def __preprocess_time(df: pd.DataFrame):
    df["purchase_timestamp"] = pd.to_datetime(df["purchase_timestamp"], format='%Y-%m-%dT%H:%M', errors="coerce")
    return df


def __transform_columns(df: pd.DataFrame):
    df["street_name"] = df["street"].apply(lambda x: x.split(" ")[1])
    df["street_name*num"] = df["street"].apply(lambda x: x.split(" ")[1] + " " + x.split(" ")[2])
    df = __add_city_street(df)
    df = df.drop(labels=["street"], axis=1)

    df["purchase_day_of_week"] = df["purchase_timestamp"].apply(lambda x: x.dayofweek)
    return df


def __add_city_street(df: pd.DataFrame):
    cities = df["city"].to_list()
    streets = df["street_name"].to_list()

    city_street = [cities[i] + "/" + streets[i] for i in range(len(cities))]

    df["city*stret_name"] = city_street
    return df


def __encode_cyclical(df: pd.DataFrame):
    df["purchase_month"] = df["purchase_timestamp"].apply(lambda x: x.month)
    df["purchase_day"] = df["purchase_timestamp"].apply(lambda x: x.day)
    df["purchase_hour"] = df["purchase_timestamp"].apply(lambda x: x.hour)
    df["purchase_min"] = df["purchase_timestamp"].apply(lambda x: x.minute)

    cyclical = [("purchase_month", 12), ("purchase_day", 30), ("purchase_hour", 24),
                ("purchase_min", 60), ("purchase_day_of_week", 7)]

    for feature, cycle in cyclical:
        df = __encode_one_cyclical(df, feature, cycle)
        df = df.drop(feature, axis=1)
    df = df.drop("purchase_timestamp", axis=1)
    return df


def __encode_one_cyclical(df, feature, num):
    df[feature + "_sin"] = np.sin(df[feature] * (2 * np.pi / num))
    df[feature + "_cos"] = np.cos(df[feature] * (2 * np.pi / num))
    return df
