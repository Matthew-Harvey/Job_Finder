import sqlite3 as sql # getting sequel module for database interactions
import tkinter as tk # modules running the GUI of the program
from tkinter import ttk
from tkinter import *
import re # module used for string manipulations
import hashlib # controlling password hashes
import os # random string of x length command
import binascii # hexify, changing binary to hex formatting
import random # generating random probabilities or integers in a range
import pgeocode # translating a postcode to longitude and latitudes

fname = "Schools.csv" # name of excel file that contains all of the government published school data
def loading():
    f = open(fname, "r") # opening the file to read
    i = 0
    for line in f: # getting a line count
        i = i+1
    j = 0
    f.close() # closing file
    k = open(fname, "r") # re-opening the file to read
    i = int(i / 2)-3 # changing the line count by dividing by 2 and then subtracting 3
    for line in k:
        if j <= i:
            l = k.readline()
            l = l.split(",") # formatting each line of the file
            for item in l:
                if item == '\n' or item == ' ' or item == '':
                    l.remove(item) # deleting all unwanted characters from the string
            name = l[4]
            ident = l[0]
            loc = l[2]
            info = l[5]
            _open = l[6] # setting appropriate names for each section of the line
            _type = l[8]
            lowage = l[9]
            highage = l[10]
            gender = l[11]
            street = l[12]
            locality = l[13]
            cont = True
            try:
                website = l[len(l)-11] # test for "www" or "http" at start of sting at various positions
                if website[0] == "h" or website[0] == "w":
                    cont = False
            except:
                cont = True
            east = l[len(l)-2]
            north = l[len(l)-1]
            try:
                import pyproj # importing a module to convert units
                bng = pyproj.Proj(init='epsg:27700')
                wgs84 = pyproj.Proj(init='epsg:4326')
            except:
                error = True
            lon,lat = pyproj.transform(bng,wgs84, east, north) # calculating latitude and longitudes from easting and northing.
            try:
                if cont == False:
                    east = int(east)
                    north = int(north)
                    handle = sql.connect("Schools.db") # inserting all of the relevant data into the database for every line/school
                    cursor = handle.cursor()
                    cursor.execute("INSERT INTO DATA VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (int(ident), name, loc, info, _open, _type, int(lowage), int(highage), gender, street, locality, website, east, north, lon, lat))
                    handle.commit()
                    handle.close()
            except:
                cont = True # placeholder
        j = j+1 # increasing j alongside iteration
    k.close()

handle = sql.connect("Schools.db") # creating all of the tables before some are populated
cursor = handle.cursor()
cursor.execute("CREATE TABLE DATA(SCHOOLID INT, NAME TEXT, LOCATION TEXT, INFO TEXT, OPEN TEXT, TYPE TEXT, LOWAGE INT, HIGHAGE INT, GENDER TEXT, STREET TEXT, LOCALITY TEXT, WEBSITE TEXT, EAST INT, NORTH INT, LONG TEXT, LATIT TEXT)")
cursor.execute("CREATE TABLE RECOMMEND3(SCHOOLID INT, USERID)")
cursor.execute("CREATE TABLE RATING3(SCHOOLID INT, RATING INT, COMMENT TEXT)")
handle.commit()
handle.close()
loading() # populate table "DATA" by running the function