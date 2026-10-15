"""Load the desk's tickets into a pandas table."""
import pandas as pd


def load_frame(path):
    """Return the tickets in the JSON file as a DataFrame with datetime columns."""
    df = pd.read_json(path)
    df["opened_at"] = pd.to_datetime(df["opened_at"])
    df["closed_at"] = pd.to_datetime(df["closed_at"])
    df["hours"] = (df["closed_at"] - df["opened_at"]).dt.total_seconds() / 3600
    return df


def status_table(df):
    """Return how many tickets are in each status."""
    return df["status"].value_counts()


def hours_by_priority(df):
    """Return the mean hours to resolve for each priority."""
    return df.groupby("priority")["hours"].mean()
