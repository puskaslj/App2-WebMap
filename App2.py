import folium
import pandas

data = pandas.read_csv("Resources/Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

def color_picker(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation <3000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(
    location=[43.615453, -116.203827], 
    zoom_start=6, 
    tiles="Stamen Terrain"
)

vulc = folium.FeatureGroup(name="Volcanoes")


for lt, ln, el in zip(lat, lon, elev):
    vulc.add_child(folium.CircleMarker(
        location=[lt, ln], 
        popup=str(el)+"m", 
        radius = 6, 
        color = 'grey', 
        fill_color=color_picker(el), 
        fill_opacity=0.7
))

popd = folium.FeatureGroup(name="Population density")

popd.add_child(folium.GeoJson(
    data=open("Resources/world.json", 'r',
    encoding='utf-8-sig').read(),
    style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 
    else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}
))

map.add_child(vulc)
map.add_child(popd)
map.add_child(folium.LayerControl())

map.save("USA_Map.html")

