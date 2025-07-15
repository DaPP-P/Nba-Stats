from dash import dcc, html
import plotly.express as px

def get_layout(df, season_averages):
    return html.Div([
        html.H4('NBA Shooting Percentages by Year (2015 to 2025)'),
        dcc.Graph(id="scatter-plot", figure=create_figure(df, season_averages))
    ])


def create_figure(df, season_averages):
    fig = px.scatter(
        season_averages,
        y="Average FT%",
        x = "Season",
        title='League shotting percentages by year',
    )

    fig.add_traces(
        px.line(
            season_averages,
            x=season_averages['Season'].astype(str),
            y= ['Average FT%', 'Average 2PT%', "Average 3PT%", "Average eFG%", "Average TS%"],
            markers=True,
        ).data
    )

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Free Throw Percentage',
        xaxis_type='category'
    )

    return fig
