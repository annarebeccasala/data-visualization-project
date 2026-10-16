import pandas as pd

# loading datasets
drivers = pd.read_csv('files/drivers.csv')
races = pd.read_csv('files/races.csv')
races = races[races['year'] >= 2010]
results = pd.read_csv('files/results.csv')
sprint_results = pd.read_csv('files/sprint_results.csv')
driver_standings = pd.read_csv('files/driver_standings.csv')

# prepare df
def prepare_results(df):
    df = df.merge(races[['raceId', 'year']], on='raceId', how='inner')
    df = df.merge(drivers[['driverId', 'forename', 'surname']], on='driverId', how='left')
    df['driver_name'] = df['forename'] + ' ' + df['surname']
    df['position_numeric'] = pd.to_numeric(df['position'], errors='coerce')
    df['points'] = pd.to_numeric(df['points'], errors='coerce').fillna(0)
    return df

results_races = prepare_results(results)
sprint_results_races = prepare_results(sprint_results)

# combine races and sprint
all_results = pd.concat([results_races, sprint_results_races], ignore_index=True)

# compute win-rate and points-rate
season_stats = (
    all_results.groupby(['year', 'driverId', 'driver_name'], as_index=False).agg(
        races=('raceId', 'count'),
        wins=('position_numeric', lambda x: (x == 1).sum()),
        points=('points', 'sum')
    )
)

season_stats['win_rate'] = season_stats['wins'] / season_stats['races']

# calculate max possible points per season
normal_max_per_race = results_races.groupby('year')['points'].max().reset_index()
normal_max_per_race.rename(columns={'points':'max_points_normal'}, inplace=True)
num_normal_races = results_races.groupby('year')['raceId'].nunique().reset_index()
num_normal_races.rename(columns={'raceId':'num_normal_races'}, inplace=True)

sprint_max_per_race = sprint_results_races.groupby('year')['points'].max().reset_index()
sprint_max_per_race.rename(columns={'points':'max_points_sprint'}, inplace=True)
num_sprint_races = sprint_results_races.groupby('year')['raceId'].nunique().reset_index()
num_sprint_races.rename(columns={'raceId':'num_sprint_races'}, inplace=True)

season_max = normal_max_per_race.merge(num_normal_races, on='year')
season_max = season_max.merge(sprint_max_per_race, on='year', how='left')
season_max = season_max.merge(num_sprint_races, on='year', how='left')

season_max[['max_points_sprint','num_sprint_races']] = season_max[['max_points_sprint','num_sprint_races']].fillna(0)

season_max['max_possible_points'] = (season_max['max_points_normal'] * season_max['num_normal_races'] +
                                    season_max['max_points_sprint'] * season_max['num_sprint_races'])

season_stats = season_stats.merge(season_max[['year','max_possible_points']], on='year')
season_stats['points_rate'] = season_stats['points'] / season_stats['max_possible_points']

# identify champions
standings_races = driver_standings.merge(races[['raceId','year','round']], on='raceId', how='inner')
final_rounds = standings_races.groupby('year')['round'].max().reset_index()
final_standings = standings_races.merge(final_rounds, on=['year','round'], how='inner')

champions = final_standings[final_standings['position'] == 1][['year','driverId']]
champions['champion_status'] = 'Champion'

# add champion status
viz_df = season_stats.merge(champions, on=['year','driverId'], how='left')
viz_df['champion_status'] = viz_df['champion_status'].fillna('Non-Champion')

# csv
viz_df_final = viz_df[['year','driver_name','wins','races','win_rate','points','points_rate','champion_status']].copy()

viz_df_final['season_driver'] = (
    viz_df_final['year'].astype(str) + ' - ' + viz_df_final['driver_name']
)

viz_df_final = viz_df_final[['season_driver', 'wins', 'races', 'win_rate', 'points', 'points_rate', 'champion_status']]

viz_df_final.to_csv('winrate_vs_pointsrate.csv', index=False)