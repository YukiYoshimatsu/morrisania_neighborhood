"""
Template program for CSci 127 Honors:  citibike map
"""

#Import pandas for reading the data and folium for making the map:
import pandas as pd
import folium

#Read directly from the citibike feed (can be replaced by static file):
stations = pd.read_json('https://feeds.citibikenyc.com/stations/stations.json')

#Create a map, centered in NYC with a simple tile set:
mapBikes = folium.Map(location=[40.75, -73.99],tiles="Cartodb Positron",zoom_start=14)

#For each row of data:
for i,row in stations.iterrows():
    #Pull out the station info:
    beanList = row['stationBeanList']
    
    #Get the lat and lon to map the location
    lat = beanList['latitude']
    lon = beanList['longitude']

    #Check if the stations is not in service:
    if beanList['statusValue'] == 'Not In Service':
        name = beanList['stationName'] + ": Not In Service"
        i = folium.Icon(color='lightgray')
    #If it is, then can set color based on number of bikes:    
    else:
        name = beanList['stationName'] + ": " + str(beanList['availableBikes']) + " bikes available of " + str(beanList['totalDocks']) + " total bikes"
        if (beanList['availableBikes']/beanList['totalDocks']) < 0.25:
        #if beanList['availableBikes'] < 2:
            i = folium.Icon(color='red')
        else:
            i = folium.Icon(color='green')
        if beanList['totalDocks'] != 0:
            full= ((beanList['availableBikes']/beanList['totalDocks']) *100)//1*(1/100)
            name = name + " " +str(full*100) + "% (percent) of docks are full"        
    #Print to the console the name of the station to be added to the map:        
    print('Adding to map: ', name)
    
    #Add to the map:
    folium.Marker([lat,lon],popup = name,icon = i).add_to(mapBikes)


#Create the html file with the map:
mapBikes.save(outfile='bikeLocations.html')

#Modify the popup message to give the percent full the station is (i.e. the percentage of docks full at a station). ¥
#Hint: compute the percentage and then add it to your message-- remember to cast/convert it to string.
#Modify the program to only show a red marker if there are less than 25% of the bikes available (currently, it shows it for < 2). ¥