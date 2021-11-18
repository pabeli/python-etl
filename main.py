import os
import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
import datetime
import sqlite3
from datetime import date
from datetime import timedelta

# Env variables
from dotenv import load_dotenv

# Recover env variables
load_dotenv()

# Database Location
DATABASE_LOCATION = os.getenv('DATABASE_LOCATION')
# User ID on Spotify
USER_ID = os.getenv('USER_ID')
# Token generated on Spotify for Developers
TOKEN = os.getenv('TOKEN')

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
    print(yesterday)

    timestamps = df['timestamp'].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
            raise Exception('At least one song does not come from the last 24 hourse')


if __name__ == '__main__':
    # Prepare the request object
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }

    #### Calculate the period after we want ###
    # We grab today
    today = datetime.datetime.now()
    ## Since we want to run this daily, we will need yesteday
    ## to see the amount of time we will need the API to give us the information
    yesterday = today - datetime.timedelta(days=1)
    # We get the unix timestamp
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Perform the request
    r = requests.get(f"https://api.spotify.com/v1/me/player/recently-played?after={yesterday_unix_timestamp}", headers = headers)

    # Grab the data
    data = r.json()
    
    # The fields we are looking for
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    # Loop through each song to get the info we want
    for song in data['items']:
        song_names.append(song['track']['name'])
        artist_names.append(song['track']['album']['artists'][0]['name'])
        played_at_list.append(song['played_at'])
        timestamps.append(song['played_at'][0:10])
    
    # Create the dict in order to create the pandas dataframe
    song_dict = {
        'song_name': song_names,
        'artist_name': artist_names,
        'played_at': played_at_list,
        'timestamp': timestamps
    }

    # Songs dataframe
    song_df = pd.DataFrame(
        song_dict,
        columns = ['song_name', 'artist_name', 'played_at', 'timestamp']
        )

    # Validate
    if check_if_valid_data(song_df):
        print('Data valid, proceed')
