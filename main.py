from utils.extract import extract_data
from utils.validation import check_if_valid_data
from utils.load import load_data
import logging

# Logger initialization
logging.basicConfig(format='[%(levelname)s]: %(message)s', level=logging.DEBUG)

if __name__ == '__main__':

    # The extract process
    logging.info('Starting data extract...')
    song_df = extract_data()

    # Validation process
    logging.info('Starting validation process...')
    if check_if_valid_data(song_df):
        logging.info('Data valid, proceed')

    # Loading data process
    logging.info('Starting loading process...')
    load_data(song_df)