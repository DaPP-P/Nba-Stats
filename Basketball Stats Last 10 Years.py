import pandas as pd
import plotly.express as px

season_data = {}

for year in range(2015, 2025):
    filename = f'NBA Reg Season {year}.txt'
    df = pd.read_csv(filename)
    
    # Remove 'Player-additional' column if it exists
    if 'Player-additional' in df.columns:
        df = df.drop(columns=['Player-additional'])
    
    season_data[year] = df

# Test: show the columns of one season
print(season_data[2024].head)
all_seasons = pd.concat(season_data.values(), ignore_index=True)


avg_points_by_age = all_seasons.groupby('Age')['PTS'].mean().reset_index()

fig = px.line(
    avg_points_by_age,
    x='Age',
    y='PTS',
    markers=True,
    title='Average Points by Age',
    labels={'PTS': 'Average Points', 'Age': 'Player Age'}
)
fig.show()
