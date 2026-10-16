import pandas as pd

#loading datasets
drivers = pd.read_csv('files/drivers.csv')
races = pd.read_csv('files/races.csv')
results = pd.read_csv('files/results.csv')

# calculate number of seasons 
results_races = results.merge(races[['raceId', 'year']], on='raceId',how='left')
career_span = (results_races.groupby('driverId')['year'].nunique().reset_index(name='num_seasons'))

# add names
career_span = career_span.merge(drivers[['driverId', 'forename', 'surname']], on='driverId', how='left')
career_span['driver_name'] = career_span['forename'] + ' ' + career_span['surname']

# csv
career_span_final = career_span[['driver_name', 'num_seasons']]
career_span_final = career_span_final.sort_values(by='num_seasons', ascending=False).head(11)

career_span_final.to_csv('career.csv', index=False)