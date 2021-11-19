import os
import sqlalchemy
import pandas as pd
from sqlalchemy import Table, Column, String, MetaData
from sqlalchemy.orm import sessionmaker
import sqlite3
import logging

# Logger initialization
logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.DEBUG)

# Env variables
from dotenv import load_dotenv

# Recover env variables
load_dotenv()

# Database Location
DATABASE_LOCATION = os.getenv('DATABASE_LOCATION')

def load_data(song_df: pd.DataFrame):
    """
    Function that allows loading data into database
    """
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
        logging.info('Data already exists in the database')
    
    conn.close()

    logging.info('Close database successfully')