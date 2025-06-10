import pandas as pd
import plotly.express as px
import numpy as np

df = pd.read_csv('basketplayers.csv')

df = df.dropna(subset=['country'])

df = df[~df['name'].str.contains('[1234567890]', regex=True)]

country_counts = df['country'].value_counts().reset_index()
country_counts.columns = ['country', 'count']

country_counts['log_count'] = np.log10(country_counts['count'])

fig = px.choropleth(
    country_counts, 
    locations='country',
    color='log_count',
    hover_name='country',
    hover_data=['count'],
    color_continuous_scale=px.colors.sequential.Plasma,
    title='Cantidad de Jugadores de Baloncesto por País, escala logarítmica',
    labels={'log_count': 'Log 10 de cantidad de jugadores', 'count': 'Cantidad'}
)

fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth',
    ),
    width=1000,
    height=600,
)

fig.write_image("basketball_players_map.png")