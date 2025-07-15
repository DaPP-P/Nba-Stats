import pandas as pd

def load_season_data(start_year=2015, end_year=2025):
    season_data = {}
    for year in range(start_year, end_year):
        filename = f'data/NBA Reg Season {year}.txt'
        df = pd.read_csv(filename)

        if 'Player-additional' in df.columns:
            df = df.drop(columns=['Player-additional'])

        if 'PTS' in df.columns and 'FGA' in df.columns and 'FTA' in df.columns:
            df['TS%'] = df['PTS'] / (2 * (df['FGA'] + 0.44 * df['FTA']))

        if 'FT' in df.columns and "G" in df.columns:
            df['FTM'] = round(df['FT'] * df['G'])

        df['Season'] = year

        season_data[year] = df
    return season_data

def get_seasonal_averages(season_data):
    rows = []
    for year, df in season_data.items():
        row = {'Season': year}

        if 'FT%' in df.columns:
            row['Average FT%'] = df['FT'].sum() / df["FTA"].sum()

        if "3P%" in df.columns:
            row['Average 3PT%'] = df['3P'].sum() / df["3PA"].sum()

        if "2P%" in df.columns:
            row['Average 2PT%'] = df['2P'].sum() / df["2PA"].sum()

        # Average eFG% calculation
        if 'FG' in df.columns and '3P' in df.columns and 'FGA' in df.columns:
            total_fgm = df['FG'].sum()
            total_3pm = df['3P'].sum()
            total_fga = df['FGA'].sum()
            row["Average eFG%"] = (total_fgm + 0.5 * total_3pm) / total_fga

        # Average TS% calculation
        if 'PTS' in df.columns and 'FGA' in df.columns and 'FTA' in df.columns:
            total_pts = df['PTS'].sum()
            total_fga = df['FGA'].sum()
            total_fta = df['FTA'].sum()
            row["Average TS%"] = total_pts / (2 * (total_fga + 0.44 * total_fta))

        if "3PA" in df.columns:
            row['Average 3PA'] = df['3PA'].sum()

        if "2PA" in df.columns:
            row['Average 2PA'] = df['2PA'].sum()

        if 'FTA' in df.columns:
            row['Average FTA'] = df['FTA'].sum()

        if "3PA" in df.columns and "2PA" in df.columns and "FTA" in df.columns:
            row["Total Shots"] = row['Average 3PA'] + row['Average 2PA'] + row['Average FTA']

        row["3PA Rate"] = row['Average 3PA'] / row["Total Shots"]
        row["2PA Rate"] = row['Average 2PA'] / row["Total Shots"]
        row["FTA Rate"] = row['Average FTA'] / row["Total Shots"]


        rows.append(row)

    return pd.DataFrame(rows)
