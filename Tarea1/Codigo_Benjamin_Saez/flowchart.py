import pandas as pd
import plotly.graph_objects as go
from plotly.colors import qualitative

df = pd.read_csv("FILTERED_ROWS.csv")

# solo motogp, rango de fechas
recent_years = list(range(2018, 2025)) 
motogp_df = df[(df['category'] == 'MotoGP') & (df['year'].isin(recent_years))]

# top 15
top_riders = motogp_df.groupby('rider_name')['points'].sum().nlargest(15).index.tolist()
rider_df = motogp_df[motogp_df['rider_name'].isin(top_riders)]

# manufacturador
rider_df['manufacturer'] = rider_df['bike_name'].str.split().str[0]

# agregar puntos
flow_data = rider_df.groupby(['rider_name', 'team_name', 'manufacturer'])['points'].sum().reset_index()

# filtrar flujos muy pequeños que "ensucian" el diagrama
flow_data = flow_data[flow_data['points'] > 20]

# indices
riders = flow_data['rider_name'].unique()
teams = flow_data['team_name'].unique()
manufacturers = flow_data['manufacturer'].unique()

rider_indices = {rider: i for i, rider in enumerate(riders)}
offset = len(rider_indices)
team_indices = {team: i + offset for i, team in enumerate(teams)}
offset += len(team_indices)
manufacturer_indices = {mfr: i + offset for i, mfr in enumerate(manufacturers)}

colors = qualitative.Set3
# un color por piloto
rider_colors = {rider: colors[i % len(colors)] for i, rider in enumerate(riders)}


# diagrama sankey con filtro por piloto
def get_sankey_data(selected_riders=None):
    if selected_riders is None:
        selected_riders = riders
    elif isinstance(selected_riders, str):
        selected_riders = [selected_riders]
    
    filtered_data = flow_data[flow_data['rider_name'].isin(selected_riders)]
    
    source = []
    target = []
    values = []
    link_labels = []
    link_colors = []
    
    # conexiones
    for _, row in filtered_data.iterrows():

        source.append(rider_indices[row['rider_name']])
        target.append(team_indices[row['team_name']])
        values.append(row['points'])
        link_labels.append(f"{row['rider_name']} → {row['team_name']}")
        link_colors.append(rider_colors[row['rider_name']])
        
        source.append(team_indices[row['team_name']])
        target.append(manufacturer_indices[row['manufacturer']])
        values.append(row['points'])
        link_labels.append(f"{row['team_name']} → {row['manufacturer']} (Rider: {row['rider_name']})")
        link_colors.append(rider_colors[row['rider_name']])
    
    return {
        'source': source,
        'target': target,
        'value': values,
        'color': link_colors,
        'customdata': link_labels
    }

all_links = get_sankey_data()

all_labels = list(riders) + list(teams) + list(manufacturers)

# colorear segun mayor contribucion
team_colors = {}
manufacturer_colors = {}

for team in teams:
    team_data = flow_data[flow_data['team_name'] == team]
    if not team_data.empty:
        max_rider = team_data.groupby('rider_name')['points'].sum().idxmax()
        team_colors[team] = rider_colors[max_rider]

for manufacturer in manufacturers:
    mfr_data = flow_data[flow_data['manufacturer'] == manufacturer]
    if not mfr_data.empty:
        max_rider = mfr_data.groupby('rider_name')['points'].sum().idxmax()
        manufacturer_colors[manufacturer] = rider_colors[max_rider]

# diagrama sankey
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=all_labels,
        color=[
            rider_colors[label] if label in riders
            else team_colors.get(label, "lightgrey") if label in teams
            else manufacturer_colors.get(label, "lightgrey") 
            for label in all_labels
        ]
    ),
    link=dict(
        source=all_links['source'],
        target=all_links['target'],
        value=all_links['value'],
        color=all_links['color'],
        hoverinfo='all',
        hovertemplate='%{value} points<br>%{customdata}',
        customdata=all_links['customdata']
    )
)])

buttons = [dict(
    label="All Riders",
    method="update",
    args=[{"link": get_sankey_data()}]
)]

for rider in riders:
    rider_data = get_sankey_data(rider)
    button = dict(
        label=rider,
        method="update",
        args=[{"link": rider_data}]
    )
    buttons.append(button)

fig.update_layout(
    updatemenus=[dict(
        type="dropdown",
        direction="down",
        active=0,
        x=1.0,
        y=1.15,
        showactive=True,
        buttons=buttons
    )]
)

fig.update_layout(
    title_text="Flujo de puntos MotoGP: Piloto → Equipos → Manufacturador (2018-2021)",
    font_size=10,
    height=800,
    width=1200,
    annotations=[
        dict(text="Seleccionar piloto:", x=0.9, y=1.18, showarrow=False)
    ]
)

fig.show()