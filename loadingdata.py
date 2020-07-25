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

import NEAbackup as NEA # imported all functions from the main file

def loaddata():
    txts = ["Science.txt", "Agri.txt", "Arch.txt", "Business.txt", "Arts.txt", "Finance.txt", "Gov.txt", "Health.txt", "Hospit.txt", "Human.txt", "IT.txt", "Law.txt", "Manufact.txt", "Market.txt", "Transport.txt", "Edu.txt"] # array of all the different text files containing all job names in that field
    counttxt = 0
    alljobs = []
    fields = []
    jobid = 0
    for x in range(0, len(txts)):
        file = open(txts[counttxt]) # connecting to one file of the array above per iteration
        fieldjob = file.readlines() # reading every line in the file
        fieldname = fieldjob[0] # field name is the first line of the file
        fields.append(fieldname)
        a = 1
        aruntime = len(fieldjob)-1 # line count minus 1
        aruntime = aruntime/2 # halving the line count    this is done because each job has two lines worth of contents
        aruntime = int(aruntime)
        for x in range(0, aruntime):
            name = fieldjob[a] # job name is assigned as a variable of name from the array of lines
            url = fieldjob[a+1] # assigning a line as the variable url as it contains a link to information
            a = a+2
            jobid = jobid+1
            handle = sql.connect("RecommendDATA.db") # Inserting all of the data into the database to be used in the following function
            cursor = handle.cursor()
            cursor.execute("INSERT INTO JOBS VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (jobid, name, url, ".", ".", ".", ".", ".", fieldname, ".", ".", "0"))
            handle.commit()
            handle.close()
        counttxt = counttxt+1
    counts = -1 # starting at -1 to add at start of each iteration
    fieldlist=[]
    for x in range(0, len(fields)): # formattuing
        counts=counts+1
        item = fields[counts]
        item = item.rstrip()
        fieldlist.append(item)
    return fieldlist # returning an array of all the field names

def getskillslist():
    handle = sql.connect("RecommendDATA.db")
    cursor = handle.cursor()
    cursor.execute("SELECT JOBS.URL FROM JOBS WHERE JOBS.JOBID > 0") # getting all of the urls from the JOBS table
    URLlist = cursor.fetchall()
    handle.commit()
    handle.close()
    URLs=[]
    counts=0
    count = 1
    for p in range(0, len(URLlist)): # for each url in the list, formatting is done below
        link = URLlist[counts]
        link = str(link)
        link = link.replace(")", "")
        link = link.replace("(", "")
        link = link.replace("\"", "") # removing all of the specific characters from the string
        link = link.rstrip('\n')
        link = link.replace("'", "")
        link = link.replace(",", "")
        if link[len(link)-1] == 'n': # if the link has unwanted characters on the end of the string after formatting, this removes them
            link = link[:-2]
        counts=counts+1
        URLs.append(link)
    iterate = 0
    try:
        from bs4 import BeautifulSoup # two modules that allow access to a long string of the html contents of a website
        import requests # handles the requests to the website for data to be sent
    except:
        cont = True # placeholder
    for job in range(0, len(URLs)):
        websiteurl = URLs[iterate]
        response = requests.get(websiteurl) # request access from url
        soup = BeautifulSoup(response.content, "html.parser") # retrieve the html parser file
        soup.prettify() # used to clean the html
        mydivs = soup.findAll("div", {"class": "careerSummaryValue"}) # finding a specfifc element within the html document
        salary = re.sub('[^0-9]', '', str(mydivs)) # using re module to only include digits 0-9 in a string
        if salary == "": # all salaries are per year in dollars
            salary = 46000 # average salary of a working person in USD
        try:
            quallevel = soup.find("div", {"class": "careerSummaryTip"}).find('a') # finding the specific element that contains the qualification level required
        except:
            quallevel = soup.find("div", {"class": "careerSummaryTip"}) # some urls require some exceptions due to different layouts
        strquallevel = str(quallevel)
        quallevelfirst = strquallevel[167:495] # shortening the regions in the string
        fullstops = 0
        firsttwo = []
        loop = True
        for char in quallevelfirst:
            if loop == True:
                if char == "&":
                    fullstops=fullstops+1 # making an array that contains all of the valid characters
                elif fullstops == 1:
                        loop = False
                else:
                    firsttwo.append(char)
        stringoutput = ""
        for i in range(0, len(firsttwo)): # converting the array into a string
            a = firsttwo[i]
            stringoutput = stringoutput+a
        if stringoutput == "" or len(stringoutput) == 1:
            stringoutput = "none" #amount of work experience required
        try:
            keyskills = soup.find("div", {"class": "careerTopSkills"}).text # find the key skills info from the html file
            keyskills = "".join([s for s in keyskills.strip().splitlines(True) if s.strip("\r\n").strip()]) # strip all of the weird formatting from the element
            keyskills = keyskills.splitlines()
            #top skills, job specific
        except:
            keyskills = "none"
        try:
            educat = soup.find("div", {"class": "careerEducationContainer"}).find("script") # searching for element in html file
            educat = str(educat)
            educat = educat[600:1700] # shortening the region of the string
            educat = list(educat)
            x=0
            store = []
            num1="0"
            quallevellist=[]
            loop = 0
            while loop <= 5:
                cert1 = []
                x=x+100
                while educat[x] != "'":
                    cert1.append(educat[x])
                    x=x+1
                cert1 = ''.join(map(str, cert1)) # all formatting the element into desired string
                x=x+88
                num1=[]
                while educat[x] != ")":
                    num1.append(educat[x])
                    x=x+1
                num1 = ''.join(map(str, num1))
                if len(num1) > 5:
                    num1 = num1[len(num1)-5:len(num1)]
                quallevellist.append(cert1)
                store.append(cert1)
                store.append(num1)
                loop = loop+1
        except:
            education = "Bachelor" # education level
        description = soup.find("div", {"class": "careerSnapshotContainer"}).text
        description = str(description)
        description = description[42:300] # removing certain postitions of the string
        description = list(description)
        des = []
        loop = True
        for char in description:
            if loop == True:
                if char == ".":
                    des.append(char) # getting all the characters from the first sentence
                    loop = False
                else:
                    des.append(char)
        des = ''.join(map(str, des)) # formatted description of job
        employ = 0
        websiteurl = URLs[iterate]
        response = requests.get(websiteurl+"/outlook/") # new website url
        soup = BeautifulSoup(response.content, "html.parser") # retrieve the html document
        soup.prettify()
        employment = soup.find("div", {"class": "generalMainContentCol"}).find("script").text # get total employed in that professtion
        employment = employment[2000:2500]
        employment = re.sub("[^0-9]", "", employment) # getting all the numbers between char 2000 and 2500
        employ = str(employment[21:len(employment)])
        employ = list(employ)
        new_employ = []
        set_ = False
        for c in range(0, len(employ)): # appending all of the chars into the new array but only after the first 0, due to formatting of the elements in the html file
            if employ[c] == "0":
                set_ = True
                new_employ.append(employ[c])
            elif set_ == True:
                new_employ.append(employ[c])
        try:
            new_employ.remove(new_employ[0]) # removing first char in the array
        except:
            continue_ = True
        employ = str(new_employ) # casted back into a string
        handle = sql.connect("RecommendDATA.db") # put all of the data into the table to be used when a job is recommended
        cursor = handle.cursor()
        cursor.execute("UPDATE JOBS SET SKILLS = ?, QUALLEVEL = ?, DESCRIPTION = ?, SALARY = ?, WORKEXP = ?, EMPLOYEES = ? WHERE JOBID = ?;", (str(keyskills), str(store), des, salary, stringoutput, employ, count))
        handle.commit()
        count=count+1
        iterate = iterate+1

handle = sql.connect("RecommendDATA.db") # creating all of the tables in the database file to be populated by running the functions
cursor = handle.cursor()
cursor.execute("CREATE TABLE RANKINGS(UNI_ID INT, UNINAME TEXT, RANK TEXT)")
cursor.execute("CREATE TABLE UNIENTRY(UNI_ID INT, UNINAME TEXT, UCAS INT)")
cursor.execute("CREATE TABLE JOBS(JOBID INT, JOBNAME TEXT, URL TEXT, SKILLS TEXT, QUALLEVEL TEXT, WORKEXP TEXT, SALARY INT, DESCRIPTION TEXT, FIELD TEXT, COUNT INT, EMPLOYEES INT, IDLE INT)")
cursor.execute("CREATE TABLE USERS(USERID TEXT, NAME TEXT, PASSWORD TEXT, QUALLEVEL TEXT, SKILL1 TEXT, SKILL2 TEXT, SKILL3 TEXT, FIELDS TEXT, CURRENTJOB TEXT)")
cursor.execute("CREATE TABLE RATINGS2(UNIID INT, RATING INT, COMMENT TEXT)")
cursor.execute("CREATE TABLE WEBLIST(WEBID INT, WEBURL TEXT)")
cursor.execute("CREATE TABLE RECOMMEND(JOBID, USERID)")
cursor.execute("CREATE TABLE RECOMMEND2(UNIID, USERID)")
cursor.execute("CREATE TABLE USER_RECOMMENDATIONS(JOBNAME TEXT, DESCRIPTION TEXT, FIELD TEXT)")
handle.commit()
handle.close()
uni = NEA.uni() # calling class creation in main file
uni.getucaspoints()
fieldlist = loaddata() # calling functions to populate tables
getskillslist()
