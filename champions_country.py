import pandas as pd

# loading datasets
drivers = pd.read_csv('files/drivers.csv')
driver_standings = pd.read_csv('files/driver_standings.csv')
races = pd.read_csv('files/races.csv')

# find driver champions
standings_races = driver_standings.merge(races[['raceId','year','round']], on='raceId', how='inner')
final_rounds = standings_races.groupby('year')['round'].max().reset_index()
final_standings = standings_races.merge(final_rounds, on=['year','round'], how='inner')

champions = final_standings[final_standings['position'] == 1][['year','driverId']]
champions['champion_status'] = 'Champion'

# add nationality
champions = champions.merge(drivers[['driverId','nationality']], on='driverId', how='left')

# mapping nationality -> country
nationality_to_country = {
    'British': 'United Kingdom',
    'German': 'Germany',
    'Dutch': 'Netherlands',
    'Finnish': 'Finland',
    'Brazilian': 'Brazil',
    'French': 'France',
    'Spanish': 'Spain',
    'Australian': 'Australia',
    'Austrian': 'Austria',
    'Italian': 'Italy',
    'Canadian': 'Canada',
    'South African': 'South Africa',
    'American': 'United States of America',
    'Argentine': 'Argentina',
    'New Zealander': 'New Zealand'
}

champions['country'] = champions['nationality'].map(nationality_to_country)

# delete duplicates
champions_unique = champions.drop_duplicates(subset=['driverId'])

# count titles by country
titles_by_country = champions_unique.groupby('country').size().reset_index(name='num_champions')

# csv
titles_by_country.to_csv('champions_country.csv', index=False)