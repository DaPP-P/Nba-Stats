from dash import dcc, html, Input, Output
import plotly.express as px

def get_layout(df):
    return html.Div([
        html.H4('NBA free throw percentage by year 2015 to 2025'),
        
        #Filter for games played
        dcc.RangeSlider(
            id='games-slider',
            min=int(df['G'].min()),
            max=int(df['G'].max()),
            step=1,
            value=[58, int(df['G'].max())],
            marks={
                int(df['G'].min()): str(int(df['G'].min())),
                int(df['G'].max()): str(int(df['G'].max()))
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

def register_callbacks(app, df):
    @app.callback(
        Output('scatter-plot', 'figure'),
        Output('output-container-range-slider', 'children'),
        Input('games-slider', 'value'),
        Input('label-toggle', 'value')
    )
    def update_chart(games_range, label_toggle):
        low, high = games_range
        mask = (df['G'] >= low) & (df['G'] <= high)
        filtered_df = df[mask]
        show_labels = "show" in label_toggle
        text_vals = filtered_df['Player'] if show_labels else None

        fig = px.scatter(
            filtered_df,
            x=filtered_df['Season'].astype(str),
            y="FT%",
            text=text_vals,
            hover_name="Player",
            hover_data=["FTM", "G"], 
            title='Free Throw Percentage by Year (Filtered by Games Played)',
        )

        if show_labels:
            fig.update_traces(textposition='top center')

        fig.update_layout(
            xaxis_title='Year', 
            yaxis_title='Free Throw Percentage',
            xassis_type='category'
        )
        return fig, f'You have selected games played between **{low} and {high}** — {len(filtered_df)} players match.'
