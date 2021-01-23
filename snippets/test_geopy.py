# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 14:09:01 2020

@author: mario
"""

def address_from_coordinates_0(longitude=14.718719,latitude=40.718220):
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="italycoviddataBot")
    coordinates=str(latitude)+','+str(longitude)
    location = geolocator.reverse(coordinates)
    user_location={}
    user_location['reg']=location.raw['address'].get('state',None)
    user_location['prov']=location.raw['address'].get('county',None)
    try:
        user_location['city']=location.raw['address']['city']
    except:
        try:
            user_location['city']=location.raw['address']['town']
        except:
            try:
                user_location['city']=location.raw['address']['village']
            except:
                try:
                    user_location['city']=location.raw['address'].get('county')
                except:
                    print('cannot find city')
    user_location['address']=location.raw['display_name']
    return location, user_location

def address_from_coordinates(longitude=14.718719,latitude=40.718220):
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="italycoviddataBot")
    coordinates=str(latitude)+','+str(longitude)
    location = geolocator.reverse(coordinates)
    user_location={}
    user_location['reg']=location.raw['address'].get('state',None)
    user_location['prov']=location.raw['address'].get('county',None)
    addr=location.raw['address']
    user_location['city']=addr.get('city',addr.get('town',addr.get('village',addr.get('county'))))
    user_location['address']=location.raw['display_name']
    return location, user_location

test_list=[[14.718719,40.718220],
           [09.07,39.13],
           [12.45,43.54],
           ]

user_locations=[]
locations=[]
for coo in test_list:
    print('#------#')
    location,user_location= address_from_coordinates(coo[0],coo[1])
    print(user_location)
    user_locations.append(user_location)
    locations.append(location)