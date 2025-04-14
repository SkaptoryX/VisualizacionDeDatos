import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib.cm as cm

# Leer los datos
df = pd.read_csv('LeMansRaces.csv')

# Configurar el diseño de la figura con dos subgráficos
fig = plt.figure(figsize=(20, 10))
fig.suptitle('Análisis de Victorias en Le Mans', fontsize=16, y=0.98)

# Gráfico 1: Top 10 Equipos con Más Victorias
ax1 = fig.add_subplot(121, projection='polar')

# Contar victorias por equipo
team_wins = df.groupby('Team').size().reset_index(name='wins')
team_wins = team_wins.sort_values('wins', ascending=False).head(10)

# Calcular los ángulos para las barras
theta1 = np.linspace(0, 2*np.pi, len(team_wins), endpoint=False)

# Crear las barras para equipos
bars1 = ax1.bar(theta1, team_wins['wins'], 
              width=2*np.pi/len(team_wins),
              alpha=0.7,
              color=plt.cm.viridis(np.linspace(0, 1, len(team_wins))))

# Personalizar el gráfico
ax1.set_xticks(theta1)
ax1.set_xticklabels(team_wins['Team'], fontsize=8, rotation=45)
ax1.set_title('Top 10 Equipos con Más Victorias', pad=20)

# Ajustar etiquetas de valores
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, height,
            f'{int(height)}',
            ha='center', va='bottom')

# Gráfico 2: Victorias por Nacionalidad de Pilotos
ax2 = fig.add_subplot(122, projection='polar')

# Contar victorias por nacionalidad de piloto
driver_nationality_wins = df.groupby('Driver_nationality').size().reset_index(name='wins')
driver_nationality_wins = driver_nationality_wins.sort_values('wins', ascending=False).head(15)

# Calcular los ángulos para las barras
theta2 = np.linspace(0, 2*np.pi, len(driver_nationality_wins), endpoint=False)

# Crear mapa de colores para las nacionalidades
# Usando colormaps directamente sin get_cmap
cmap = plt.cm.tab20
color_values = np.linspace(0, 1, len(driver_nationality_wins))
color_list = [cmap(i) for i in color_values]

# Crear las barras para nacionalidades
bars2 = ax2.bar(theta2, driver_nationality_wins['wins'], 
              width=2*np.pi/len(driver_nationality_wins),
              alpha=0.8,
              color=color_list)

# Personalizar el gráfico
ax2.set_xticks(theta2)
ax2.set_xticklabels(driver_nationality_wins['Driver_nationality'], fontsize=9, rotation=45)
ax2.set_title('Top 15 Nacionalidades de Pilotos con Más Victorias', pad=20)

# Crear etiquetas y leyenda
country_names = driver_nationality_wins['Driver_nationality'].tolist()
legend_elements = [Patch(facecolor=color_list[i], label=f"{country_names[i]}: {driver_nationality_wins['wins'].iloc[i]} victorias") 
                  for i in range(len(country_names))]

# Colocar leyenda fuera del gráfico polar
ax2.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1.1, 0.5), fontsize=8)

# Añadir anotación explicativa
plt.figtext(0.5, 0.01, 
           'El gráfico muestra las nacionalidades de los pilotos con más victorias en Le Mans.\n'
           'La longitud de cada barra representa el número de victorias y cada color representa una nacionalidad diferente.',
           ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

# Ajustar etiquetas de valores
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, height,
            f'{int(height)}',
            ha='center', va='bottom')

plt.tight_layout()
plt.subplots_adjust(wspace=0.4, top=0.9, bottom=0.15)  # Ajustar espaciado

plt.show()