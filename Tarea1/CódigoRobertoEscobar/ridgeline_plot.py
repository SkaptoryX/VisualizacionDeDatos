import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats

# Cargar el archivo CSV
df = pd.read_csv('data.csv')

# Limpiar el DataFrame: quitar filas sin vueltas o año
df_clean = df.dropna(subset=['Laps', 'Year', 'Drivers'])

# Crear columna de década
df_clean['Decade'] = ((df_clean['Year'] // 4) * 4)

# Preparamos los datos para el gráfico de ridgeline
ridgeline_data = []
decades = sorted(df_clean['Decade'].unique())

print("Generando Ridgeline Plot (Gráfico de Perfil de Montañas)...")

# Preparar los datos para cada década
for i, decade in enumerate(decades):
    decade_df = df_clean[df_clean['Decade'] == decade]
    # Usamos KDE (Kernel Density Estimation)
    if len(decade_df) > 5:  # Verificamos que haya suficientes datos
        x = np.linspace(100, 400, 1000)  # Rango de vueltas
        kde = stats.gaussian_kde(decade_df['Laps'])
        y = kde(x)
        # Normalizamos
        y = y / y.max()
        # Desplazamos verticalmente para crear efecto de montaña
        y = y + i
        # Eliminamos la mediana del objeto de datos
        ridgeline_data.append((x, y, decade))

# Crear el gráfico de ridgeline con márgenes ajustados
fig = plt.figure(figsize=(14, 10))
ax = plt.axes([0.1, 0.15, 0.8, 0.75])  # Ajustado el espacio vertical del gráfico

for i, (x, y, decade) in enumerate(ridgeline_data):
    color = plt.cm.viridis(i / len(ridgeline_data))
    ax.fill_between(x, i, y, alpha=0.8, color=color)
    ax.plot(x, y, color='black', linewidth=1.0)
    
    # Añadimos etiqueta de década
    ax.text(100, i + 0.2, f"{decade}s", fontsize=12, ha='left', va='center')

# Configurar el gráfico
ax.set_yticks([])
ax.set_xlabel('Número de vueltas', fontsize=14)
ax.set_title('Evolución histórica de las vueltas completadas en las 24 Horas de Le Mans', 
             fontsize=18, 
             loc='left',
             weight='bold',
             pad=20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# Añadir barra de color en la parte superior con más espacio
sm = plt.cm.ScalarMappable(cmap="viridis", norm=plt.Normalize(vmin=min(decades), vmax=max(decades)))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', pad=0.12, location='top')
cbar.set_label('Década', fontsize=12)

# Añadir explicación debajo del diagrama
plt.figtext(0.5, 0.02, 
            "Cada curva representa la distribución de vueltas completadas en promedio cada 4 años.\n" + 
            "Las áreas más altas indican una mayor densidad de datos en ese rango de vueltas.",
            ha='center', fontsize=12, 
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8))

plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.2)  # Ajustado el espacio superior e inferior
plt.show()