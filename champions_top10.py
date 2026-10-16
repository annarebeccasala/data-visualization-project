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

# add name
champions = champions.merge(drivers[['driverId', 'forename', 'surname']], on='driverId', how='left')
champions['driver_name'] = champions['forename'] + ' ' + champions['surname']

# count titles per driver
titles_per_driver = champions.groupby('driver_name').size().reset_index(name='titles')

# order titles and select top 10
titles_top10 = titles_per_driver.sort_values('titles', ascending=False).head(11)

# csv
titles_top10.to_csv('champions_top10.csv', index=False)