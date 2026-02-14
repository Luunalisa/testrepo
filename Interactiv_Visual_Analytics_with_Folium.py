import folium
import pandas as pd
# Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
# Import folium MousePosition plugin
from folium.plugins import MousePosition
# Import folium DivIcon plugin
from folium.features import DivIcon
import requests
# Download and read the `spacex_launch_geo.csv`

import io

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv"

# Download the file
response = requests.get(URL)

# Convert to file-like object
spacex_csv_file = io.StringIO(response.text)

# Read into pandas dataframe
spacex_df = pd.read_csv(spacex_csv_file)

print(spacex_df.head())

# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]
launch_sites_df

# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,
    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)

# Initial the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)
# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label

for idx, row in launch_sites_df.iterrows():
    coord = [row['Lat'], row['Long']]
    site_name = row['Launch Site']
    # Add a circle
    folium.Circle(
        location=coord,
        radius=1000,
        color='#000000',
        fill=True,
        fill_color='#000000',
        fill_opacity=0.2
    ).add_child(folium.Popup(site_name)).add_to(site_map)
    
    # Add a marker with a label
    folium.map.Marker(
        location=coord,
        icon=DivIcon(
            icon_size=(20,20),
            icon_anchor=(0,0),
            html=f'<div style="font-size: 12pt; color:#d35400;"><b>{site_name}</b></div>'
        )
    ).add_to(site_map)

# Display the map
site_map
spacex_df.tail(10)

marker_cluster = MarkerCluster()
# Define a mapping from class to marker color
color_map = {1: 'green', 0: 'red'}

# Create the new column 'marker_color' based on the 'class' column
spacex_df['marker_color'] = spacex_df['class'].map(color_map)

# Check the new column
spacex_df[['class', 'marker_color']].head()

# Add marker_cluster to current site_map
site_map.add_child(marker_cluster)

# for each row in spacex_df data frame
# create a Marker object with its coordinate
# and customize the Marker's icon property to indicate if this launch was successed or failed, 
# e.g., icon=folium.Icon(color='white', icon_color=row['marker_color']

# Loop through each row in spacex_df
for index, record in spacex_df.iterrows():
    # TODO: Create and add a Marker cluster to the site map
    # marker = folium.Marker(...)

    
    # Create a Marker with coordinates
    marker = folium.Marker(
        location=[record['Lat'], record['Long']],
        icon=folium.Icon(color='white', icon_color=record['marker_color']),
        popup=f"Launch Site: {record['Launch Site']}<br>Class: {record['class']}"
    )
    # Add the marker to the cluster
    marker_cluster.add_child(marker)

# Display the map
site_map

# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)

site_map.add_child(mouse_position)
site_map

from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# find coordinate of the closet coastline
# e.g.,: Lat: 28.56367  Lon: -80.57163
# distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)
coastline_lat = 28.56364
coastline_lon = -80.56764
launch_site_lat = launch_sites_df.loc[launch_sites_df['Launch Site'] == 'CCAFS LC-40', 'Lat'].values[0]
launch_site_lon= launch_sites_df.loc[launch_sites_df['Launch Site'] == 'CCAFS LC-40', 'Long'].values[0]
distance_coastline = calculate_distance(
    launch_site_lat, launch_site_lon,
    coastline_lat, coastline_lon
)

print(f"Distance to coastline: {distance_coastline:.3f} km")

# Coordinates for launch site and closest coastline point
coastline_coords = [coastline_lat, coastline_lon]
launch_site_coords = [launch_site_lat, launch_site_lon]

# Create the map centered between the two points
map_center = [(launch_site_coords[0] + coastline_coords[0]) / 2,
              (launch_site_coords[1] + coastline_coords[1]) / 2]
site_map = folium.Map(location=map_center, zoom_start=14)

# Add marker for launch site
folium.Marker(location=launch_site_coords, popup='Launch Site').add_to(site_map)

# Add marker for coastline point
folium.Marker(location=coastline_coords, popup='Coastline Point').add_to(site_map)

# Add distance marker on coastline point with distance displayed
distance_marker = folium.Marker(
    location=coastline_coords,
    icon=DivIcon(
        icon_size=(100, 20),
        icon_anchor=(0, 0),
        html=f'<div style="font-size: 12pt; color:#d35400;"><b>{distance_coastline:.2f} KM</b></div>'
    )
)
distance_marker.add_to(site_map)
site_map

# Create a `folium.PolyLine` object using the coastline coordinates and launch site coordinate
# lines=folium.PolyLine(locations=coordinates, weight=1)
lines=folium.PolyLine(locations=[launch_site_coords, coastline_coords],
                color='blue', weight=1).add_to(site_map)

site_map.add_child(lines)


# Create a marker with distance to a closest city, railway, highway, etc.
# Draw a line between the marker to the launch site

railway_lat = 28.55085
railway_lon = -80.56874
launch_site_lat = launch_sites_df.loc[launch_sites_df['Launch Site'] == 'CCAFS LC-40', 'Lat'].values[0]
launch_site_lon= launch_sites_df.loc[launch_sites_df['Launch Site'] == 'CCAFS LC-40', 'Long'].values[0]
distance_railway = calculate_distance(
    launch_site_lat, launch_site_lon,
    railway_lat, railway_lon
)

print(f"Distance to railway: {distance_railway:.3f} km")

# Coordinates for launch site and closest railway point
launch_site_coords = [launch_site_lat, launch_site_lon]
railway_coords = [railway_lat, railway_lon]

# Create the map centered between the two points
map_center = [(launch_site_coords[0] + railway_coords[0]) / 2,
              (launch_site_coords[1] + railway_coords[1]) / 2]
site_map = folium.Map(location=map_center, zoom_start=14)

# Add marker for launch site
folium.Marker(location=launch_site_coords, popup='Launch Site').add_to(site_map)

# Add marker for railway point
folium.Marker(location=railway_coords, popup='Railway Point').add_to(site_map)

# Add distance marker on railway point with distance displayed
distance_marker = folium.Marker(
    location=railway_coords,
    icon=DivIcon(
        icon_size=(100, 20),
        icon_anchor=(0, 0),
        html=f'<div style="font-size: 12pt; color:#d35400;"><b>{distance_railway:.2f} KM</b></div>'
    )
)
distance_marker.add_to(site_map)

lines=folium.PolyLine(locations=[launch_site_coords, railway_coords],
                color='blue', weight=1).add_to(site_map)

site_map.add_child(lines)

highway_lat = 28.57157
highway_lon = -80.58525
launch_site_lat = launch_sites_df.loc[launch_sites_df['Launch Site'] == 'CCAFS LC-40', 'Lat'].values[0]
launch_site_lon= launch_sites_df.loc[launch_sites_df['Launch Site'] == 'CCAFS LC-40', 'Long'].values[0]
distance_highway = calculate_distance(
    launch_site_lat, launch_site_lon,
    highway_lat, highway_lon
)

print(f"Distance to highway: {distance_highway:.3f} km")

# Coordinates for launch site and closest railway point
launch_site_coords = [launch_site_lat, launch_site_lon]
highway_coords = [highway_lat, highway_lon]

# Create the map centered between the two points
map_center = [(launch_site_coords[0] + highway_coords[0]) / 2,
              (launch_site_coords[1] + highway_coords[1]) / 2]
site_map = folium.Map(location=map_center, zoom_start=14)

# Add marker for launch site
folium.Marker(location=launch_site_coords, popup='Launch Site').add_to(site_map)

# Add marker for highway point
folium.Marker(location=highway_coords, popup='Highway Point').add_to(site_map)

# Add distance marker on highway point with distance displayed
distance_marker = folium.Marker(
    location=highway_coords,
    icon=DivIcon(
        icon_size=(100, 20),
        icon_anchor=(0, 0),
        html=f'<div style="font-size: 12pt; color:#d35400;"><b>{distance_highway:.2f} KM</b></div>'
    )
)
distance_marker.add_to(site_map)

lines=folium.PolyLine(locations=[launch_site_coords, highway_coords],
                color='blue', weight=1).add_to(site_map)

site_map.add_child(lines)


city_lat = 28.56364
city_lon = -80.56764
launch_site_lat = launch_sites_df.loc[launch_sites_df['Launch Site'] == 'CCAFS LC-40', 'Lat'].values[0]
launch_site_lon= launch_sites_df.loc[launch_sites_df['Launch Site'] == 'CCAFS LC-40', 'Long'].values[0]
distance_city = calculate_distance(
    launch_site_lat, launch_site_lon,
    city_lat, city_lon
)

print(f"Distance to highway: {distance_city:.3f} km")

# Coordinates for launch site and closest railway point
launch_site_coords = [launch_site_lat, launch_site_lon]
city_coords = [city_lat, city_lon]

# Create the map centered between the two points
map_center = [(launch_site_coords[0] + city_coords[0]) / 2,
              (launch_site_coords[1] + city_coords[1]) / 2]
site_map = folium.Map(location=map_center, zoom_start=14)

# Add marker for launch site
folium.Marker(location=launch_site_coords, popup='Launch Site').add_to(site_map)

# Add marker for city point
folium.Marker(location=city_coords, popup='City Point').add_to(site_map)

# Add distance marker on city point with distance displayed
distance_marker = folium.Marker(
    location=city_coords,
    icon=DivIcon(
        icon_size=(100, 20),
        icon_anchor=(0, 0),
        html=f'<div style="font-size: 12pt; color:#d35400;"><b>{distance_city:.2f} KM</b></div>'
    )
)
distance_marker.add_to(site_map)

lines=folium.PolyLine(locations=[launch_site_coords, city_coords],
                color='blue', weight=1).add_to(site_map)

site_map.add_child(lines)