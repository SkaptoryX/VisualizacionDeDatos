import pandas as pd
import bar_chart_race as bcr

# Cargar datasets
results = pd.read_csv('results.csv')
races = pd.read_csv('races.csv')
constructors = pd.read_csv('constructors.csv')

results = results.merge(races[['raceId', 'year']], on='raceId', how='left')
winners = results[results['positionOrder'] == 1]

# Contar victorias por escudería y año
victorias = winners.groupby(['year', 'constructorId']).size().unstack(fill_value=0)
victorias = victorias.sort_index()

# Obtener nombres de escuderías
constructor_names = constructors.set_index('constructorId')['name']
victorias.columns = [constructor_names.get(cid, f'ID {cid}') for cid in victorias.columns]
victorias_acumuladas = victorias.cumsum()
victorias_acumuladas.index = victorias_acumuladas.index.astype(str)

# Filtrar hasta el año 2020
victorias_acumuladas = victorias_acumuladas[victorias_acumuladas.index.astype(int) <= 2020]

# Crear el bar chart race
bcr.bar_chart_race(
    df=victorias_acumuladas,
    filename='f1_victorias_acumuladas.gif',
    orientation='h',
    sort='desc',
    n_bars=10,
    fixed_order=False,
    fixed_max=True,
    steps_per_period=20,
    period_length=800,
    interpolate_period=False,
    period_fmt=None,
    title='Victorias acumuladas por escudería en Fórmula 1 (1950 - 2020)',
    bar_size=.95,
    period_label={
        'x': .99,
        'y': .25,
        'ha': 'right',
        'va': 'center',
        'size': 30,
        'color': 'black'
    }
)

