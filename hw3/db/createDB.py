#Use this script to create the database tables
#This script does NOT populate the tables with any data

import mysql.connector

#Define database variables
DATABASE_USER = 'root'
DATABASE_HOST = '127.0.0.1'
DATABASE_NAME = 'feedND'

#Create connection to MySQL
cnx = mysql.connector.connect(user=DATABASE_USER, host=DATABASE_HOST, use_unicode=True)
cursor = cnx.cursor()

###################################
## Create DB if it doesn't exist ##
###################################

createDB = (("CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARACTER SET utf8mb4") % (DATABASE_NAME))
cursor.execute(createDB)

#########################
## Switch to feednd DB ##
#########################

useDB = (("USE %s") % (DATABASE_NAME))
cursor.execute(useDB)

###########################
## Drop all tables first ##
###########################

#Hours
dropTableQuery = ("DROP TABLE IF EXISTS hours")
cursor.execute(dropTableQuery)

#OrderItems
dropTableQuery = ("DROP TABLE IF EXISTS orderItems")
cursor.execute(dropTableQuery)

#Orders
dropTableQuery = ("DROP TABLE IF EXISTS orders")
cursor.execute(dropTableQuery)

#Items
dropTableQuery = ("DROP TABLE IF EXISTS items")
cursor.execute(dropTableQuery)

#Menus
dropTableQuery = ("DROP TABLE IF EXISTS menus")
cursor.execute(dropTableQuery)

#Users
dropTableQuery = ("DROP TABLE IF EXISTS users")
cursor.execute(dropTableQuery)

#Restaurants
dropTableQuery = ("DROP TABLE IF EXISTS restaurants")
cursor.execute(dropTableQuery)

########################
## Create tables next ##
########################


#Restaurants
createTableQuery = ('''CREATE TABLE restaurants (
						restId INT NOT NULL AUTO_INCREMENT,
						restCd VARCHAR(20) CHARACTER SET utf8mb4 NOT NULL,
						name VARCHAR(45) CHARACTER SET utf8mb4 NOT NULL,
						address VARCHAR(100) CHARACTER SET utf8mb4 NOT NULL,
						city VARCHAR(45) CHARACTER SET utf8mb4 NOT NULL,
						state VARCHAR(20) CHARACTER SET utf8mb4 NOT NULL,
						zip VARCHAR(10) CHARACTER SET utf8mb4 NOT NULL,
						phone VARCHAR(20) CHARACTER SET utf8mb4 NOT NULL,
						lat DECIMAL(10,8) NOT NULL,
						lng DECIMAL(11,8) NOT NULL,
                                                url VARCHAR(100) CHARACTER SET utf8mb4,
						PRIMARY KEY (restId),
						UNIQUE KEY (restCd) USING BTREE)'''
                    )
cursor.execute(createTableQuery)

#Hours
createTableQuery = ('''CREATE TABLE hours (
						restId INT NOT NULL,
                                                day enum ('M','T','W','TH','F','S','SU') not null,
                                                open TIME NOT NULL,
                                                close TIME NOT NULL,
                                                PRIMARY KEY(restId,day,open),
                                                FOREIGN KEY(restId)
                                                REFERENCES restaurants(restId)
                                                ON DELETE CASCADE)'''
                    )
cursor.execute(createTableQuery)

#Menus
createTableQuery = ('''CREATE TABLE menus (
						menuId INT NOT NULL AUTO_INCREMENT,
						restId INT NOT NULL,
						menu_name VARCHAR(45) CHARACTER SET utf8mb4 NOT NULL,
						currency VARCHAR(10) CHARACTER SET utf8mb4 NOT NULL,
						PRIMARY KEY(menuId),
						FOREIGN KEY(restId) REFERENCES restaurants(restId) ON DELETE CASCADE,
						UNIQUE KEY(restId, menu_name) USING BTREE)'''
		   )
cursor.execute(createTableQuery)

#Items
createTableQuery = ('''CREATE TABLE items (
						itemId INT NOT NULL AUTO_INCREMENT,
						menuId INT NOT NULL,
						item_name VARCHAR(100) CHARACTER SET utf8mb4 NOT NULL,
						section VARCHAR(45) CHARACTER SET utf8mb4 NOT NULL,
						subsection VARCHAR(45) CHARACTER SET utf8mb4 NOT NULL,
						description VARCHAR(500) CHARACTER SET utf8mb4,
						price VARCHAR(45) CHARACTER SET utf8mb4,
						PRIMARY KEY(itemId),
						FOREIGN KEY(menuId) REFERENCES menus(menuId) ON DELETE CASCADE)'''
		   )
cursor.execute(createTableQuery)

#Users
createTableQuery = ('''CREATE TABLE users (
						userId INT NOT NULL AUTO_INCREMENT,
                                                name VARCHAR(45) CHARACTER SET utf8mb4  NOT NULL,
                                                email VARCHAR(45)  CHARACTER SET utf8mb4 NOT NULL,
                                                password VARCHAR(120)  CHARACTER SET utf8mb4 NOT NULL,
                                                phone VARCHAR(20) CHARACTER SET utf8mb4  NOT NULL,
                                                UNIQUE KEY (email) USING BTREE,
                                                PRIMARY KEY (userId))'''
		   )
cursor.execute(createTableQuery)

#Orders
createTableQuery = ('''CREATE TABLE orders (
						orderId INT NOT NULL AUTO_INCREMENT,
						userId INT NOT NULL,
						lastUpdated DATE NOT NULL,
						placed INT NOT NULL,
						PRIMARY KEY(orderId),
						FOREIGN KEY(userId) REFERENCES users(userId) ON DELETE CASCADE)'''
		   )
cursor.execute(createTableQuery)

#OrderItems
createTableQuery = ('''CREATE TABLE orderItems (
                                                orderItemId INT NOT NULL AUTO_INCREMENT,
                                                orderId INT NOT NULL,
						itemId INT NOT NULL,
                                                quantity INT NOT NULL,
                                                PRIMARY KEY(orderItemId),
						UNIQUE KEY(orderId, itemId) USING BTREE,
						FOREIGN KEY (orderId) references orders(orderId) on delete cascade,
                                                FOREIGN KEY (itemId) references items(itemId) on delete cascade)'''
                   )
cursor.execute(createTableQuery)

#Commit the data and close the connection to MySQL
cnx.commit()
cnx.close()
