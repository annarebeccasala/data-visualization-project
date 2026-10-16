import pandas as pd

MIN_STARTS = 10

# loading datasets
results = pd.read_csv("files/results.csv")
qualifying = pd.read_csv("files/qualifying.csv")
drivers = pd.read_csv("files/drivers.csv")
constructor_standings = pd.read_csv("files/constructor_standings.csv")
constructors = pd.read_csv("files/constructors.csv")
status = pd.read_csv("files/status.csv")
races = pd.read_csv("files/races.csv")

drivers["driver_name"] = drivers["forename"] + " " + drivers["surname"]

# starts per driver
starts = (results.groupby("driverId").size().reset_index(name="starts"))

eligible_drivers = starts[starts["starts"] >= MIN_STARTS]

# pole positions
poles = (qualifying[qualifying["position"] == 1].groupby("driverId").size().reset_index(name="poles"))

pole_stats = (poles.merge(starts, on="driverId").merge(drivers[["driverId", "driver_name"]], on="driverId"))

pole_stats["pole_rate"] = pole_stats["poles"] / pole_stats["starts"]

print("Most pole positions (absolute):")
print(pole_stats.sort_values("poles", ascending=False).head(1))

print("\nHighest pole position rate (min. 50 starts):")
print(pole_stats[pole_stats["starts"] >= MIN_STARTS].sort_values("pole_rate", ascending=False).head(1))

# wins
wins = (results[results["positionOrder"] == 1].groupby("driverId").size().reset_index(name="wins"))

win_stats = (wins.merge(starts, on="driverId").merge(drivers[["driverId", "driver_name"]], on="driverId"))

win_stats["win_rate"] = win_stats["wins"] / win_stats["starts"]

print("\nMost race wins (absolute):")
print(win_stats.sort_values("wins", ascending=False).head(1))

print("\nHighest win rate (min. 50 starts):")
print(win_stats[win_stats["starts"] >= MIN_STARTS].sort_values("win_rate", ascending=False).head(1))

# podiums
podiums = (results[results["positionOrder"].isin([1, 2, 3])].groupby("driverId").size().reset_index(name="podiums"))

podium_stats = (podiums.merge(starts, on="driverId").merge(drivers[["driverId", "driver_name"]], on="driverId"))

podium_stats["podium_rate"] = podium_stats["podiums"] / podium_stats["starts"]

print("\nMost podium finishes (absolute):")
print(podium_stats.sort_values("podiums", ascending=False).head(1))

print("\nHighest podium rate (min. 50 starts):")
print(podium_stats[podium_stats["starts"] >= MIN_STARTS].sort_values("podium_rate", ascending=False).head(1))

# dnfs
results_status = results.merge(status, on="statusId")
dnf_results = results_status[~results_status["status"].str.contains("Finished", case=False)]

dnfs = (dnf_results.groupby("driverId").size().reset_index(name="dnfs"))

dnf_stats = (dnfs.merge(starts, on="driverId").merge(drivers[["driverId", "driver_name"]], on="driverId"))

dnf_stats["dnf_rate"] = dnf_stats["dnfs"] / dnf_stats["starts"]

eligible_dnf = dnf_stats[dnf_stats["starts"] >= MIN_STARTS]

print("\nMost DNFs (absolute):")
print(eligible_dnf.sort_values("dnfs", ascending=False).head(1))

#print("\nLeast DNFs (absolute):")
#print(eligible_dnf.sort_values("dnfs").head(1))

print("\nHighest DNF rate (min. 50 starts):")
print(eligible_dnf.sort_values("dnf_rate", ascending=False).head(1))

print("\nLowest DNF rate (min. 50 starts):")
print(eligible_dnf.sort_values("dnf_rate").head(1))


# constructors
last_races = (races.sort_values(["year", "round"]).groupby("year").tail(1)[["year", "raceId"]])

final_constructor_standings = (constructor_standings.merge(last_races, on="raceId"))

constructor_titles = (final_constructor_standings[final_constructor_standings["position"] == 1].groupby("constructorId").size().reset_index(name="titles").merge(constructors[["constructorId", "name"]], on="constructorId").sort_values("titles", ascending=False))

print("\nConstructor with most world titles (final standings):")
print(constructor_titles.head(5))
