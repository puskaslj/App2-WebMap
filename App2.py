import folium
import pandas

data = pandas.read_csv("Resources/Volcanoes.txt")
latitudeData = list(data["LAT"])
longitudeData = list(data["LON"])
elevationData = list(data["ELEV"])

def color_picker(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

map = folium.Map(
    location = [43.615453, -116.203827],
    zoom_start = 6,
    tiles = "Stamen Terrain"
)

volcanoes = folium.FeatureGroup(name = "Volcanoes")

for latitude, longitude, elevation in zip(latitudeData, longitudeData, elevationData):
    volcanoes.add_child(
        folium.CircleMarker(
            location = [latitude, longitude],
            popup = str(elevation) + "m",
            radius = 6,
            color = 'grey',
            fill_color = color_picker(elevation),
            fill_opacity = 0.7))

pop_density = folium.FeatureGroup(name = "Population density")

pop_density.add_child(
    folium.GeoJson(
        data = open("Resources/world.json", 'r', encoding = 'utf-8-sig').read(),
        style_function = lambda color: {
            'fillColor':
                'green' if color['properties']['POP2005'] < 10000000 else
                'orange' if 10000000 <= color['properties']['POP2005'] < 20000000 else
                'red'})),

        # DOES THIS WORK - maybe it should be like below or using elif?
        # style_function2 = lambda x: {
        #     'fillColor':
        #         'green' if x['properties']['POP2005'] < 10000000 else (
        #         'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else
        #         'red')},

map.add_child(volcanoes)
map.add_child(pop_density)
map.add_child(folium.LayerControl())

map.save("USA_Map.html")
