import pandas as pd
import plotly.express as px

# Cargar los CSVs
drivers = pd.read_csv("drivers.csv")
results = pd.read_csv("results.csv")

# Filtrar solo los drivers que aparecen en el archivo de resultados
pilotos_con_resultados = results['driverId'].unique()
drivers_filtrados = drivers[drivers['driverId'].isin(pilotos_con_resultados)]

# Contar cuántos pilotos han participado por nacionalidad
conteo_nacionalidades = drivers_filtrados['nationality'].value_counts().reset_index()
conteo_nacionalidades.columns = ['nationality', 'count']

# Diccionario de mapeo: nacionalidad → nombre de país estándar
nacionalidad_a_pais = {
    'British': 'United Kingdom',
    'American': 'United States',
    'Italian': 'Italy',
    'French': 'France',
    'German': 'Germany',
    'Brazilian': 'Brazil',
    'Argentine': 'Argentina',
    'Argentinian': 'Argentina',
    'Belgian': 'Belgium',
    'Swiss': 'Switzerland',
    'South African': 'South Africa',
    'Japanese': 'Japan',
    'Australian': 'Australia',
    'Dutch': 'Netherlands',
    'Austrian': 'Austria',
    'Spanish': 'Spain',
    'Canadian': 'Canada',
    'Swedish': 'Sweden',
    'New Zealander': 'New Zealand',
    'Finnish': 'Finland',
    'Mexican': 'Mexico',
    'Danish': 'Denmark',
    'Irish': 'Ireland',
    'Uruguayan': 'Uruguay',
    'Portuguese': 'Portugal',
    'Russian': 'Russia',
    'Venezuelan': 'Venezuela',
    'Colombian': 'Colombia',
    'East German': 'Germany',
    'Thai': 'Thailand',
    'Indian': 'India',
    'Polish': 'Poland',
    'Hungarian': 'Hungary',
    'Malaysian': 'Malaysia',
    'Czech': 'Czech Republic',
    'Chilean': 'Chile',
    'Liechtensteiner': 'Liechtenstein',
    'Indonesian': 'Indonesia',
    'Chinese': 'China',
    'Monegasque': 'Monaco',
    'Rhodesian': 'Zimbabwe',
    'American-Italian': 'United States',
    'Argentine-Italian': 'Argentina',
}

# Aplicar el mapeo
conteo_nacionalidades['country'] = conteo_nacionalidades['nationality'].map(nacionalidad_a_pais)
conteo_nacionalidades = conteo_nacionalidades.dropna(subset=['country'])

# Agrupar por país en caso de duplicados
conteo_final = conteo_nacionalidades.groupby('country', as_index=False)['count'].sum()

# Crear el mapa mejorado
fig = px.choropleth(
    conteo_final,
    locations='country',
    locationmode='country names',
    color='count',
    color_continuous_scale='OrRd',
    labels={'country': 'País', 'count': 'Pilotos'},
    title='Cantidad de pilotos de F1 por país'
)

# Estética y personalización
fig.update_layout(
    title={
        'text': 'Cantidad de pilotos de F1 por país',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 22}
    },
    coloraxis_colorbar=dict(title='Cantidad de pilotos'),
    geo=dict(
        showocean=False,
        showlakes=False,
        bgcolor='white',
        showframe=False,
        showcountries=True
    )
)

fig.update_traces(
    hovertemplate="<b>%{location}</b><br>Pilotos: %{z}<extra></extra>"
)

fig.show()