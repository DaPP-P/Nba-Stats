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
        if 'FT%' in df.columns:
            avg_ft = df['FT%'].mean()
            rows.append({'Season': year, 'Average FT%': avg_ft})
    return pd.DataFrame(rows)
