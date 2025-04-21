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


# Load data for the 2024 season
# Note: Ensure the data files are in the same directory as this script
loadData()
df_2024 = season_data[2024]


# App setup
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)


# App layout
# Create a scatter plot of Points vs True Shooting Percentage
# with a range slider for games played
# and a toggle for player names
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

    
    html.Label('Show player names on chart:'),
    dcc.Checklist(
        id='label-toggle',
        options=[{'label': 'Show Labels', 'value': 'show'}],
        value=[],
        style={'marginBottom': '20px'}
    ),
    
    dcc.Graph(id="scatter-plot")
])


# Callback to update the scatter plot based on the selected range of games played
# and whether to show player names
# Links the slider/ toggle and the scatter plot
@callback(
    Output('scatter-plot', 'figure'),
    Output('output-container-range-slider', 'children'),
    Input('games-slider', 'value'),
    Input('label-toggle', 'value')
)

def update_chart(games_range, label_toggle):
    low, high = games_range
    mask = (df_2024['G'] >= low) & (df_2024['G'] <= high)
    filtered_df = df_2024[mask]

    show_labels = "show" in label_toggle
    text_vals = filtered_df['Player'] if show_labels else None

    fig = px.scatter(
        filtered_df,
        x="PTS",
        y="TS%",
        text=text_vals,
        hover_name="Player",
        hover_data=["G"],
        trendline="ols",
        title='Points vs True Shooting % (Filtered by Games Played)'
    )

    if show_labels:
        fig.update_traces(textposition='top center')

    fig.update_layout(xaxis_title='Points', yaxis_title='True Shooting Percentage')

    return fig, f'You have selected games played between **{low} and {high}** — {len(filtered_df)} players match.'

if __name__ == '__main__':
    app.run(debug=True)
