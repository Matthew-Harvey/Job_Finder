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

def getinfo():
    f = open("JobCentres", "r") # opening job centre document, that contains all the relevant data, to read 
    for line in f:
        line = f.readline()
        line = str(line) # casting each line to a string and then removing the last 5 characters before splitting words
        centreid = line[:5]
        centreid = centreid.strip()
        add = line.split("\t")
        string = ""
        for i in range(0, len(add)):
            if i != 0:
                address = str(add[i])
                string = string + " " + address # appending each word in the line without invalid characters into a long string
        string = string.strip()
        postcode = add[len(add)-1] # removing last character
        postcode = str(postcode)
        postcode1 = postcode.strip()
        try:
            nomi = pgeocode.Nominatim('GB')
            info = nomi.query_postal_code(postcode1) # get all the data about the postcode
            lat = info[9] # attaining latitude and longitude as an independant variable
            longit = info[10]
        except:
            lat = 0
            longit = 0
        handle = sql.connect("JobCentreData.db") # inserting all the data about one job centre into the database, per iteration
        cursor = handle.cursor()
        cursor.execute("INSERT INTO DATA VALUES(?,?,?,?,?)", (centreid, longit, lat, postcode1, string))
        handle.commit()
        handle.close()

handle = sql.connect("JobCentreData.db") # creating all of the tables in the database file to be populated
cursor = handle.cursor()
cursor.execute("CREATE TABLE DATA(CENTREID INT, LONG TEXT, LAT TEXT, POST TEXT, ADDRESS TEXT)")
cursor.execute("CREATE TABLE RECOMMEND4(CENTREID INT, USERID INT)")
cursor.execute("CREATE TABLE RATING4(CENTREID INT, RATING INT, COMMENT TEXT)")
handle.commit()
handle.close()

#fill table
getinfo()

