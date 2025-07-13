from dash import Dash
import os
import pandas as pd
from data_loader import load_season_data, get_seasonal_averages
from graphs import points_vs_ts, ft_percentage_by_year  

# Season data loading
season_data = load_season_data()
season_averages = get_seasonal_averages(season_data)

print(season_averages)

df_all_years = pd.concat(
    [season_data[year].assign(Season=year) for year in range(2015, 2025)],
    ignore_index=True
)


df_2024 = season_data[2024]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = ft_percentage_by_year.get_layout(df_all_years)
ft_percentage_by_year.register_callbacks(app, df_all_years)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))
