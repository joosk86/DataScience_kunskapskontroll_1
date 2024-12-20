import pandas as pd
import sqlite3
import logging
import requests

# logging
logging.basicConfig(
    filename=r'C:\Users\john_\Documents\Tuc_ds\log.log',
    level=logging.INFO,
    format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

Logger = logging.getLogger(__name__)

# Create connection and database file
con = sqlite3.connect('beer.db')

def my_function():
    try:
        # try to read the CSV
        df_beer = pd.read_csv('beer_profile_and_ratings.csv', index_col=False, usecols=['Name', 'Style', 'ABV', 'review_overall', 'number_of_reviews'])
        logging.info("CSV file read successfully.")
        return df_beer

    except FileNotFoundError:
        # file not found, log the message
        logging.warning("CSV file not found, trying to find data from http://hd.se")
        try:
            # try to find data online
            response = requests.get("http://hd.se")
            if response.status_code == 200:
                logging.info("Data found successfully from http://hd.se.")
                
            else:
                logging.error(f"Failed to find data from http://hd.se. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
        
        return None  # Return None if no data is found

# Call the function
df_beer = my_function()

if df_beer is not None:
    # Filter Lager beer
    lager_df = df_beer[df_beer['Style'].str.startswith('Lager')]
    logging.info("Filtered Lager beer styles.")

    # Dataframe to SQL
    try:
        lager_df.to_sql('lager_beer', con, if_exists='replace')
        logging.info("lager_beer data written to SQL database.")
    except Exception as e:
        logging.error(f"Error writing to SQL database: {e}")
else:
    logging.error("Failed to create dataframe from CSV or URL.")
