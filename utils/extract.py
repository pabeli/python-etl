import os
import pandas as pd
import requests
import datetime
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

def extract_data():
    """
    Function that allows the download of information from 
    Spotify
    """

    ### Prepare the headers ###
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }

    #### Calculate the period after we want ###
    # We grab today
    today = datetime.datetime.now()
    
    # Since we want to run this daily, we will need yesteday
    # to see the amount of time we will need the API to give us the information
    yesterday = today - timedelta(days=1)
    
    # We get the unix timestamp
    yesterday_unix_timestamp = int(yesterday.timestamp())
    
    ### Perform the request ###
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = headers)

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
    
    return song_df
    