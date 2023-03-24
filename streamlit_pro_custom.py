# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns
import folium
#from streamlit.components.v1 import IFrame


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
         math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(lat2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def emissions(distance, fuel_efficiency, passengers):
    CO2_PER_LITER = 2.31 # kg CO2 per liter of gasoline
    liters = distance / fuel_efficiency
    total_emissions = liters * CO2_PER_LITER
    return total_emissions / passengers

# def car_sharing_emissions_multiple_cars(locations, workplace_coordinates, fuel_efficiency):
#     total_emissions = 0
#     for _, coordinates in locations.items():
#         distance_to_location = haversine_distance(*workplace_coordinates, *coordinates) * 2
#         distance_to_workplace = haversine_distance(*coordinates, *workplace_coordinates) * 2
#         total_emissions += emissions(distance_to_location + distance_to_workplace, fuel_efficiency, 1)
#     return total_emissions / len(locations)


import itertools

def nearest_neighbor_path(start_location, other_locations):
    path = [start_location]
    unvisited_locations = other_locations.copy()

    while unvisited_locations:
        current_location = path[-1]
        next_location = min(unvisited_locations, key=lambda x: haversine_distance(*current_location, *x))
        unvisited_locations.remove(next_location)
        path.append(next_location)
    
    return path

def car_sharing_emissions_optimal(locations, workplace_coordinates, fuel_efficiency, passengers):
    min_emissions = None

    for start_location, start_coordinates in locations.items():
        other_locations = [coordinates for loc, coordinates in locations.items() if loc != start_location]
        path = nearest_neighbor_path(start_coordinates, other_locations)
        
        total_distance = 0
        for i in range(len(path) - 1):
            total_distance += haversine_distance(*path[i], *path[i+1]) * 2
        total_distance += haversine_distance(*path[-1], *workplace_coordinates) * 2
        
        current_emissions = emissions(total_distance, fuel_efficiency, passengers)
        
        if min_emissions is None or current_emissions < min_emissions:
            min_emissions = current_emissions

    return min_emissions

def car_sharing_emissions_total(locations, workplace_coordinates, fuel_efficiency):
    total_emissions = 0

    for start_location, start_coordinates in locations.items():
        other_locations = [coordinates for loc, coordinates in locations.items() if loc != start_location]
        path = nearest_neighbor_path(start_coordinates, other_locations)
        
        total_distance = 0
        for i in range(len(path) - 1):
            total_distance += haversine_distance(*path[i], *path[i+1]) * 2
        total_distance += haversine_distance(*path[-1], *workplace_coordinates) * 2
        
        total_emissions += emissions(total_distance, fuel_efficiency, 1)
    
    return total_emissions



def main():
    
    
    # Define the initial map location and zoom level
    lat, lon = 47.490000, 9.430000
    zoom_start = 12

    # Create a map object using Folium
    m = folium.Map(location=[lat, lon], zoom_start=zoom_start)

    st.title("Carbon Footprint and Savings Calculator")
    
    
    workplace_lat = st.sidebar.number_input("Workplace Latitude", min_value=-90.00000, max_value=90.000000, value=47.490000, step=0.01)
    workplace_lon = st.sidebar.number_input("Workplace Longitude", min_value=-180.000000, max_value=180.000000, value=9.430000, step=0.01)
    workplace_coordinates = (workplace_lat, workplace_lon)

    # Add a red marker to the map to indicate the location of the workplace
    folium.Marker(location=[workplace_lat, workplace_lon], popup="Workplace", icon=folium.Icon(color='red')).add_to(m)

    locations = {}
    for i in range(1, 6):
        lat = st.sidebar.number_input(f"Location {i} Latitude", min_value=-90.0, max_value=90.0, value=47.480000, step=0.01)
        lon = st.sidebar.number_input(f"Location {i} Longitude", min_value=-180.0, max_value=180.0,value = 9.410000,   step=0.01)
        if haversine_distance(workplace_lat, workplace_lon, lat, lon) <= 50:
            locations[f"Location {i}"] = (lat, lon)
        else:
            st.sidebar.error(f"Location {i} is more than 50 km away from the workplace. Please adjust the coordinates.")

    fuel_efficiency = st.sidebar.number_input("Fuel Efficiency (km/l)", min_value=1, max_value=50, value=15, step=1)

    results = []
    
    individual_emissions = []
    
    for location, coordinates in locations.items():
        folium.Marker(location=coordinates, popup=location).add_to(m)
    
        distance = haversine_distance(*coordinates, workplace_lat, workplace_lon) * 2
        emission = emissions(distance, fuel_efficiency, 1)
        individual_emissions.append(emission)
    
    total_individual_emissions = sum(individual_emissions)
    
    for location, coordinates in locations.items():
        other_locations = {loc: coords for loc, coords in locations.items() if loc != location}
        path = nearest_neighbor_path(coordinates, list(other_locations.values()))
        
        total_distance = haversine_distance(*coordinates, *workplace_coordinates) * 2
        for i in range(len(path) - 1):
            total_distance += haversine_distance(*path[i], *path[i+1]) * 2
    
        car_sharing_emission = emissions(total_distance, fuel_efficiency, 5)
        savings = total_individual_emissions - car_sharing_emission
    
        distance = haversine_distance(*coordinates, workplace_lat, workplace_lon) * 2
    
        results.append((location, distance, total_individual_emissions, car_sharing_emission, savings))
    




    
    m.save('map.html')
    with open('map.html', 'r') as f:
        map_html = f.read()
    st.components.v1.html(map_html, height=600)



    results_df = pd.DataFrame(results, columns=["Location", "Distance (km)", "Emission (kg CO2)", "Car Sharing Emission (kg CO2)", "Savings (kg CO2)"])
    st.table(results_df)

    if results:
        optimal_location = max(results, key=lambda x: x[4])
        st.subheader(f"Optimal starting location: {optimal_location[0]}")
        st.write(f"Savings in emissions: {optimal_location[4]:.2f} kg CO2")
    else:
        st.error("Please input valid coordinates for all locations within 50 km from the workplace.")
        

    emissions_df = results_df[['Location', 'Savings (kg CO2)']]
    ax = emissions_df.plot(kind='bar', x='Location', y='Savings (kg CO2)', color='green', legend=None)
    
    ax.set_xlabel('Location')
    ax.set_ylabel('Savings (kg CO2)')
    ax.set_title('Total Savings per Location')
    
    st.pyplot(fig=ax.figure)

    
if __name__ == "__main__":
    main()
