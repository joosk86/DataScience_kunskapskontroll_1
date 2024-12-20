import pandas as pd
import sqlite3
import logging
logger = logging.getLogger()

 
con = sqlite3.connect('beer.db')

df_beer = pd.read_csv('beer_profile_and_ratings.csv', index_col=False, usecols=['Name', 'Style', 'ABV', 'review_overall', 'number_of_reviews'])
 


lager_df = df_beer[df_beer['Style'].str.startswith('Lager')] 

 
lager_df.to_sql('lager_beer', con, if_exists='replace', index=False)
 
def check_beer_in_df_beer(df_beer, name, percentage):
    """
    Kontrollera om en specifik öl har en viss alkoholhalt.
 
    Example:
        >>> test_df = pd.DataFrame({"Name": ["Budweiser", "Singha"], "ABV": [5, 5]})
        >>> check_beer_in_df_beer(test_df, ["Budweiser", "Singha"], [5, 5])
        True
        >>> check_beer_in_df_beer(test_df, ["Estrella Damm", "Helles Lager"], [5, 5])
        False
    """
    return not df_beer[(df_beer['Name'] == name) & (df_beer['ABV'] == percentage)].empty
 
print(check_beer_in_df_beer(lager_df, "Budweiser", 5))
print(check_beer_in_df_beer(lager_df, "Singha", 5))
print(check_beer_in_df_beer(lager_df, "Estrella Damm", 5))
print(check_beer_in_df_beer(lager_df, "Helles Lager", 5))
 
if __name__ == "__main__":
    import doctest
    doctest.testmod()