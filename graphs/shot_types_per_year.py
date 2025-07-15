from dash import dcc, html
import plotly.express as px

def get_layout(df, season_averages):
    return html.Div([
        html.H4('NBA Shooting Zones pes by Year (2015 to 2025)'),
        dcc.Graph(id="scatter-plot", figure=create_figure(df, season_averages))
    ])


def create_figure(df, season_averages):

    # Melting data for shot type rates
    long_df = season_averages.melt(
        id_vars='Season',
        value_vars=['3PA Rate', '2PA Rate', 'FTA Rate'],
        var_name='Shot Type',
        value_name='Proportion'
    )

    fig = px.line(
        long_df,
        x='Season',
        y='Proportion',
        color='Shot Type',
        markers=True,
        title='Shot Type Rates by Season'
    )

    fig.update_layout(
        xaxis_title='Season',
        yaxis_title='Proportion of Total Shots',
        yaxis_tickformat='.1%',
        xaxis_type='category'
    )

    return fig
