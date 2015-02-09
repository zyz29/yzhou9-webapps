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
		cursor.execute("insert into hours (restId, day, open, close) values ('%s', 'T', '%s', '%s')" % (restId, open_time, close_time))

	for t in wedDict:
		open_time = t[:8]
		close_time = t[-8:]
		cursor.execute("insert into hours (restId, day, open, close) values ('%s', 'W', '%s', '%s')" % (restId, open_time, close_time))

	for t in thuDict:
		open_time = t[:8]
		close_time = t[-8:]
		cursor.execute("insert into hours (restId, day, open, close) values ('%s', 'TH', '%s', '%s')" % (restId, open_time, close_time))

	for t in friDict:
		open_time = t[:8]
		close_time = t[-8:]
		cursor.execute("insert into hours (restId, day, open, close) values ('%s', 'F', '%s', '%s')" % (restId, open_time, close_time))

	for t in satDict:
		open_time = t[:8]
		close_time = t[-8:]
		cursor.execute("insert into hours (restId, day, open, close) values ('%s', 'S', '%s', '%s')" % (restId, open_time, close_time))

	for t in sunDict:
		open_time = t[:8]
		close_time = t[-8:]
		cursor.execute("insert into hours (restId, day, open, close) values ('%s', 'SU', '%s', '%s')" % (restId, open_time, close_time))

	###############
	## Add menus ##
	###############

	menuList = restaurant['menus']

	for menuDict in menuList:
		currency = menuDict['currency_symbol']
		menu_name = menuDict['menu_name']
		cursor.execute("insert into menus (restId, menu_name, currency) values ('%s', '%s', '%s')" % (restId, menu_name, currency))

		###############
		## Add items ##
		###############

		cursor.execute("SELECT menuId FROM menus WHERE restId='%s' AND menu_name='%s'" % (restId, menu_name))
		menuId = cursor.fetchone()[0]

		secList = menuDict['sections']

		for secDict in secList:
			section_name = secDict['section_name']
			if section_name is not None:
				section_name.encode('ascii', 'ignore')
			subsecList = secDict['subsections']

			for subsecDict in subsecList:
				subsection_name = subsecDict['subsection_name']
				if subsection_name is not None:
					subsection_name.encode('ascii', 'ignore')
				contentList = subsecDict['contents']

				for contentDict in contentList:
					item_type = contentDict.get('type')
					if item_type == 'ITEM':
						description = contentDict.get('description')
						if description is not None:
							description.encode('ascii', 'ignore')
						item_name = contentDict.get('name')
						if item_name is not None:
							item_name.encode('ascii', 'ignore')
						price = contentDict.get('price')
						cursor.execute("""insert into items (menuId, item_name, section, subsection, description, price) values ("%s", "%s", "%s", "%s", "%s", "%s")""" % (menuId, item_name, section_name, subsection_name, description, price))

cnx.commit()
cnx.close()
