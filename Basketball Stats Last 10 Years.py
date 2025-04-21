import pandas as pd
import plotly.express as px
import numpy as np


season_data = {}

# Load the data for each season from 2015 to 2024
# Under season_data, the data for each season is stored in a dictionary
# with the year as the key and the DataFrame as the value
def loadData():
    # Load the data for each season from 2015 to 2024
    for year in range(2015, 2025):
        filename = f'NBA Reg Season {year}.txt'
        df = pd.read_csv(filename)
        
        # Remove 'Player-additional' column if it exists
        if 'Player-additional' in df.columns:
            df = df.drop(columns=['Player-additional'])
        
        # Keep only players with more than 58 games played
        if 'G' in df.columns:
            df = df[df['G'] > 58]

        season_data[year] = df


# Main
loadData()
print(season_data[2024].head())  # Now this will show column names and values

# Sort by points
sorted_df = season_data[2024].sort_values(by='PTS', ascending=True)

# Plot Points Per Game in the 2024-2025 season
fig = px.scatter(
    sorted_df,
    y='PTS',
    x='Player',
    title='Points Per Game in the 2024-2025 Season (Sorted)'
)

fig.update_layout(xaxis_title='Player', yaxis_title='Points Per Game')
fig.show()