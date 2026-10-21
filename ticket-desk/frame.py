"""Load the desk's tickets into a pandas table (dataframe)"""
import pandas as pd

def load_frame(path):
    """Return the tickets in tickets.json as a Dataframe with datetime columns"""
    df = pd.read_json(path) # "tickets.json"
    
    # By default Pandas is going to try to give your columns an appropriate 
    # data type. For things like datetime - they'll be read in as strings. 
    # We can easily nudge Pandas to change the type.
    df["opened_at"] = pd.to_datetime(df["opened_at"])
    df["closed_at"] = pd.to_datetime(df["closed_at"])
    
    return df