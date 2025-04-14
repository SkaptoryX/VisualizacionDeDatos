import pandas as pd
import numpy as np
import plotly.express as px


df = pd.read_csv("FILTERED_ROWS.csv")

# filtrar DNF
df_clean = df[df['position'] > 0]
df_clean = df_clean[df_clean['category'].isin(['MotoGP', 'Moto2', 'Moto3'])]

# puntos promedios por piloto
driver_avg = df_clean.groupby(['country', 'category', 'rider_name'])['points'].mean().reset_index()

# raiz quinta +1 para visualizar bien tamaños
driver_avg['points_viz'] = np.power(driver_avg['points'] + 1, 0.2)

# capa superior total
driver_avg['overall'] = 'MotoGP Racing'

# limita color para evitar outliers quitando variedad al gradiente
color_max = np.percentile(driver_avg['points'], 95)
color_min = 0

fig = px.sunburst(
    driver_avg,
    path=['overall', 'category', 'country', 'rider_name'], 
    values='points_viz',  # tamaño (raiz quinta)
    color='points',       # color (promedio de puntos)
    color_continuous_scale='thermal',
    range_color=[color_min, color_max],
    title='Puntos promedios por piloto en MotoGP, agregados por país y categoría',
    hover_data=['points'], 
    maxdepth=2,      
    branchvalues="total"
)

fig.update_traces(marker_line_width=0) 
fig.update_layout(
    height=900,
    width=900,
    font=dict(size=12),
    coloraxis_colorbar=dict(
        title="Puntos promedio",
        thicknessmode="pixels", 
        thickness=15,
        len=0.75
    )
)

fig.show()