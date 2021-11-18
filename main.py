from utils.extract import extract_data
from utils.validation import check_if_valid_data
from utils.load import load_data

if __name__ == '__main__':

    # The extract process
    song_df = extract_data()

    # Validation process
    if check_if_valid_data(song_df):
        print('Data valid, proceed')

    # Loading data process
    load_data(song_df)