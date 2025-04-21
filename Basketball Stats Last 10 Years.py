from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

# Load NBA Data
season_data = {}
def loadData():
    for year in range(2015, 2025):
        filename = f'NBA Reg Season {year}.txt'
        df = pd.read_csv(filename)

        if 'Player-additional' in df.columns:
            df = df.drop(columns=['Player-additional'])

        if 'PTS' in df.columns and 'FGA' in df.columns and 'FTA' in df.columns:
            df['TS%'] = df['PTS'] / (2 * (df['FGA'] + 0.44 * df['FTA']))

        season_data[year] = df

loadData()
df_2024 = season_data[2024]


# App setup
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H4('NBA 2024-2025: Points vs True Shooting Percentage'),
    
    dcc.RangeSlider(
        id='games-slider',
        min=int(df_2024['G'].min()),
        max=int(df_2024['G'].max()),
        step=1,
        value=[58, int(df_2024['G'].max())],
        marks={
            int(df_2024['G'].min()): str(int(df_2024['G'].min())),
            int(df_2024['G'].max()): str(int(df_2024['G'].max()))
        }
    ),
    
    html.Div(id='output-container-range-slider', style={'marginTop': 10, 'fontWeight': 'bold'}),
    
    dcc.Graph(id="scatter-plot")
])

@callback(
    Output('scatter-plot', 'figure'),
    Output('output-container-range-slider', 'children'),
    Input('games-slider', 'value'))
def update_output(games_range):
    low, high = games_range
    mask = (df_2024['G'] >= low) & (df_2024['G'] <= high)
    filtered_df = df_2024[mask]

    fig = px.scatter(
        filtered_df,
        x="PTS",
        y="TS%",
        hover_name="Player",
        trendline="ols",
        title='Points vs True Shooting % (Filtered by Games Played)'
    )
    fig.update_layout(xaxis_title='Points', yaxis_title='True Shooting Percentage')

    return fig, f'You have selected games played between **{low} and {high}** — {len(filtered_df)} players match.'

if __name__ == '__main__':
    app.run(debug=True)
