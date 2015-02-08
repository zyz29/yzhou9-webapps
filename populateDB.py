#Use this script to populate the |restaurant| table of the database

import mysql.connector
import json
from decimal import *
import random

#Define database variables
DATABASE_USER = 'root'
DATABASE_HOST = '127.0.0.1'
DATABASE_NAME = 'feedND'

#Create connection to MySQL
cnx = mysql.connector.connect(user=DATABASE_USER, host=DATABASE_HOST, database=DATABASE_NAME)
cursor = cnx.cursor()

#Load json file
inputFile = open('restaurantData.json','r')
restaurantDict = json.load(inputFile)
inputFile.close()


#Loop through the restaurants and add info and menu to database
for key, restaurant in restaurantDict.iteritems():
	
	###############################
	## Add restaurant info first ##
	###############################

	inputDict = {
		'restCd' : key,
		'name' : restaurant['name'],
		'address' : restaurant['street_address'],
		'city' : restaurant['locality'],
		'state' : restaurant['region'],
		'zip' : restaurant['postal_code'],
		'phone' : restaurant['phone'],
		'lat' : restaurant['lat'],
		'lng' : restaurant['long'],
		'url' : restaurant['website_url']
	}

	#Insert this info into the database
	addRestaurant = ("INSERT INTO restaurants (restCd, name, address, city, state, zip, phone, lat, lng, url) VALUES (%(restCd)s,  %(name)s, %(address)s, %(city)s, %(state)s, %(zip)s, %(phone)s, %(lat)s, %(lng)s, %(url)s)")
	cursor.execute(addRestaurant,inputDict)

	###################
	## Add hour info ##
	###################

	cursor.execute("SELECT restId FROM restaurants WHERE restCd='%s'" % (key))
	restId = cursor.fetchone()[0]
	hourDict = restaurant['open_hours']
	monDict = hourDict['Monday']
	tueDict = hourDict['Tuesday']
	wedDict = hourDict['Wednesday']
	thuDict = hourDict['Thursday']
	friDict = hourDict['Friday']
	satDict = hourDict['Saturday']
	sunDict = hourDict['Sunday']
	
	for t in monDict:
		open_time = t[:8]
		close_time = t[-8:]
		cursor.execute("insert into hours (restId, day, open, close) values ('%s', 'M', '%s', '%s')" % (restId, open_time, close_time))
		
	for t in tueDict:
		open_time = t[:8]
		close_time = t[-8:]
		cursor.execute("insert into hours (restId, day, open, close) values ('')")
#Insert hours (hardcoded) for some restaurants
#addHours = ("insert into hours (restId, day, open, close) values ('0559f40309a19b3949d5','M','11:00:00','21:00:00')")
#cursor.execute(addHours)	

cnx.commit()
cnx.close()

