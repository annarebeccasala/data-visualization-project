import pandas as pd

# loading datasets
drivers = pd.read_csv('files/drivers.csv')
constructors = pd.read_csv('files/constructors.csv')
driver_standings = pd.read_csv('files/driver_standings.csv')
constructor_standings = pd.read_csv('files/constructor_standings.csv')
races = pd.read_csv('files/races.csv')
races = races[races['year'] >= 2010]
results = pd.read_csv('files/results.csv')

# calculate final driver positions
driver_standings_races = driver_standings.merge(races[['raceId','year','round']], on='raceId', how='inner')
final_rounds_driver = driver_standings_races.groupby('year')['round'].max().reset_index()
final_driver_standings = driver_standings_races.merge(final_rounds_driver, on=['year','round'], how='inner')

final_driver_standings = final_driver_standings[['year','driverId','position','points']]
final_driver_standings = final_driver_standings.merge(drivers[['driverId','forename','surname']], on='driverId', how='left')
final_driver_standings['driver_name'] = final_driver_standings['forename'] + ' ' + final_driver_standings['surname']
final_driver_standings = final_driver_standings.rename(columns={'position':'driver_position', 'points':'driver_points'})

# calculate final constructor positions
constructor_standings_races = constructor_standings.merge(races[['raceId','year','round']], on='raceId', how='inner')
final_rounds_constructor = constructor_standings_races.groupby('year')['round'].max().reset_index()
final_constructor_standings = constructor_standings_races.merge(final_rounds_constructor, on=['year','round'], how='inner')

final_constructor_standings = final_constructor_standings[['year','constructorId','position']]
final_constructor_standings = final_constructor_standings.merge(constructors[['constructorId','name']], on='constructorId', how='left')
final_constructor_standings = final_constructor_standings.rename(columns={'position':'constructor_position','name':'constructor_name'})

# associate each driver with their constructor
results_races = results.merge(races[['raceId','year']], on='raceId', how='inner')
last_race_per_driver = results_races.groupby(['year','driverId'])['raceId'].max().reset_index()
last_driver_team = last_race_per_driver.merge(results_races[['raceId','driverId','constructorId']], 
                                              on=['raceId','driverId'], how='left')
last_driver_team = last_driver_team.merge(constructors[['constructorId','name']], on='constructorId', how='left')
last_driver_team = last_driver_team.rename(columns={'name':'constructor_name'})

# merge driver and constructor final positions
viz_df = final_driver_standings.merge(last_driver_team[['year','driverId','constructorId','constructor_name']], 
                                     on=['year','driverId'], how='left')

viz_df = viz_df.merge(final_constructor_standings[['year','constructorId','constructor_position']], 
                      on=['year','constructorId'], how='left')

# csv
viz_df_final = viz_df[['year','driver_name','constructor_name','driver_position','constructor_position']]

bubble_df = (
    viz_df_final.groupby(['driver_position','constructor_position'])
    .size()
    .reset_index(name='count')
)

bubble_df.to_csv('driver_vs_constructor.csv', index=False)