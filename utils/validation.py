import pandas as pd
import datetime

def check_if_valid_data(df: pd.DataFrame):
    """
    Function to check if the date is in a valid format
    """
    # Check if the DataFrame is empty
    if df.empty:
        print('No songs in the past 24hs!')
        return False
    
    # Since you can't simultaneously listen to 2 different songs
    # our primary key is played_at
    if not pd.Series(df['played_at']).is_unique:
        # If the played at is not unique, then primary key check is violated
        raise Exception('Primary key check is violated!')
    
    # Check for empty values
    if df.isnull().values.any():
        raise Exception('Null values!')

    # Check we are only saving songs from yesterday
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    timestamps = df['timestamp'].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
            raise Exception('At least one song does not come from the last 24 hourse')