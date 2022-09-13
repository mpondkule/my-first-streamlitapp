import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import pandas as pd
import streamlit as st
from urllib.request import urlopen
import json
from copy import deepcopy

@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df

# Read the data of volcanoes around the world
volcanoes_around_the_world_raw = load_data(path="./data/processed/volcano_ds_pop.csv")
volcanoes_around_the_world = deepcopy(volcanoes_around_the_world_raw)

st.title("Volcanoes around the World")
# Setting up columns
left_column, middle_column, right_column = st.columns([6, 6, 6])

volcanoes_around_the_world['Country'] = volcanoes_around_the_world['Country'].replace({'United States':'United States of America',
                                                                      'Tanzania':'United Republic of Tanzania',
                                                                      'Martinique':'Martinique',
                                                                      'Sao Tome & Principe':'Sao Tome and Principe',
                                                                      'Guadeloupe':'Guadeloupe',
                                                                      'Wallis & Futuna':'Wallis and Futuna'})

# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)
if st.checkbox("Show Volcanoes Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(data=volcanoes_around_the_world)

# Widgets: selectbox
countries = ["All"]+sorted(pd.unique(volcanoes_around_the_world['Country']))
country = left_column.selectbox("Choose a country", countries)

# Widgets: selectbox
v_name = ["All"]+sorted(pd.unique(volcanoes_around_the_world['Volcano Name']))
volcano_name = middle_column.selectbox("Choose a Volcano name", v_name)

# Widgets: selectbox
v_type = ["All"]+sorted(pd.unique(volcanoes_around_the_world['Type']))
volcano_type = right_column.selectbox("Choose a Volcano type", v_type)

# Flow control and plotting
if (country == "All" and (volcano_name == "All" and volcano_type == "All")):
    volcanoes = volcanoes_around_the_world
elif (country != "All" and (volcano_name == "All" and volcano_type == "All")):
    volcanoes = volcanoes_around_the_world[volcanoes_around_the_world["Country"] == country]
elif (country == "All" and (volcano_name != "All" and volcano_type == "All")):
    volcanoes = volcanoes_around_the_world[volcanoes_around_the_world["Volcano Name"] == volcano_name]
elif (country == "All" and (volcano_name == "All" and volcano_type != "All")):
    volcanoes = volcanoes_around_the_world[volcanoes_around_the_world["Type"] == volcano_type]
elif (country != "All" and (volcano_name != "All" and volcano_type == "All")):
    volcanoes = volcanoes_around_the_world[((volcanoes_around_the_world["Country"] == country) &
                                            (volcanoes_around_the_world["Volcano Name"] == volcano_name))]
elif (country != "All" and (volcano_name == "All" and volcano_type != "All")):
    volcanoes = volcanoes_around_the_world[((volcanoes_around_the_world["Country"] == country) &
                                            (volcanoes_around_the_world["Type"] == volcano_type))]
elif (country == "All" and (volcano_name != "All" and volcano_type != "All")):
    volcanoes = volcanoes_around_the_world[((volcanoes_around_the_world["Volcano Name"] == volcano_name) &
                                            (volcanoes_around_the_world["Type"] == volcano_type))]
elif (country != "All" and (volcano_name != "All" and volcano_type != "All")):
    volcanoes = volcanoes_around_the_world[((volcanoes_around_the_world["Country"] == country) &
                                            (volcanoes_around_the_world["Volcano Name"] == volcano_name) &
                                            (volcanoes_around_the_world["Type"] == volcano_type))]

# Sample Choropleth mapbox using Plotly GO
#st.subheader("Plotly Map")
st.title("Green Energy in Switzerland")

with open('./data/raw/countries.geojson') as json_file:
    countries = json.load(json_file)
#countries

with open('./data/raw/georef-switzerland-kanton.geojson') as response:
    cantons_json = json.load(response)

#Green energy in Switzerland
df = pd.read_csv("./data/processed/renewable_power_plants_CH.csv", dtype={"postcode": str})

cantons_dict = {'TG':'Thurgau', 'GR':'Graubünden', 'LU':'Luzern', 'BE':'Bern', 'VS':'Valais',
                'BL':'Basel-Landschaft', 'SO':'Solothurn', 'VD':'Vaud', 'SH':'Schaffhausen', 'ZH':'Zürich',
                'AG':'Aargau', 'UR':'Uri', 'NE':'Neuchâtel', 'TI':'Ticino', 'SG':'St. Gallen', 'GE':'Genève',
                'GL':'Glarus', 'JU':'Jura', 'ZG':'Zug', 'OW':'Obwalden', 'FR':'Fribourg', 'SZ':'Schwyz',
                'AR':'Appenzell Ausserrhoden', 'AI':'Appenzell Innerrhoden', 'NW':'Nidwalden', 'BS':'Basel-Stadt'}

#counties["features"][0]
df = df.replace({"canton": cantons_dict})

# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)
if st.checkbox("Show Green Energy in Switzerland Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(data=df)

# Setting up columns
left_column_1, right_column_2 = st.columns([4, 4])

# Widgets: selectbox
cantons = ["All"]+sorted(pd.unique(df['canton']))
canton = left_column_1.selectbox("Choose a canton", cantons)

# Widgets: selectbox
energy_sources = ["All"]+sorted(pd.unique(df['energy_source_level_2']))
energy_source = right_column_2.selectbox("Choose the Energy source", energy_sources)

# Flow control and plotting
if (canton == "All" and energy_source == "All"):
    df_select = df
elif (canton != "All" and energy_source == "All"):
    df_select = df[df["canton"] == canton]
elif (canton == "All" and energy_source != "All"):
    df_select = df[df["energy_source_level_2"] == energy_source]
elif (canton != "All" and energy_source != "All"):
    df_select = df[(df["energy_source_level_2"] == energy_source) & (df["canton"] == canton)]

fig = px.scatter_mapbox(volcanoes, lat="Latitude", lon="Longitude",
                        hover_name="Volcano Name",
                        hover_data=["Elev","Type","Latitude","Longitude","Status"],
                        color_discrete_sequence=px.colors.qualitative.Light24, zoom=3, width=1500, height=1000)
fig.update_layout(mapbox_style="stamen-terrain")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_layout(title_text = 'Volcanoes around the World', showlegend = True)

fig1 = px.choropleth_mapbox(df_select, geojson=cantons_json,
                            locations='canton', color='energy_source_level_2', featureidkey='properties.kan_name',
                            mapbox_style="stamen-terrain",
                            zoom=6, center={"lat": 46.798333, "lon": 8.231944},
                            opacity=0.5
                            )

if (len(fig1.data) == 4):
    fig.add_trace(fig1.data[0])
    fig.add_trace(fig1.data[1])
    fig.add_trace(fig1.data[2])
    fig.add_trace(fig1.data[3])
elif (len(fig1.data) == 3):
    fig.add_trace(fig1.data[0])
    fig.add_trace(fig1.data[1])
    fig.add_trace(fig1.data[2])
elif (len(fig1.data) == 2):
    fig.add_trace(fig1.data[0])
    fig.add_trace(fig1.data[1])
elif (len(fig1.data) == 1):
    fig.add_trace(fig1.data[0])

fig.update_geos(fitbounds="locations", visible=False)
st.plotly_chart(fig)


question = "which green energy source in switzerland would possibly be effected the most if" \
         " there is super volcanic erruption in mount Etna, Italy?"
paragraph = "https://en.wikipedia.org/wiki/Volcanic_ash"
"Question: ",question
"Answer: ", paragraph