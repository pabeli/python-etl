import os
import sqlalchemy
import pandas as pd
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
import requests
import datetime
import sqlite3

from datetime import timedelta

from utils.extract import extract_data

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

    timestamps = df['timestamp'].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
            raise Exception('At least one song does not come from the last 24 hourse')

if __name__ == '__main__':

    # The extract process
    song_df = extract_data()


    # Validate
    if check_if_valid_data(song_df):
        print('Data valid, proceed')

    # Load
    # Create the database
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    # Create the connection
    conn = sqlite3.connect('myplayedtracks.sqlite')
    # Create the pointer to direct to specific rows into the database
    cursor = conn.cursor()
    # Metadata object that will hold the table
    meta = MetaData(engine)
    # If the table does not exist
    insp = sqlalchemy.inspect(engine)
    if not insp.has_table('my_played_tracks'):
        # Create the table
        sql_create_table = Table(
            'my_played_tracks',
            meta,
            Column('song_name', String),
            Column('artist_name', String),
            Column('played_at', String, primary_key = True),
            Column('timestamp', String)
        )
    meta.create_all()
    
    try:
        song_df.to_sql('my_played_tracks', engine, index=False, if_exists='append')
    except:
        print('Data already exists in the database')
    
    conn.close()

    print('Close database successfully')
