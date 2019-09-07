import numpy as np

import utm   # https://github.com/Turbo87/utm


def to_utm(latitudes, longitudes):

	""" 
	Converts geographic coordinates to Universal Transverse Mercator (UTM) 
	"""

	easting=[]
	northing=[]
	tmp=None
	for lat, lon in zip(latitudes, longitudes):
		tmp = utm.from_latlon(lat, lon)
		easting.append(tmp[0])
		northing.append(tmp[1])

	znumber, zletter = tmp[2], tmp[3]
	return np.array(easting), np.array(northing), znumber, zletter
 

def geo_distance(latitudes, longitudes):

	""" 
	Calculates an equirectangular approximation of the lineal displacement (in m) 
	from geographic coordinates. See:

	https://www.movable-type.co.uk/scripts/latlong.html
	"""
	
	distance = 0	
	lon = np.radians(longitudes)
	lat = np.radians(latitudes)

	for i in range(1, len(lon)):
		x = (lon[i] - lon[i-1]) * np.cos( (lat[i]+lat[i-1])/2.0 )
		y = lat[i] - lat[i-1]
		distance += 6371e3 * np.sqrt(x*x + y*y ) 

	return distance

def utm_distance(easting, northing):

	""" 
	Calculates an approximation of the lineal displacement (in m) 
	from UTM coordinates.
	"""
	
	distance = 0	

	for i in range(1, len(northing)):
		x = easting[i] - easting[i-1]
		y = northing[i] - northing[i-1]
		distance += np.sqrt(x*x + y*y ) 

	return distance

