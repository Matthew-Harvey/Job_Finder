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
 
import in_built as built # getting all in builts methods imported to use

class HoverButton(tk.Button): # creating a new variation of the HoverButton that inherits the tkinter regular button
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw) # inheriting the regualar attributes of tk.Buttoon
        self.defaultBackground = self["background"] # the default colour of the button is set by "background"
        self.bind("<Enter>", self.on_enter) 
        self.bind("<Leave>", self.on_leave) # binding new events by mouse hover

    def on_enter(self, e):
        self['background'] = self['activebackground'] # when active hovering it sets to a new activebackground

    def on_leave(self, e):
        self['background'] = self.defaultBackground # when inactive it reverts back to original state

class both: # contains functions / classes used by various sections
    class home:
        def __init__(self, IDinsert):
            self.__IDinsert = IDinsert # making the identifier a private attribute
            self.__tab1 = ttk.Frame(tabcontrol) # creating a new tkinter tab
            both.home.make(self)  # calling to create the main home GUI
        
        def make(self): # holds all components of the main GUI
            tabcontrol.add(self.__tab1, text="HOME")
            tabcontrol.select(self.__tab1)
            HoverButton(self.__tab1, height = 5, width = 70 , activebackground='grey', fg="white", bg="red", text="UNIVERSITY", command = lambda: [both.closetab(self.__tab1), uni.unimenu(self.__IDinsert)]).grid(row=1) # redirects to university section on click of button
            HoverButton(self.__tab1, height = 5, width = 70 , activebackground='grey', fg="white", bg="blue", text="JOBS", command = lambda: [both.closetab(self.__tab1), job.mainmenu(self.__IDinsert)]).grid(row=2) # redirects to job section on click of button
            HoverButton(self.__tab1, height = 5, width = 70 , activebackground='grey', fg="black", bg="white", text="SCHOOLS", command = lambda: [both.closetab(self.__tab1), schools.home(self, self.__IDinsert)]).grid(row=3) # redirects to school section on click of button
            tk.Label(self.__tab1, text=" ").grid(row=4)
            tk.Label(self.__tab1, text=" ").grid(row=5) # making gaps for seperation of attributes, for clarity in the interface
            string = "Username = '" + self.__IDinsert + "'"
            tk.Label(self.__tab1, font="Verdana 15", text= string).grid(row=6) # label showing the user the username of who is logged in 
            HoverButton(self.__tab1, height = 3, width = 70 , activebackground='grey', fg="White", bg="Black", text="Account Details", command = lambda: [both.closetab(self.__tab1), both.changelogin(self.__IDinsert)]).grid(row=7) # display user stats home upon clicking atribute and closing the previous tab
            tk.Label(self.__tab1, text=" ").grid(row=8)
            HoverButton(self.__tab1, height = 3, width = 70 , activebackground='grey', fg="black", bg="Light Green", text="Log Out", command = lambda: [both.closetab(self.__tab1), both.loginhome()]).grid(row=9) # back to no login home upon click of attribute

    class loginhome:
        def __init__(self):
            self.__tab0 = ttk.Frame(tabcontrol)
            both.loginhome.made(self) # calling made sub-routine to make the login page GUI, passing self variables
        
        def made(self):
            tabcontrol.add(self.__tab0, text="HOME")
            tabcontrol.select(self.__tab0) # selects the new tab for the user
            tk.Label(self.__tab0, text="                   ", font="Verdana 1").grid(row=1, column=1)
            tk.Label(self.__tab0, text="                   ", font="Verdana 1").grid(row=2, column=2) # formatting of the UI by using spacing with blank labels
            tk.Label(self.__tab0, text="LOGIN:", font="Verdana 22 bold italic", fg="Dark Grey").grid(row=5+1, columnspan=7)
            tk.Label(self.__tab0, text="                   ", font="Verdana 18").grid(row=7, column=2)
            IDENTentry = tk.Entry(self.__tab0, font="Ariel 13")
            IDENTentry.insert(END, "ID") # making a entrybox with it pre-filled with "ID"
            IDENTentry.grid(row=7+1, columnspan=7)
            Passwordentry = tk.Entry(self.__tab0, font="Ariel 13", show="*") # making all inputs into the entrybox show as ***** etc.
            Passwordentry.insert(END, "Password") # making a entrybox with it pre-filled with "Password"
            Passwordentry.grid(row=9+1, columnspan=7)
            tk.Label(self.__tab0, text="                   ", font="Verdana 18").grid(row=11, column=2)
            attempts = 0
            HoverButton(self.__tab0, height=3, width=70, activebackground='Light Grey', fg="White", bg="Black", text="ENTER", command= lambda: both.login(attempts, IDENTentry, Passwordentry).main(self.__tab0)).grid(row=13+1, columnspan=7) # button to redirect to the function "login.main" with the appropriate parameters of username and password
            tk.Label(self.__tab0, text="                   ", font="Verdana 18").grid(row=15, column=2)
            tk.Label(self.__tab0, text="NEW USER:", font="Verdana 22 bold italic", fg="Dark Grey").grid(row=15+1, columnspan=7)
            tk.Label(self.__tab0, text="                   ", font="Verdana 18").grid(row=17, column=2)
            IDentry = tk.Entry(self.__tab0, font="Ariel 13")
            IDentry.insert(END, "ID") # making the default entry into the IDentry entrybox "ID"
            IDentry.grid(row=19+1, columnspan=7)
            tk.Label(self.__tab0, text="                   ", font="Verdana 18").grid(row=27, column=3)
            HoverButton(self.__tab0, height=3, width=70, activebackground='Light Grey', fg="White", bg="Black", text="ENTER", command = lambda: both.user1(IDentry, self.__tab0)).grid(row=28, columnspan=7) # button to redirect to the function "user1" with the appropriate parameters of the username and tkinter tab

    def closetab(self, result_tab):
        result_tab.destroy() # closing any tkinter tab that gets passed to it as a variable

    class hash_password:
        def __init__(self, password): # passed password as the only variable
            self.__password = password # password made private 
            self.__salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii') # creating the salt to combine with the hashed result from a random 60 length string in ascii encoding

        def hashed(self):
            self.__pwdhash = hashlib.pbkdf2_hmac('sha512', self.__password.encode('utf-8'), self.__salt, 100000) # encrypting in SHA512 with the salt and encoding in utf-8 (100000 is the amount of bytes produced)
            self.__pwdhash = binascii.hexlify(self.__pwdhash) # translating the binary into equivilant hexidecimal 
            return (self.__salt + self.__pwdhash).decode('ascii') # returning a decoded into ascii combination of the hash and salt

    class verify_password:
        def __init__(self, stored_password, provided_password):
            self.__salt = stored_password[:64] # seperating the salt and hash from the return statement in the hashed function
            self.__stored_password = stored_password[64:]
            self.__provided_password = provided_password # making given password private

        def verify(self):
            self.__pwdhash = hashlib.pbkdf2_hmac('sha512', self.__provided_password.encode('utf-8'), self.__salt.encode('ascii'), 100000) # same operation as done in hashed function to compare results
            self.__pwdhash = binascii.hexlify(self.__pwdhash).decode('ascii')
            return self.__pwdhash == self.__stored_password # this returns either True or False, True if they are identical, else False

    class login:
        def __init__(self, attempts, IDENTentry, Passwordentry):
            IDENT_insert = IDENTentry.get() # retrieval of the ID data from the users inputs when trying to login
            PIN_insert = Passwordentry.get() # retrieval of the Password data from the users inputs when trying to login
            self.__IDENT_insert = IDENT_insert
            self.__PIN_insert = PIN_insert # making both new attributes private

        def main(self, tab1): # recieving a tkinter tab as a parameter
            self.__tab1 = tab1 # making the tab private
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            cursor.execute("SELECT USERS.USERID FROM USERS") # using sqlite3 to get all userids from the database
            self.__ids = cursor.fetchall()
            handle.commit()
            idsclean = []
            for x in range(0, len(self.__ids)): # iterating through the tuple to extract each id
                a = str(self.__ids[x])
                b = a.strip('(),/\'') # removing formatting of the ids from a tuple to an array, done by stripping the extra characters as a string
                idsclean.append(b)
            ids = idsclean
            k = 0
            for x in range(0, len(ids)): # getting every id from the array
                if ids[x] == self.__IDENT_insert: # if id is equal to the given username
                    cursor.execute("SELECT USERS.PASSWORD FROM USERS WHERE USERS.USERID = ?", (self.__IDENT_insert,))
                    PINreceived = cursor.fetchall() # retrieval of the password from the given username
                    handle.commit()
                    PINreceived = PINreceived[0]
                    PINreceived = str(PINreceived) # formatting of the password from a tuple to a string
                    PINreceived = PINreceived.strip("/'(),'") # using .strip to remove all unwanted characters
                    TrueorFalse = both.verify_password(PINreceived, self.__PIN_insert).verify() # running to see if the passwords are identical
                    if TrueorFalse == True:
                        both.home(self.__IDENT_insert) # this goes to the logged in homepage
                        k = 8
            self.__tab1.destroy()
            if k != 8:
                errorlogin = ttk.Frame(tabcontrol) # creating a tab to show the user that the inputs were incorrect
                tabcontrol.add(errorlogin, text="INVALID")
                tk.Label(errorlogin, text="ID or  Password is incorrect", font="Ariel 15 bold italic", fg="blue").grid(row=1)
                HoverButton(errorlogin, text="Back to Main Menu", activebackground='blue', fg="white", bg="black", command= lambda: [both.closetab(errorlogin), both.loginhome()]).grid(row=2) # redirecting to the login home if the user presses the button with the tab being destoryed

    class changelogin:
        def __init__(self, IDENT_insert):
            #give option to change details (other than id/password)
            tab4 = ttk.Frame(tabcontrol)
            tabcontrol.add(tab4, text="Step 2")
            tabcontrol.select(tab4) # selecting the new tkinter tab
            ID_insert = IDENT_insert
            HoverButton(tab4, height=2, width=30, font="Verdana 20", activebackground='Light Yellow', fg="Black", bg="Yellow", text=" edit your data ", command = lambda: both.changingdata(ID_insert, tab4)).grid(row=2) # redirect for the function, for the user to change any information
            tk.Label(tab4, text=" ").grid(row=1)
            tk.Label(tab4, text=" ").grid(row=3) # formatting with blank labels
            tk.Label(tab4, text=" ").grid(row=10)
            HoverButton(tab4, height=2, width=30, font="Verdana 20", activebackground='Light Grey', fg="white", bg="Dark Grey", text=" Previous Recommendations ", command = lambda: [both.viewing_all(ID_insert), both.closetab(tab4)]).grid(row=6) # redirecting to a function that handles all of the recommendations processed 
            HoverButton(tab4, text="Back to Main Menu", activebackground='blue', fg="white", bg="black", command= lambda: [both.closetab(tab4), both.home(IDENT_insert)]).grid(row=11) # back to logged in home button

    def viewing_all(self, ID_insert): # creating function with a parameter of the username
        tab4 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab4, text="Recommendations")
        tabcontrol.select(tab4) # selction and creation of a new tkinter tab
        try: # using try and except as the user may or may not of had any recommendations for each section
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            cursor.execute("SELECT JOBID FROM RECOMMEND WHERE USERID = ? AND JOBID != ?;", (ID_insert, 0))
            userinfo = cursor.fetchall() # using userid to get any job ids the user is linked to
            handle.commit()
            handle.close()
            nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] # array of all single digit numbers
            newarr = [] # new array
            for string in userinfo:
                string = str(string) # casting tuple to a string
                newstr = ""
                for char in string:
                    try:
                        char = int(char) # extracting all of the ids from tuple form to within an array
                    except:
                        char = char
                    for num in nums:
                        if num == char: # if a character is a number
                            char = str(char)
                            newstr = newstr + char # add the char to a string
                newstr = int(newstr) # make each id an integer
                newarr.append(newstr)
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            allnames = []
            for integer in newarr: # for every id
                cursor.execute("SELECT JOBNAME FROM JOBS WHERE JOBID = ? AND JOBID > ?;", (integer, "0"))
                userinfo = cursor.fetchall()
                handle.commit() # getting a jobname that corresponds to each id
                userinfo = str(userinfo)
                userinfo = userinfo[3:len(userinfo)-6] # formatting into string from tuple
                if userinfo not in allnames:
                    allnames.append(userinfo) # removing duplicate names in array
            handle.close()
            varc = StringVar()
            varc.set(allnames[random.randint(0, len(allnames)-1)]) # creating a option menu with a set random jobname
            OptionMenu(tab4 , varc, *allnames).grid(row=3, columnspan=7)
            tk.Label(tab4, text="Job Recommendations", font="Ariel 15", fg="Blue").grid(row=2, columnspan=7)
            HoverButton(tab4, activebackground='blue', fg="white", bg="black", text="Enter", command = lambda: [both.getvar(varc, ID_insert), both.closetab(tab4)]).grid(row=4, columnspan=7) # button to proceed to the selected jobpage
        except:
            cont = True # placeholder
        tk.Label(tab4, text="    ", font="Ariel 10", fg="White").grid(row=5) # spacing between sections
        try:
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            cursor.execute("SELECT UNIID FROM RECOMMEND2 WHERE USERID = ? AND USERID > ?;", (ID_insert, "0"))
            userinfo = cursor.fetchall() # getting all the university ids where the username matches
            handle.commit()
            handle.close()
            nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            newarr = []
            for string in userinfo:
                string = str(string)
                newstr = ""
                for char in string:
                    try:
                        char = int(char) # same process as above to convert the tuple of ids into an array of ids
                    except:
                        char = char
                    for num in nums: 
                        if num == char:
                            char = str(char)
                            newstr = newstr + char
                newstr = int(newstr)
                newarr.append(newstr)
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            allnames = []
            for integer in newarr:
                cursor.execute("SELECT UNINAME FROM RANKINGS WHERE UNI_ID = ? AND UNI_ID > ?;", (integer, "0"))
                userinfo = cursor.fetchall()
                handle.commit() # getting a university name from the coresponding id and then formatting into string
                userinfo = str(userinfo)
                userinfo = userinfo[3:len(userinfo)-4]
                if userinfo not in allnames: # making no duplicate names in the array
                    allnames.append(userinfo)
            handle.close()
            vara = StringVar()
            vara.set(allnames[random.randint(0, len(allnames)-1)])
            OptionMenu(tab4 , vara, *allnames).grid(row=7, columnspan=7) # setting an optionmenu with a set random university name
            tk.Label(tab4, text="University Recommendations", font="Ariel 15", fg="Red").grid(row=6, columnspan=7)
            HoverButton(tab4, activebackground='blue', fg="white", bg="black", text="Enter", command = lambda: [both.getvar2(vara, ID_insert), both.closetab(tab4)]).grid(row=8, columnspan=7) # directs to the selected university page while closing the tkinter tab
            tk.Label(tab4, text="    ", font="Ariel 10", fg="White").grid(row=8)
            tk.Label(tab4, text="    ", font="Ariel 10", fg="White").grid(row=4)
        except:
            cont = True # placeholder
        try:
            handle = sql.connect("JobCentreData.db")
            cursor = handle.cursor()
            cursor.execute("SELECT CENTREID FROM RECOMMEND4 WHERE USERID = ? AND CENTREID > ?", (ID_insert, 0))
            centreids = cursor.fetchall() # using userid to retrieve any associated centres (the ids)
            alladdress = []
            for ids in centreids:
                ids = str(ids)
                ids = ids[1:len(ids)-2] # formatting the ids into integers
                ids = int(ids)
                handle = sql.connect("JobCentreData.db")
                cursor = handle.cursor()
                cursor.execute("SELECT ADDRESS FROM DATA WHERE CENTREID = ? AND CENTREID > ?", (ids, 0))
                add = cursor.fetchall() # getting address from the centreid retrieved eariler
                handle.commit()
                handle.close()
                add = str(add)
                add = add[3:len(add)-4] # formatting address by removing first 3 and last 4 characters
                if add not in alladdress: # not permitting duplicates
                    alladdress.append(add)
            varf = StringVar()
            varf.set(alladdress[random.randint(0, len(alladdress)-1)]) # option menu containing all of the centres recommended for that user
            tk.Label(tab4, text="Job Centre Recommendations", font="Ariel 15", fg="Green").grid(row=10, columnspan=7)
            OptionMenu(tab4 , varf, *alladdress).grid(row=11, columnspan=7)
            tk.Label(tab4, text="    ", font="Ariel 10", fg="White").grid(row=9)
        except:
            cont = True # placeholder
        try:
            handle = sql.connect("Schools.db")
            cursor = handle.cursor()
            cursor.execute("SELECT SCHOOLID FROM RECOMMEND3 WHERE USERID = ? AND USERID > ?", (ID_insert, 0))
            schools = cursor.fetchall() # retrieving school ids that have been recommended to that user
            handle.commit()
            handle.close()
            allschools = []
            display = []
            for school in schools:
                school = str(school)
                school = school[1:len(school)-2] # making each piece of data into a string from a tuple
                school = int(school)
                handle = sql.connect("Schools.db")
                cursor = handle.cursor()
                cursor.execute("SELECT NAME FROM DATA WHERE SCHOOLID = ? AND SCHOOLID > ?", (school, 0))
                names = cursor.fetchall() # retrieving the names of school from the school id
                handle.commit()
                handle.close()
                names = str(names)
                names = names[3:len(names)-4] # formatting the name to remove unwanted characters
                if names[0] == '"':
                    app = True
                    names = names[1:]
                else:
                    app = False
                if names not in allschools:
                    allschools.append(names) # gathering all the information into arrays
                    allschools.append(app)
                    display.append(names)
            varn = StringVar()
            varn.set(display[random.randint(0, len(display)-1)]) # making an option menu for user to select which job they want to view, setting a random name as default
            tk.Label(tab4, text="School Recommendations", font="Ariel 15", fg="Dark Grey").grid(row=14, columnspan=7)
            OptionMenu(tab4, varn, *display).grid(row=15, columnspan=7)
            HoverButton(tab4, activebackground='blue', fg="white", bg="black", text="Enter", command = lambda: [both.getvar3(tab4, varn, ID_insert), both.closetab(tab4)]).grid(row=16, columnspan=7) # run job specific page
            tk.Label(tab4, text="    ", font="Ariel 10", fg="White").grid(row=16)
            tk.Label(tab4, text="    ", font="Ariel 10", fg="White").grid(row=13) # blank labels for spacing purposes
        except:
            cont = True # placeholder
        tab1 = ttk.Frame(tabcontrol)
        tk.Label(tab4, text="    ", font="Ariel 10", fg="White").grid(row=25) # blank labels for spacing purposes
        tk.Label(tab4, text="    ", font="Ariel 10", fg="White").grid(row=24)
        HoverButton(tab4, activebackground='blue', fg="white", bg="black", text="Back", command = lambda: [both.changelogin(ID_insert), both.closetab(tab4)]).grid(row=26, columnspan=7) # return to the accoint details home

    def getvar(self, var, ID_insert):
        var = var.get()
        job.display(var, 0, ID_insert) # function that takes an input and interprets it, then proceeds to run the input to create a job page

    def getvar2(self, var, ID_insert):
        var = var.get()
        uni.display_uni(var, ID_insert) # function that takes an input and interprets it, then proceeds to run the input to create a university page

    def getvar3(self, tab, var, ID_insert):
        var = var.get()
        schools.run2(self, tab, var, ID_insert) # function that takes an input and interprets it, then proceeds to run the input to create a school page

    def changingdata(self, ID_insert, tab4):
        tab4.destroy()
        tab4 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab4, text="Update Info")
        tabcontrol.select(tab4)
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT USERID, NAME, QUALLEVEL, SKILL1, SKILL2, SKILL3, CURRENTJOB FROM USERS WHERE USERID = ? AND USERID > ?;", (ID_insert, "0"))
        userinfo = cursor.fetchall() # get all associated data with the user that is inputted on the second page when creating a new account
        handle.commit()
        handle.close()
        for h in range(0, len(userinfo)):
            punctuation = """!"#$%&'()*+/:;<=>?@[\\]^_`{|}~"""
            user_info = ""
            string = str(userinfo[h]) # formatting all pieces of data in the tuple received from the database
            for e in string:
                if e not in punctuation:
                    user_info += e
        user_info = user_info.split(",") # user info is an array containing each part of the users data seperately eg. [name, qual, skill1, skill2, skill3, job]
        tk.Label(tab4, text="Name:").grid(row=1)
        ident = tk.Entry(tab4)
        ident.insert(0,user_info[1]) # setting name default from what was in the database, in column name (in the row of ID_insert matching userid column)
        ident.grid(row=1, column=1)
        tk.Label(tab4, text="Qual:").grid(row=2)
        vare = StringVar()
        vare.set(user_info[2]) # setting qual-level default from what was in the database, in column quallevel
        choices = ["< High School Diploma", "High School Diploma", "Master", "Bachelor", "Associate", "Some College", "Doctoral Degree", "Vocational Certificate"]
        OptionMenu(tab4 , vare, *choices).grid(row=2, column=1)
        tk.Label(tab4, text="SKILL:").grid(row=3)
        skilldoc = open("keyskills.txt")
        skill_list = []
        read = "/n"
        while read != "":
            read = skilldoc.readline() # open the skill list file to read and then gather each line as a skill, then make an array full of all the skills users can choose from
            read = read.rstrip()
            skill_list.append(read)
        skill_list.sort()
        skill_list.remove("")
        skilldoc.close()
        vara = StringVar()
        vara.set(user_info[3]) # setting skill1 default from what was in the database, in column skill1
        varb = StringVar()
        varb.set(user_info[4]) # setting skill2 default from what was in the database, in column skill2
        varc = StringVar()
        varc.set(user_info[5]) # setting skill2 default from what was in the database, in column skill3
        OptionMenu(tab4 , vara, *skill_list).grid(row=3, column=1)
        OptionMenu(tab4 , varb, *skill_list).grid(row=4, column=1) # creating the option menus themselves
        OptionMenu(tab4 , varc, *skill_list).grid(row=5, column=1)
        tk.Label(tab4, text="Current Job:").grid(row=6)
        current = tk.Entry(tab4)
        current.insert(0,user_info[6]) # setting default job as what is currently in the database in the current job column
        current.grid(row=6, column=1)
        HoverButton(tab4, activebackground='blue', fg="white", bg="black", text="Commit Changes", command = lambda: both.updatechanges(vara, varb, varc, vare, ID_insert, ident, current, tab4)).grid(row=7) # confirming any changes to then update in the database

    def updatechanges(self, vara, varb, varc, vare, ID_insert, ident, current, tab4):
        skill1 = vara.get()
        skill2 = varb.get() # recieving as parameters all the option menu data from above function named changingdata
        skill3 = varc.get()
        vare = vare.get()
        name = ident.get()
        current = current.get()
        handle = sql.connect("RecommendDATA.db") # updating the appropriate columns in the database with the data received
        cursor = handle.cursor()
        cursor.execute("UPDATE USERS SET QUALLEVEL = ?, NAME = ?, CURRENTJOB = ?, SKILL1 = ?, SKILL2 = ?, SKILL3 = ? WHERE USERID = ?", (vare, name, current, skill1, skill2, skill3, ID_insert))
        handle.commit()
        handle.close()
        tab4.destroy()
        both.changelogin(ID_insert) # going back to the user details homepage
            
    def loguser(self, ID_insert, tab6, nameentry, tkvar, abvar, advar, acvar, currententry, Password, IDentry, tab1, choices):
        username_insert = nameentry.get()
        quallevel_insert = tkvar.get()
        skill1_insert = abvar.get()
        skill2_insert = acvar.get() # getting all of the inputted data from the previous page
        skill3_insert = advar.get()
        current_insert = currententry.get()
        Password_insert = Password.get()
        # conditions of passwords
        while len(Password_insert) < 6:
            Password_insert = Password_insert+random.randint(0, 9) # adding numbers onto password if not long enough
        Password_insert = str(Password_insert)
        Password_insert1 = both.hash_password(Password_insert).hashed()
        if username_insert == "":
            username_insert = "NULL"
        if current_insert == "":
            current_insert = "N"
        tab6.destroy()
        handle = sql.connect("RecommendDATA.db") # inserting all given data into the database as a user row
        cursor = handle.cursor()
        cursor.execute("INSERT INTO USERS VALUES(?,?,?,?,?,?,?,?,?)", (ID_insert, username_insert, Password_insert1, quallevel_insert, skill1_insert, skill2_insert, skill3_insert, ".", current_insert))
        handle.commit()
        handle.close()
        tab4 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab4, text="REMEMBER THIS") # creating a remember page so users dont forget what they entered
        tabcontrol.select(tab4)
        tk.Label(tab4, font="Verdana 15", fg="Black", text="Remember these to login in next time to avoid ").grid(row=1, columnspan=7)
        tk.Label(tab4, font="Verdana 15", fg="Black", text="re-completing the questions.").grid(row=2, columnspan=7)
        tk.Label(tab4, text=" ").grid(row=3, column=1)
        tk.Label(tab4, text=" ").grid(row=6, column=1) # blank labels for spacing purposes
        tk.Label(tab4, text=" ").grid(row=9, column=1)
        tk.Label(tab4, text=" ").grid(row=10, column=1)
        tk.Label(tab4, text="ID:", font="Verdana 14", fg="Grey").grid(row=4, column=1)
        tk.Label(tab4, text=ID_insert, font="Ariel 14 italic", fg="Black").grid(row=5, column=2)
        tk.Label(tab4, text="Password:", font="Verdana 14", fg="Grey").grid(row=7, column=1)
        counted = 0
        nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        string__ = ""
        for char in Password_insert:
            if char in nums:
                string__ = string__ + char # creating a string that will only show numbers to the user in the case they have been added on 
            else:
                string__ = string__ + "*"
        displaypass = string__
        tk.Label(tab4, text=displaypass, font="Ariel 14 italic", fg="Black").grid(row=9, column=2)
        HoverButton(tab4, activebackground='Grey', fg="white", bg="Blue", text="Home", command= lambda: [both.home(ID_insert), both.closetab(tab4)]).grid(row=11, column=1) # continue to logged in homepage

    def user1(self, IDentry, tab1):
        choices = ["< High School Diploma", "High School Diploma", "Master", "Bachelor", "Associate", "Some College", "Doctoral Degree", "Vocational Certificate"]
        z = False
        ID_insert = IDentry.get()
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT USERID FROM USERS") # getting all of the current ids that have been created
        allids = cursor.fetchall()
        handle.commit()
        handle.close()
        idsclean=[]
        tab1.destroy()
        for j in range(0, len(allids)):
            #call for new id if already exists, new tab with back button to main menu.
            a = str(allids[j])
            b = a.strip('(),') # formatting into an array
            idsclean.append(b)
        nodup = 0
        for r in range(0, len(idsclean)):
            idsclean[r] = idsclean[r][1:len(idsclean[r])-1]
            if idsclean[r] == ID_insert:
                z = True
                nodup = nodup+1 ## if ids match from already in database, display an error tab and ask for re-entry of a new name
                if nodup == 1:
                    error = ttk.Frame(tabcontrol)
                    tabcontrol.add(error, text="Id taken")
                    tabcontrol.select(error)
                    tk.Label(error, text="ID is already taken...").grid(row=1)
                    HoverButton(error, activebackground='blue', fg="white", bg="black", text="Back to Main Menu", command = lambda: [both.closetab(error), both.loginhome()]).grid(row=2)
        if z == False:
            tab6 = ttk.Frame(tabcontrol)
            tabcontrol.add(tab6, text="CREATE USER")
            tabcontrol.select(tab6)
            tk.Label(tab6, text="Name: ", font="Verdana 14", fg="Black").grid(row=2, column=1) # if ids dont match, a new user can be made and this is the creation of the tkinter tab for user entry of relevant information
            nameentry = tk.Entry(tab6, bg="Light Grey", fg="Black", font="Ariel 15")
            nameentry.grid(row=2, column=2)
            tkvar = StringVar()
            tkvar.set(choices[random.randint(0, len(choices)-1)])
            tk.Label(tab6, text="Highest Qual-level:", font="Verdana 14", fg="Black").grid(row=4, column=1)
            tk.OptionMenu(tab6 , tkvar, *choices).grid(row=4, column=2)
            skilldoc = open("keyskills.txt")
            skill_list = []
            read = "/n"
            while read != "":
                read = skilldoc.readline() # getting all of the possible user skills in an array and then put into option menus
                read = read.rstrip()
                skill_list.append(read)
            skill_list.sort()
            skill_list.remove("")
            abvar = StringVar()
            set1 = skill_list[random.randint(0, len(skill_list)-1)] # randomly assign a skill as default
            skill_list_temp = skill_list
            skill_list_temp.remove(set1)
            abvar.set(set1)
            acvar = StringVar()
            set2 = skill_list_temp[random.randint(0, len(skill_list_temp)-1)] # randomly assign a skill as default
            skill_list_temp.remove(set2)
            acvar.set(set2)
            advar = StringVar()
            set3 = skill_list_temp[random.randint(0, len(skill_list_temp)-1)] # randomly assign a skill as default
            advar.set(set3)
            tk.Label(tab6, text="Applicable Skills:", font="Verdana 14", fg="Black").grid(row=6, column=1)
            OptionMenu(tab6 , abvar, *skill_list).grid(row=6, column=2)
            OptionMenu(tab6 , acvar, *skill_list).grid(row=7, column=2) # creating option menus
            OptionMenu(tab6 , advar, *skill_list).grid(row=8, column=2)
            tk.Label(tab6, text="Current Job:", font="Verdana 14", fg="Black").grid(row=11, column=1)
            currententry = tk.Entry(tab6, bg="Light Grey", fg="Black", font="Ariel 15")
            currententry.grid(row=11, column=2)
            tk.Label(tab6, text="Password:", font="Verdana 14", fg="Black").grid(row=13, column=1)
            Password = tk.Entry(tab6, bg="Light Grey", fg="Black", font="Ariel 15", show="*") # only showing inputs as * for privacy reasons
            Password.grid(row=13, column=2)
            tab1 = ttk.Frame(tabcontrol)
            HoverButton(tab6, activebackground='blue', fg="white", bg="black", text="Continue", command= lambda: both.loguser(ID_insert, tab6, nameentry, tkvar, abvar, acvar, advar, currententry, Password, IDentry, tab1, choices)).grid(row=16, column=2) # update users table and proceed to logged in homepage
            HoverButton(tab6, activebackground='black', fg="white", bg="blue", text="Home", command = lambda: [both.closetab(tab1), both.loginhome(), both.closetab(tab6)]).grid(row=16, column=1) # back to not logged in homepage
            tk.Label(tab6, text=" ", font="Verdana 16", fg="Black").grid(row=3, column=1)
            tk.Label(tab6, text=" ", font="Verdana 16", fg="Black").grid(row=5, column=1)
            tk.Label(tab6, text=" ", font="Verdana 16", fg="Black").grid(row=10, column=1)
            tk.Label(tab6, text=" ", font="Verdana 16", fg="Black").grid(row=12, column=1) # blank labels for spacing purposes
            tk.Label(tab6, text=" ", font="Verdana 16", fg="Black").grid(row=14, column=1)
            tk.Label(tab6, text=" ", font="Verdana 16", fg="Black").grid(row=15, column=1)
            tk.Label(tab6, text=" ", font="Verdana 16", fg="Black").grid(row=1, column=1)

#
#
#
#

class uni: # creating a class for all functions to classify each name
    def unimenu(self, IDinsert): 
        attempts = 0
        uniorjob = True
        tab0 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab0, text="Uni Menu") # creating new menu that contains all of the buttons and entrys for each process by linking it on confirmation buttons
        tabcontrol.select(tab0)
        tk.Label(tab0, fg="red", text="University Research Tool", font="Verdana 29").grid(row=2+1, columnspan=7)
        HoverButton(tab0, activebackground='red', fg="white", bg="black", text="Overall Rankings", command = lambda: [both.closetab(tab0), uni.overallranking(IDinsert)]).grid(row=28)
        tk.Label(tab0, text=" ").grid(row=5+1)
        tk.Label(tab0, text=" ").grid(row=4+1)
        tk.Label(tab0, text= "SEARCH UNI:", font= "Verdana 12 bold italic", fg="Black").grid(row=6+1)
        entrybox = tk.Entry(tab0, font="Ariel 12")
        entrybox.insert(END, "University Name") # show university name to the user initally so they know what to enter in this entry box
        entrybox.grid(row=7+1, column=1)
        HoverButton(tab0, activebackground='red', fg="white", bg="black", text="ENTER", command = lambda: uni.searchbyuni(entrybox, tab0, IDinsert)).grid(row=8+1, column=1)
        HoverButton(tab0, activebackground='red', fg="white", bg="black", text="Subject Search", command = lambda: [both.closetab(tab0), uni.searchbysub(IDinsert)]).grid(row=28, column=2)
        HoverButton(tab0, activebackground='red', fg="white", bg="black", text="Most Popular", command = lambda: [both.closetab(tab0), uni.searchbyviews(IDinsert)]).grid(row=28, column=1) # all buttons that link to processes described in the text of each button
        HoverButton(tab0, activebackground='red', fg="white", bg="black", text="Highly Rated", command = lambda: [both.closetab(tab0), uni.rating(IDinsert)]).grid(row=8, column=2)
        tk.Label(tab0, text=" ").grid(row=9+1)
        HoverButton(tab0, width=70, height=5, activebackground='black', fg="white", bg="red", text="Find Reccomendations", command = lambda: uni.uni_quals(IDinsert, tab0)).grid(row=32, columnspan=7)
        tk.Label(tab0, text = " ").grid(row=30+1) # blank labels for spacing purposes
        tk.Label(tab0, text = " ").grid(row=35+1)
        HoverButton(tab0, width=70, height=5, activebackground='black', fg="white", bg="blue", text="Home", command = lambda: [both.closetab(tab0), both.home(IDinsert)]).grid(row=38, columnspan=7) # back to the logged in home

    def rating(self, IDinsert):
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        averages = []
        averages2 = []
        for t in range(0, 135):
            cursor.execute("SELECT RATING FROM RATINGS2 WHERE UNIID = ? AND UNIID != ?", (t, "")) # get all of the ratings for each uni in the table
            IDS = cursor.fetchall()
            IDS = str(IDS)
            IDS = IDS.split('(')
            allids = []
            for ids in IDS:
                ids = re.sub('[^0-9]', '', str(ids)) # formatting the ids into an array of digits as each rating is from 1-5
                if ids == "":
                    cont = True
                else:
                    allids.append(ids)
            if allids == []:
                averages.append(3)
                averages2.append(3) # if no ratings are present for a university choose 3 as it is central in the rating system
            else:
                total = 0
                for num in allids:
                    total = total + int(num)
                average = total / len(allids) # getting the average rating by using the total score and dividing by the amount of ratings
                averages.append(average)
                averages2.append(average)
        averages.sort()
        names = []
        for c in range(1, 5):
            for y in range(0, len(averages2)):
                if averages[len(averages)-c] == averages2[y]: # getting the highest average ratings and finding the positions where they are in the array
                    if y not in names:
                        names.append(y)
        while len(names) > 5:
            names.remove(names[len(names)-1])
        for _id in names:
            _id = int(_id)
            cursor.execute("SELECT UNINAME FROM UNIENTRY WHERE UNI_ID = ? AND UNI_ID != ?", (_id, "")) # getting the university name from the university id (which is identical to the postition in the array)
            string = cursor.fetchall()
            string = str(string)
            string = string[3:len(string)-4] # converting a tuple to a string
            uni.display_uni(string, IDinsert) # giving the user the appropriate university name sorted by rating
        handle.commit()
        handle.close()

    def searchbyviews(self, ID_insert):
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor() 
        cursor.execute("SELECT UNIID FROM RECOMMEND2") # receive all of the university ids that have a recommendation with a university
        IDS = cursor.fetchall()
        handle.commit()
        handle.close()
        IDS_array = []
        for t in range(0, len(IDS)):
            IDS[t] = str(IDS[t])
            IDS[t] = re.sub('[^0-9]', '', IDS[t]) # formatting into an array from a tuple
            IDS_array.append(IDS[t])
        IDS = IDS_array
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        counts = []
        counts2 = []
        for t in range(0, len(IDS)):
            num = 0
            for s in range(0, len(IDS)): # getting the counts of how many an id appears
                if IDS[t] == IDS[s]:
                    num = num + 1
            counts.append(num)
            counts2.append(num)
        counts.sort()
        ids = []
        for x in range(1, len(counts)-1):
            for y in range(0, len(counts2)):
                if counts2[y] == counts[len(counts)-x]: # calculating the postition of the highest repeating ids
                    if IDS[y] not in ids:
                        ids.append(IDS[y])
        names = []
        for _id in ids:
            cursor.execute("SELECT UNINAME FROM UNIENTRY WHERE UNI_ID > ? AND UNI_ID = ?", (0, _id))
            uni_name = cursor.fetchall()
            uni_name = str(uni_name)
            uni_name = uni_name[3:len(uni_name)-4] # receiving the names from the university id to show to the user in an option menu
            names.append(uni_name)
        handle.commit()
        handle.close()
        new_tab = ttk.Frame(tabcontrol)
        tabcontrol.add(new_tab, text="Popular Unis")
        tabcontrol.select(new_tab)
        tk.Label(new_tab, text= " ").grid(row=1) # blank labels for appropriate spacing
        tk.Label(new_tab, text= " ").grid(row=3)
        tk.Label(new_tab, text= " ").grid(row=5)
        tk.Label(new_tab, text= "Popular Universities", font="Verdana 30 italic").grid(row=2, column=3)
        VAR = StringVar()
        VAR.set(names[random.randint(0, len(ids)-1)]) # setting a random university name to be default in the selection menu
        tk.OptionMenu(new_tab, VAR, *names).grid(row=4, columnspan=7)
        HoverButton(new_tab, activebackground='Black', fg="white", bg="Red", text="Confirm", command = lambda: uni.continue_similar_uni(VAR, VAR, new_tab, ID_insert)).grid(row=6, column=3) # confirming choice of university
        HoverButton(new_tab, activebackground='Black', fg="white", bg="Red", text="Back", command = lambda: [both.closetab(new_tab), uni.unimenu(ID_insert)]).grid(row=6, column=1) # back to the university main menu

    def uni_quals(self, ID_insert, tab4):
        both.closetab(tab4)
        tab0 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab0, text="Enter Grades")
        tabcontrol.select(tab0)
        tk.Label(tab0, text= "Total UCAS points = ").grid(row=1) # getting the number of UCAS points from the user to choose from all the universities that require below that amount of points
        digit3 = IntVar()
        digit3.set("1")
        zero_to_nine = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        OptionMenu(tab0, digit3, *zero_to_nine).grid(row=2, column=1)
        digit2 = IntVar()
        digit2.set("5")
        OptionMenu(tab0, digit2, *zero_to_nine).grid(row=2, column=2) # broke up the ucas points into each digit selection to limit the need of validations of typed inputs
        digit1 = IntVar()
        digit1.set("0")
        OptionMenu(tab0, digit1, *zero_to_nine).grid(row=2, column=3)
        arts_var = StringVar()
        yesno = ["Yes", "No"]
        arts_var.set(yesno[1])
        OptionMenu(tab0, arts_var, *yesno).grid(row=3, column=1)
        tk.Label(tab0, text = "Are you interested in arts/drama/music courses?").grid(row=3)
        HoverButton(tab0, activebackground='black', fg="white", bg="Red", text="ENTER", command = lambda: uni.calculate_uni(ID_insert, digit3, digit2, digit1, tab0, arts_var)).grid(row=4, column=1) # confirming all inputs 
        HoverButton(tab0, activebackground='black', fg="white", bg="Red", text="back", command = lambda: [uni.unimenu(ID_insert), both.closetab(tab0)]).grid(row=5, column=1) # back to the university menu page
        
    def calculate_uni(self, ID_insert, digit1, digit2, digit3, tab0, arts_var):
        digit1 = digit1.get()
        digit2 = digit2.get()
        digit3 = digit3.get()
        arts_var = arts_var.get() # getting all the inputs from the function uni_quals
        points = str(digit1)+str(digit2)+str(digit3)
        points = int(points)
        both.closetab(tab0)
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT UNINAME FROM UNIENTRY WHERE UCAS <= ? AND  UCAS != ?;", (points, "0"))
        entry = cursor.fetchall() # retreiving all of the university names where the UCAS points is lower than what the user has given
        handle.commit()
        handle.close()
        for x in range(0, len(entry)):
            entry[x] = str(entry[x])
            entry[x] = entry[x][2:len(entry[x])-3] # formatting into array from tuple
        if len(entry) > 3:
            ranks = []
            for q in range(0, len(entry)):
                handle = sql.connect("RecommendDATA.db")
                cursor = handle.cursor()
                cursor.execute("SELECT RANK FROM RANKINGS WHERE UNINAME LIKE ? AND  RANK != ?;", (entry[q], ""))
                ranking = cursor.fetchall() # getting the rank that corresponds with that university
                handle.commit()
                handle.close()
                ranking = str(ranking)
                ranking = ranking[8:len(ranking)-4] # formatting from tuple to string
                ranks.append(ranking)
            new = []
            if arts_var == "Yes":
                for c in range(0, len(ranks)):
                    if ranks[c][0] == "A": # all of the arts universities are ranked in another table that begins with the letter A
                        ranks[c] = re.sub("[^0-9]", "", ranks[c]) 
                        new.append(ranks[c])
            else:
                for c in range(0, len(ranks)):
                    if ranks[c][0] == "L": # all of the regular universities are ranked in another table that begins with the letter L
                        ranks[c] = re.sub("[^0-9]", "", ranks[c])
                        new.append(ranks[c])
            allofranks = []
            for c in range(0, len(ranks)):
                if ranks[c][0] == "L":
                    ranks[c] = re.sub("[^0-9]", "", ranks[c])
                allofranks.append(ranks[c]) # gathering all of the ranks into an arrray
            temp = allofranks
            old = new
            highest = 0
            for t in range(0, len(old)): # get the lowest rank from the array
                val = len(old[t])
                if val < highest:
                    highest = val
            for n in range(0, len(old)-1):
                try:
                    old[n] = str(old[n])
                    #old[n] = str(old[n])[-2:]
                    if len(old[n]) != highest:  #removing excess data from the array
                        old.remove(old[n])
                except:
                    cont = True
            new = []
            for char in old:
                char = int(char) # casting each piece of data in the array to an integer
                new.append(char)
            new.sort()
            newv2 = []
            run = True
            while run:
                try:
                    for h in range(0, 2000):
                        newv2.append(str(new[h]))
                except:
                    run = False
            if len(newv2) > 3:
                while len(newv2) > 3:
                    newv2.remove(newv2[len(newv2)-1])
            final = []
            for r in range(0, len(newv2)):
                for p in range(0, len(temp)): # finding the position of the lowest ranks in the orginal rank list, this is used to get the University name from the array "entry"
                    if newv2[r] == temp[p]:
                        final.append(entry[p])
            for r in range(0, len(final)):
                handle = sql.connect("RecommendDATA.db")
                cursor = handle.cursor()
                cursor.execute("SELECT UNI_ID FROM RANKINGS WHERE UNINAME = ? AND UNI_ID > ?", (final[r], 0)) # get the matching id from the University name, to populate recommended table
                ID = cursor.fetchall()
                handle.commit()
                ID = str(ID)
                ID = ID[2:len(ID)-3]
                cursor.execute("INSERT INTO RECOMMEND2 VALUES(?,?)", (ID, ID_insert)) # insert data that the userid has been recommended the University id
                handle.commit()
                handle.close()
                uni.display_uni(final[r], ID_insert) # display the University specific page using the University name
        else:
            for x in range(0, len(entry)-1):
                handle = sql.connect("RecommendDATA.db")
                cursor = handle.cursor()
                cursor.execute("SELECT UNI_ID FROM RANKINGS WHERE UNINAME = ? AND UNI_ID > ?", (entry[x], 0)) # identical as above, except using entry instead of the final array
                ID = cursor.fetchall()
                ID = str(ID)
                ID = ID[2:len(ID)-3]
                handle.commit()
                cursor.execute("INSERT INTO RECOMMEND2 VALUES(?,?)", (ID, ID_insert))
                handle.commit()
                handle.close()
                uni.display_uni(entry[x], ID_insert)
            
    def overallranking(self, IDinsert):
        url= "https://www.thecompleteuniversityguide.co.uk/league-tables/rankings"
        try:
            from bs4 import BeautifulSoup # modules that allow access to html parser of any url
            import requests
        except:
            cont = True # placeholder
        response = requests.get(url) # request to the website for access
        soup = BeautifulSoup(response.content, "html.parser") # gathering the html file
        soup.prettify() # cleaning the html file
        name = soup.find_all("td", class_="league-table-institution-name") # finding the matching element in the html code
        for t in range(0, len(name)):
            name[t] = str(name[t])
            name[t] = name[t].split('title="') # splitting the array by each different university section by "title="
            name[t] = name[t][1][2:len(name[t][1])-10]
        tabres = ttk.Frame(tabcontrol)
        tabcontrol.add(tabres, text="Rankings For Universities")
        tabcontrol.select(tabres)
        tk.Label(tabres, font="Verdana 15", text="Overall Rankings").grid(row=2, column=1) # making new tkinter tab to display the overall rankings
        count = 1
        if len(name) > 15:
            while len(name)> 15:
                name.remove(name[len(name)-1]) # making it only show the top 15 Universities
        for v in range(0, len(name)):
            count = str(count)
            string = count+". "+name[v]
            count = int(count)
            tk.Label(tabres, font="Ariel 12", text=string).grid(row=count+4, column=1) # label containing the University name and the rank in the top 15
            count = count+1
        tk.Label(tabres, font="Verdana 7", text=" ").grid(row=1)
        tk.Label(tabres, font="Verdana 7", text=" ").grid(row=3) # spacing to provide structure
        tk.Label(tabres, font="Verdana 7", text=" ").grid(row=count+5)
        HoverButton(tabres, activebackground='black', fg="white", bg="red", text="Menu", command = lambda: [both.closetab(tabres), uni.unimenu(IDinsert)]).grid(row=count+6, columnspan=7) # back to the main university homepage

    def searchbyuni(self, entrybox, tab0, IDinsert):
        entrybox = entrybox.get()
        both.closetab(tab0)
        f = open("NamesOfUnis.txt")
        subjects = []
        try:
            for j in range(0,140):
                subjects.append(f.readline()) # reading all University names from a file and arranging them into an array and then calling the next function "searchresults_uni"
        except:
            cont= True
        for i in range(0, len(subjects)-1):
            subjects[i] = subjects[i][:len(subjects[i])-1]
        all_names = subjects
        uni.searchresults_uni(entrybox, all_names, IDinsert)
        
    def searchresults_uni(self, entrybox, all_names, IDinsert):
        entrybox = entrybox.upper()
        repeatlist = []
        for l in range(0, len(all_names)):
            all_names[l] = all_names[l].upper() # making all the characters upper so it's case insensitive
            repeats = 0
            for p in range(0, len(all_names[l])):
                try:
                    letter = all_names[l][p]
                    if entrybox[p] == letter: # getting the number of matches for each University name to the input and then storing in an array
                        repeats = repeats+1
                except:
                    cont=True
            repeatlist.append(repeats)
        repeatlist.sort()
        highestrepeat = repeatlist[len(repeatlist)-1] # finding the highest amount of repeats
        unis =[]
        for l in range(0, len(all_names)):
            repeats = 0
            for p in range(0, len(all_names[l])):
                try:
                    letter = all_names[l][p]
                    if entrybox[p] == letter:
                        repeats = repeats+1 # doing the same process again and if it matches the highest number of repeats, save it to an array
                except:
                    cont=True
            if repeats == highestrepeat:
                unis.append(all_names[l])
        if len(unis) > 3:
            while len(unis) > 3:
                unis.remove(unis[len(unis)-1]) # maximum amount of suggestions is 3
        for r in range(0, len(unis)):
            uniname = unis[r]
            uni.display_uni(uniname, IDinsert) # displaying each University page to the user
            
    def display_uni(self, uniname, IDinsert):
        name = uniname
        uniname = uniname.lower()
        uniname = uniname.split(",")
        uniname = uniname[0]
        uniname = uniname.replace(" ", "-")
        url = "https://www.thecompleteuniversityguide.co.uk/" # creating the url that this data was extracted from
        url = url+uniname
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT RANK FROM RANKINGS WHERE UNINAME LIKE ? AND  RANK != ?;", (name, ""))
        ranks = cursor.fetchall()
        cursor.execute("SELECT UCAS FROM UNIENTRY WHERE UNINAME LIKE ? AND  UCAS != ?;", (name, "")) # all of these retreivals are done seperately is it's easier to format them independently as adding an extra step of breaking them up again
        points = cursor.fetchall()
        cursor.execute("SELECT UNI_ID FROM UNIENTRY WHERE UNINAME LIKE ? AND  UNI_ID != ?;", (name, ""))
        uniid = cursor.fetchall()
        uniid = re.sub("[^0-9]", "", str(uniid))
        cursor.execute("SELECT RATING FROM RATINGS2 WHERE UNIID = ? AND UNIID != ?", (uniid, ""))
        all_ratings = cursor.fetchall()
        all_ratings = str(all_ratings)
        all_ratings = all_ratings.split('(')
        all_ratings2 = []
        total_rating = 0
        for rate in all_ratings:
            rate = re.sub('[^0-9]', '', str(rate)) # formatting each of the tuples into appropriate types
            if rate == "":
                cont = True # placeholder
            else:
                all_ratings2.append(rate)
                total_rating = total_rating + int(rate)
        try:
            average = total_rating / len(all_ratings2)
        except:
            average = 3
        handle.commit()
        handle.close()
        points = str(points)
        points = points[2:len(points)-3]
        pointint = points
        points = "Average UCAS Entry Requirements: "+points
        ranks = str(ranks)
        ranks = ranks[3:len(ranks)-4]
        unitab = ttk.Frame(tabcontrol) # creating the tkinter tab before adding all of the labels and buttons
        tabcontrol.add(unitab, text=name)
        tabcontrol.select(unitab)
        ratingtext = "Rate this Uni: average rating = " + str(average)
        tk.Label(unitab, fg="red", text=name, font="Ariel 17 italic").grid(row=2, columnspan=3)
        tk.Label(unitab, fg="black", text=points, font="Ariel 12 italic").grid(row=4, column=1) # displaying all of the appropriate data
        tk.Label(unitab, fg="black", text=ranks, font="Ariel 10 italic").grid(row=3, column=1)
        tk.Label(unitab, fg="black", text= ratingtext, font="Ariel 15 italic").grid(row=6, column=1)
        HoverButton(unitab, activebackground='red', fg="white", bg="black", text="Similar Universities", command = lambda: uni.similar_uni(name, pointint, unitab, IDinsert)).grid(row=5, column=1)
        HoverButton(unitab, activebackground='black', fg="white", bg="red", text="Menu", command = lambda: uni.unimenu(IDinsert)).grid(row=12, column=1) # back to University homepage
        HoverButton(unitab, activebackground='black', fg="white", bg="red", text="Close Tab", command = lambda: [both.closetab(unitab)]).grid(row=13, column=1)
        one_to_five = [1, 2, 3, 4, 5]
        stars = IntVar()
        stars.set(3)
        tk.OptionMenu(unitab, stars, *one_to_five).grid(row=7, column=1) # rating digit option menu to impact its average rating
        tk.Label(unitab, text ="Comment: ", font="Ariel 12").grid(row=8, column=1)
        comment = tk.Entry(unitab) # allowing the user to make any comments on the content provided
        comment.grid(row=9, column=1)
        HoverButton(unitab, activebackground='black', fg="white", bg="Red", text="Enter", command = lambda: uni.ratingadd(stars, comment, uniid, name, IDinsert, unitab)).grid(row=10, column=1) # entering any comments and the rating

    def ratingadd(self, stars, comment, uniid, uniname, ID_insert, tab):
        var = stars.get()
        comment = comment.get() # processing the users data into the table of ratings for Universities
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("INSERT INTO RATINGS2 VALUES(?,?,?)", (uniid, var, comment))
        handle.commit()
        handle.close()
        both.closetab(tab)
        uni.display_uni(uniname, ID_insert) # refreshing the specific University page for the user with a new average rating


    def similar_uni(self, name, pointint, unitab, IDinsert):
        tab39 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab39, text="Similar Universities")
        tabcontrol.select(tab39)
        pointint = int(pointint)
        point = pointint-11
        similar = []
        for b in range(0, 10): # selecting all of the other Universities that are within a 10 point range of the selected University (5 either side)
            point = point+1
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            cursor.execute("SELECT UNINAME FROM UNIENTRY WHERE UCAS = ? AND  UNINAME != ?;", (point, ""))
            names = cursor.fetchall()
            handle.commit()
            handle.close()
            if names == []:
                cont = True
            else:
                if len(names) > 1:
                    names = names[0] #formatting any University names to be put into an array for the user to evaluate
                names = str(names)
                names = names[2:len(names)-3]
                if names[0] == "'":
                    names = names[1:len(names)-1]
                similar.append(names)
        if similar == []:
            tk.Label(tab39, text="No Similar Universities.").grid(row=5, column=1) # no universities within a 10 point range
        else:
            variable = StringVar()
            variable.set(similar[random.randint(0, len(similar)-1)]) # set default as a random University name
            OptionMenu(tab39, variable, *similar).grid(row=5, column=1)
            HoverButton(tab39, activebackground='black', fg="white", bg="red", text="ENTER", command = lambda: uni.continue_similar_uni(variable, name, tab39, IDinsert)).grid(row=6, column=1) # get the matching job page
        HoverButton(tab39, activebackground='black', fg="white", bg="red", text="Back", command = lambda: both.closetab(tab39)).grid(row=8, column=1)

    def continue_similar_uni(self, variable, name, tab39, IDinsert):
        tab39.destroy()
        variable = variable.get() # interpret the selection
        uni.display_uni(variable, IDinsert) # call for a new job specifc page
        
    def searchbysub(self, IDinsert):
        tab0 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab0, text="Select Subject")
        tabcontrol.select(tab0)
        f = open("Subjects.txt")
        subjects = []
        try:
            for j in range(0,70):
                subjects.append(f.readline()) # getting all of the different subjects that can be used to rank Universities
        except:
            cont= True
        for i in range(0, len(subjects)-1):
            subjects[i] = subjects[i][:len(subjects[i])-1]
        opt = StringVar()
        opt.set(subjects[random.randint(0, len(subjects)-1)])
        tk.Label(tab0, text=" ").grid(row=1)
        tk.Label(tab0, text=" ").grid(row=5) # spacing purposes
        tk.Label(tab0, text=" ").grid(row=3)
        OptionMenu(tab0, opt, *subjects).grid(row=2, column=1) # option menu to select which subject the user desires
        HoverButton(tab0, activebackground="Black", fg="White", bg="Red", text="Enter", command = lambda: [uni.displaysubjectsearch(opt, IDinsert), both.closetab(tab0)]).grid(row=4, column=1)
        HoverButton(tab0, activebackground='Black', fg="Red", bg="White", text="Menu", command = lambda: [both.closetab(tab0), uni.unimenu(IDinsert)]).grid(row=9, column=1)

    def displaysubjectsearch(self, opt, IDinsert):
        opt = opt.get()
        subjectname = opt
        opt= str(opt)
        opt = opt.replace(" ", "+")
        opt = opt.replace("&", "%26") # replicating the url pattern consistantly done for all ranking tables
        url= "https://www.thecompleteuniversityguide.co.uk/league-tables/rankings?s="
        url = url+opt
        try:
            from bs4 import BeautifulSoup # modules that allow access to html parser of any url
            import requests
        except:
            cont = True
        response = requests.get(url) # request to the website for access
        soup = BeautifulSoup(response.content, "html.parser") # gathering the html file
        soup.prettify() # cleaning the html file
        name = soup.find_all("td", class_="league-table-institution-name") # searching for an element in the html file
        for t in range(0, len(name)):
            name[t] = str(name[t])
            name[t] = name[t].split('title="') # splitting the name into sections for each University
            name[t] = name[t][1][2:len(name[t][1])-10]
        tabres = ttk.Frame(tabcontrol)
        tabcontrol.add(tabres, text="Rankings For Subject")
        tabcontrol.select(tabres)
        tk.Label(tabres, font="Verdana 13", text=" ").grid(row=1)
        tk.Label(tabres, font="Verdana 12", text=subjectname).grid(row=2, column=3) # displaying the subject name the user choose previously
        tk.Label(tabres, font="Verdana 13", text=" ").grid(row=3, columnspan=7)
        count = 1
        if len(name) > 15:
            while len(name)> 15:
                name.remove(name[len(name)-1])
        for v in range(0, len(name)):
            count = str(count)
            string = count+". "+name[v] # formatting into number then the University name (eg. 15. University of Sheffield)
            count = int(count)
            tk.Label(tabres, font="Ariel 13", text=string).grid(row=count+3, column=3)
            count = count+1
        HoverButton(tabres, activebackground='Black', fg="white", bg="Red", text="Menu", command = lambda: [both.closetab(tabres), uni.unimenu(IDinsert)]).grid(row=3, column=7)
        HoverButton(tabres, activebackground='Red', fg="Black", bg="White", text="Back", command = lambda: [both.closetab(tabres), uni.searchbysub(IDinsert)]).grid(row=3, column=1)

    def getucaspoints(self):
        f = open("NamesOfUnis.txt") # this function is used when setting up the Rankings and Unientry tables with all the data
        names = []
        try:
            for j in range(0,140):
                names.append(f.readline()) # producing an array of all the University names
        except:
            cont= True
        for i in range(0, len(names)-1):
            names[i] = names[i][:len(names[i])-1]
            uniname = names[i]
            uniname = uniname.lower()
            uniname = uniname.split(",") # replicating the url for each University by replacing the $ in the url string
            uniname = uniname[0]
            uniname = uniname.replace(" ", "-")
            url = "https://www.thecompleteuniversityguide.co.uk/$/performance"
            url = url.replace("$", uniname)
            try:
                from bs4 import BeautifulSoup # modules that allow access to html parser of any url
                import requests
            except:
                cont = True
            response = requests.get(url) # request to the website for access
            soup = BeautifulSoup(response.content, "html.parser") # gathering the html file
            soup.prettify() # cleaning the html file
            try:
                ranks = soup.find("div", class_="institution-header-league-table").text
                ranks = ranks.strip() # searching for the rank in the html file
            except:
                ranks = ""
            try:
                entrypoint = soup.find("span", class_="league-table-score-value") # searching for the amount of UCAS points on average needed
            except:
                entrypoint= ""
            entrypoint = str(entrypoint)
            entrypoint = re.sub("[^0-9]", "", entrypoint) # inputting all of the data into the tables for reference in other functions
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            cursor.execute("INSERT INTO UNIENTRY VALUES(?,?,?)", (i, names[i], entrypoint))
            cursor.execute("INSERT INTO RANKINGS VALUES(?,?,?)", (i, names[i], ranks))
            handle.commit()
            handle.close()
 #
 #
 #
 #
 #
 #

class job: # making a job class to catagorise all of the functions
    def mainmenu(self, IDinsert):
        uniorjob = False
        tab1 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab1, text="Jobs")
        tabcontrol.select(tab1)
        attempts = 0
        tk.Label(tab1, text="Job Research Tool", font="Verdana 29", fg="blue").grid(row=2+1, columnspan=7)
        tk.Label(tab1, text=" ").grid(row=3+1, column=1)
        tk.Label(tab1, text=" ").grid(row=19, column=1) # spacing for structural purposes
        tk.Label(tab1, text=" ").grid(row=11, column=1)
        tk.Label(tab1, text=" ").grid(row=21, column=1)
        HoverButton(tab1, activebackground='blue', fg="white", bg="black", text = "POPULAR JOBS", command = lambda: job.popular(tab1, IDinsert)).grid(row=12, column=1)
        HoverButton(tab1, activebackground='blue', fg="white", bg="black", text = "HIGHLY RATED", command = lambda: job.rating(tab1, IDinsert)).grid(row=12, column=2) # creating buttons to redirect, to recommend jobs based on held statistics
        HoverButton(tab1, activebackground='blue', fg="white", bg="black", text = "SEARCH FIELDS", command = lambda: job.fieldstart(tab1, IDinsert)).grid(row=12, column=3)
        tk.Label(tab1, text="SEARCH JOBS:", font="Verdana 12 bold italic", fg="black").grid(row=6+1, column=1)
        searchjobentry = tk.Entry(tab1, font="Ariel 12")
        searchjobentry.insert(END, "Job Title") # inserting job title so the user knows what to input into the entry box
        searchjobentry.grid(row=7+1, column=2)
        HoverButton(tab1, activebackground='blue', fg="white", bg="black", text="ENTER", command= lambda: job.search(searchjobentry, tab1, IDinsert)).grid(row=8+1, column=2)
        HoverButton(tab1, width=70, height=5, activebackground='black', fg="white", bg="blue", text="Find Reccomendations", command = lambda: job.fieldq(IDinsert, tab1)).grid(row=20, columnspan=7) # buttons to different processes
        tk.Label(tab1, text="JOB CENTRES:", font="Verdana 12 bold italic", fg="Green").grid(row=23+1, column=1)
        postcode = tk.Entry(tab1, font="Ariel 12")
        postcode.insert(END, "POSTCODE") # inserting postcode so the user knows what to input into the entry box
        postcode.grid(row=23+1, column=2)
        HoverButton(tab1, activebackground='black', fg="white", bg="Green", text="ENTER", command = lambda: job.jobcentre(postcode, tab1, IDinsert).run()).grid(row=24+1, column=2)
        namesearch = tk.Entry(tab1, font="Ariel 12")
        namesearch.insert(END, "NAME") # inserting name so the user knows what to input into the entry box
        namesearch.grid(row=24, column=3)
        HoverButton(tab1, activebackground='black', fg="white", bg="Green", text="ENTER", command = lambda: job.jobcentre(namesearch, tab1, IDinsert).name_similar()).grid(row=25, column=3)
        tk.Label(tab1, text=" ").grid(row=28+1, column=1)
        HoverButton(tab1, height=5, width=70, activebackground='black', fg="white", bg="red", text="Home", command = lambda: [both.closetab(tab1), both.home(IDinsert)]).grid(row=29+1, columnspan=7) # back to logged in home
    
    class jobcentre:
        def __init__(self, post, tab, IDinsert): # creating a base class that holds all crucial data as public variables and to catagorise functions
            self.post = post
            self.tab = tab
            self.IDinsert = IDinsert
        
        def main_menu(self):
            both.closetab(self.tab)
            tab1 = ttk.Frame(tabcontrol)
            tabcontrol.add(tab1, text= self.post)
            tabcontrol.select(tab1)
            handle = sql.connect("JobCentreData.db") # creating a main menu by pulling all the data from the database and displaying it to the user
            cursor = handle.cursor()
            cursor.execute("SELECT CENTREID, LONG, LAT, POST FROM DATA WHERE ADDRESS = ? AND LAT != ?", (str(self.post), 0))
            data = cursor.fetchall()
            data = str(data)
            data = data.split(',')
            data[0] = re.sub('[^0-9]', '', str(data[0]))
            data[1] = data[1][2:len(data[1])-1]
            data[2] = data[2][2:len(data[2])-1] # formatting tuple data by replacing all unwanted characters at each end of the strings
            data[3] = data[3][2:len(data[3])-3]
            handle.commit()
            handle.close()
            tk.Label(tab1, text="Address: ", font="Ariel 12", fg="Black").grid(row=1)
            tk.Label(tab1, text=self.post, font="Ariel 9 italic", fg="Black").grid(row=2)
            tk.Label(tab1, text="CentreID: ", font="Ariel 12", fg="Black").grid(row=3)
            tk.Label(tab1, text=data[0], font="Ariel 13 italic", fg="Black").grid(row=4)
            tk.Label(tab1, text="Longitude: ", font="Ariel 12", fg="Black").grid(row=5) # using labels to show all of the different information to the user
            tk.Label(tab1, text=data[1], font="Ariel 13 italic", fg="Black").grid(row=6)
            tk.Label(tab1, text="Latitude: ", font="Ariel 12", fg="Black").grid(row=7)
            tk.Label(tab1, text=data[2], font="Ariel 13 italic", fg="Black").grid(row=8)
            tk.Label(tab1, text="Postcode: ", font="Ariel 12", fg="Black").grid(row=9)
            tk.Label(tab1, text=data[3], font="Ariel 13 italic", fg="Black").grid(row=10)
            tk.Label(tab1, text="Rate this Centre: ", font="Ariel 12", fg="Black").grid(row=11)
            stars = IntVar()
            stars.set(3)
            handle = sql.connect("JobCentreData.db")
            cursor = handle.cursor()
            cursor.execute("INSERT INTO RECOMMEND4 VALUES(?,?)", (data[0], self.IDinsert)) # inserting data into this table to record any job centre recommendations by association with user id and jobcentre id
            handle.commit()
            handle.close()
            one_to_five = [1, 2, 3, 4, 5]
            tk.OptionMenu(tab1, stars, *one_to_five).grid(row=12)
            tk.Label(tab1, text ="Comment: ", font="Ariel 12").grid(row=13) # rating mechansim so users can rate the centre accordingly
            comment = tk.Entry(tab1)
            comment.grid(row=14)
            HoverButton(tab1, activebackground='black', fg="white", bg="Green", text="Enter", command = lambda: job.jobcentre(comment, tab1, self.IDinsert).rating(stars, self.post, data[0])).grid(row=15)
            HoverButton(tab1, activebackground='Green', fg="white", bg="Black", text="Close Tab", command = lambda: both.closetab(tab1)).grid(row=17)
            HoverButton(tab1, height=5, width=70, activebackground='black', fg="white", bg="Green", text="Home", command = lambda: [both.closetab(tab1), job.mainmenu(self.IDinsert)]).grid(row=21, columnspan=7) # buttons to following processes / functions

        def rating(self, VAR, address, centreid):
            var = VAR.get()
            comment = self.post.get() # interpreting the user inputs
            handle = sql.connect("JobCentreData.db") # inserting all of the user given data into the rating database for job centres
            cursor = handle.cursor()
            cursor.execute("INSERT INTO RATING4 VALUES(?,?,?)", (centreid, var, comment))
            handle.commit()
            handle.close()
            job.jobcentre(address, self.tab, self.IDinsert).main_menu() # go back to the job centre page that the user left a rating on

        def name_similar(self):
            entrybox = self.post.get().upper()
            handle = sql.connect("JobCentreData.db")
            cursor = handle.cursor()
            cursor.execute("SELECT ADDRESS FROM DATA") # receiving all of the addresses from every single job centre
            addresses = cursor.fetchall()
            handle.commit()
            handle.close()
            addresslist = []
            addresslist2 = []
            for address in addresses:
                address = str(address)
                address = address[2:len(address)-3] # formatting data by removing unwanted characters at each end of the strings
                addresslist.append(address)
                addresslist2.append(address)
            addresses = addresslist
            repeatlist = []
            for l in range(0, len(addresses)):
                addresses[l] = addresses[l].upper() # making it all upper case so insensitive
                repeats = 0
                for p in range(0, len(addresses[l])):
                    try:
                        letter = addresses[l][p]
                        if entrybox[p] == letter: # tracking number of matches for each job centre and storing this in an array
                            repeats = repeats+1
                    except:
                        cont=True
                repeatlist.append(repeats)
            repeatlist.sort()
            highestrepeat = repeatlist[len(repeatlist)-1] # getting the highest number of repeats
            unis =[]
            for l in range(0, len(addresses)):
                repeats = 0
                for p in range(0, len(addresses[l])):
                    try:
                        letter = addresses[l][p]
                        if entrybox[p] == letter: # doing the same process as above but if the outcome matches, the job centre will be added to a new array
                            repeats = repeats+1
                    except:
                        cont=True
                if repeats == highestrepeat:
                    unis.append(addresses[l])
            if len(unis) > 3:
                while len(unis) > 3:
                    unis.remove(unis[len(unis)-1]) # maximum of 3 job centres can be shown
            counts = []
            for r in range(0, len(unis)):
                uniname = unis[r]
                count = 0
                hold = 0
                for address in addresslist:
                    if address.upper() == uniname:
                        hold = count
                    count = count + 1
                counts.append(hold)
            for num in counts:
                job.jobcentre(addresslist2[num], self.tab, self.IDinsert).main_menu() # call for a new job centre page to be created that is the most appropriate for the search

        def distance(self, longit1, lat1, longit2, lat2):
            try:
                import math # mainly to do the square root operation for the various distance calculations
            except:
                cont = True
            step1 = float(lat2) - float(lat1)
            step1 = step1 * step1
            step2 = float(longit2) - float(longit1) # from the parameters given, a distance will be returned that is between two pairs of longitudes and latitudes
            step2 = step2 * step2
            step3 = step1 + step2
            step3 = math.sqrt(step3)
            return step3

        def run(self):
            self.post = self.post.get()
            both.closetab(self.tab)
            tab1 = ttk.Frame(tabcontrol)
            tabcontrol.add(tab1, text="Job Centres")
            tabcontrol.select(tab1)
            try:
                nomi = pgeocode.Nominatim('GB')
                info = nomi.query_postal_code(self.post) # getting a bunch of data from the postcode given
                lat = info[9]
                longit = info[10] # provides an array which long lat are the 10th and 11th items
            except:
                lat = 0
                longit = 0
            handle = sql.connect("JobCentreData.db")
            cursor = handle.cursor()
            cursor.execute("SELECT LONG, LAT FROM DATA") # getting all of the coordinates for each jobcentre
            latlong = cursor.fetchall()
            handle.commit()
            handle.close()
            hold = 999
            data = []
            for y in range(0, len(latlong)):
                dist = job.jobcentre.distance(self, longit, lat, latlong[y][0], latlong[y][1]) # finding the distance between the coordinates
                if float(dist) <= float(hold):
                    hold = dist
                    data.append(latlong[y][0]) # if the distance is the smallest so far, record the long lat and distance
                    data.append(latlong[y][1])
            tk.Label(tab1, text="Nearest Job Centre to your Postcode").grid(row=1)
            try:
                handle = sql.connect("JobCentreData.db")
                cursor = handle.cursor()
                cursor.execute("SELECT CENTREID, POST, ADDRESS FROM DATA WHERE LAT = ? AND LONG = ?", (data[len(data)-1], data[len(data)-2])) # retreive all of the data for the jobcentre with the smallest distance
                latlongs = cursor.fetchall()
                handle.commit()
                handle.close()
                latlongs = str(latlongs)
                lats = str(latlongs)
                latlongs = latlongs.split(",") # formatting by splitting attributes
                centre_id = int(latlongs[0][2:])
                add = lats.split("'")
                add = add[3]
                result = latlongs[0][3:len(latlongs[0])-1]
                tab3 = ttk.Frame(tabcontrol)
                both.closetab(tab1)
                job.jobcentre(add, tab3, self.IDinsert).main_menu() # display the resulting jobcentre specific page
            except:
                tk.Label(tab1, text="Closest Job Centre:").grid(row=2)
                tk.Label(tab1, text="Invalid Postcode Input").grid(row=2, column=1) # if the postcode is invalid, show the user this and then a way back the the section menu for potential re-entry
            tk.Button(tab1, text="Back", command = lambda: [job.mainmenu(self.IDinsert), both.closetab(tab1)]).grid(row=3)
            tk.Label(tab1, text="*This works on straight distance not traffic, river, sea variables are included in calculations").grid(row=4, columnspan=2)

    def fieldq(self, ID_insert, tab4):
        tab4.destroy()
        tab3 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab3, text="Field Choice")
        tabcontrol.select(tab3)
        file = open("fieldlist.txt", "r")
        fields = []
        for r in range(0, 16):
            field = file.readline() # retreiving all of the fields that all jobs fit under
            fields.append(field)
        countofiterations = 0
        recordchoices = []
        var1 = IntVar()
        tk.Label(tab3, text=" ").grid(row=1, column=1)
        job.recurfield(ID_insert, tab3, fields, countofiterations, recordchoices, var1) # call for opinion on each field

    def recurfield(self, ID_insert, tab3, fields, countofiterations, recordchoices, var1):
        if countofiterations == 0:
            tk.Label(tab3, font="Verdana 13", fg="Black", text="Choose a proirity of each field so recommendation.").grid(row=1, columnspan=7)
            tk.Label(tab3, font="Verdana 13", fg="Black", text=" can be more appropriate.").grid(row=2, columnspan=7) # display labels on the first call of the function
            tk.Label(tab3, font="Verdana 10", fg="Black", text=" ").grid(row=3, columnspan=7)
        else:
            var1=var1.get() # get previous recursion's input and record it in an array 
            recordchoices.append(var1)
        if countofiterations == len(fields):
            job.updatefields(ID_insert, recordchoices, fields, tab3) # upon completion move onto the storage of input data
        try:
            label = tk.Label(tab3, font="Ariel 11", fg="Grey", text=fields[countofiterations])
            label.grid(row=4, column=1)
            tk.Label(tab3, font="Ariel 11", fg="Grey", text=str(countofiterations)+"/"+str(len(fields)-1)).grid(row=4, column=2)
            countofiterations=countofiterations+1
            var1 = IntVar()
            tk.Radiobutton(tab3, font="Ariel 13", text="Very Interested", value=5, variable=var1).grid(row=5, columnspan=7)
            tk.Radiobutton(tab3, font="Ariel 13", text="Interested", value=4, variable=var1).grid(row=6, columnspan=7)
            tk.Radiobutton(tab3, font="Ariel 13", text="Neutral", value=3, variable=var1).grid(row=7, columnspan=7)
            tk.Radiobutton(tab3, font="Ariel 13", text="Not Interested", value=2, variable=var1).grid(row=8, columnspan=7) # choice for a user to show their opinion on each field
            tk.Radiobutton(tab3, font="Ariel 13", text="Avoid", value=1, variable=var1).grid(row=9, columnspan=7)
            tk.Label(tab3, text=" ").grid(row=10)
            HoverButton(tab3, width=10, height=2, activebackground='Light Yellow', fg="Black", bg="Yellow", text="NEXT FIELD", command= lambda: [job.recurfield(ID_insert, tab3, fields, countofiterations, recordchoices, var1), both.closetab(label)]).grid(row=11, columnspan=8) # continues recursion
            HoverButton(tab3, width=10, height=2, activebackground='Light Green', fg="white", bg="Green", text="SKIP ALL", command= lambda: job.Increasefield(ID_insert, tab3, fields, countofiterations, recordchoices, var1)).grid(row=12, columnspan=8) # skips to the end of the recursion
            tk.Label(tab3, text=" ").grid(row=13)
            HoverButton(tab3, width=10, height=2, activebackground='blue', fg="white", bg="black", text="Home", command= lambda: [both.closetab(tab3), job.mainmenu(ID_insert)]).grid(row=14, columnspan=7)
        except:
            hold = 0 # placeholder

    def Increasefield(self, ID_insert, tab3, fields, countofiterations, recordchoices, var1):
        while countofiterations < 16:
            countofiterations=countofiterations+1 # keep increasing the variable that counts iterations of the recursive function
        job.recurfield(ID_insert, tab3, fields, countofiterations, recordchoices, var1)

    def updatefields(self, ID_insert, recordchoices, fields, tab3):
        recordchoices.reverse()
        tab3.destroy()
        recordchoices.pop()
        recordchoices.reverse() # flipping the inputs so they are in the correct order
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        if recordchoices == []:
            recordchoices = ["5"]*len(fields)
        cursor.execute("UPDATE USERS SET FIELDS = ? WHERE USERID = ?;", (str(recordchoices), ID_insert)) # inputting the field into the database of what the user chose for each field
        handle.commit()
        handle.close()
        job.usedata(recordchoices, fields, ID_insert)# the array is 5 - very interested to 1 - avoid per field

    def usedata(self, recordchoices, fields, ID_insert): # function that attains all of the data for workxp to use in the algorithm
        if recordchoices == []:
            recordchoices = ["3"]*len(fields)
        store=[]
        joblist = []
        sorts = recordchoices
        sorts.sort()
        if len(sorts) == "0":
            skip = True # placeholder
        else:
            high = sorts[len(sorts)-1]
            for c in range(0, len(sorts)):
                if recordchoices[c] == high:
                    store.append(c)
            while len(store) < 2:
                high = high-1
                for c in range(0, len(sorts)):
                    if recordchoices[c] == high: #finding the highest interest rating for fields, hence skipping the whole process will result in all jobs being included in the algorithm
                        store.append(c)
            finalfields = []
            for i in range(0, len(store)):
                finalfields.append(fields[store[i]])
        all_ = []
        for e in range(0, len(finalfields)):
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            cursor.execute("SELECT JOBNAME FROM JOBS WHERE FIELD = ?;", (finalfields[e],)) # retreiving all of the jobs in each of the top rated fields
            alljobsinfields = cursor.fetchall()
            handle.commit()
            handle.close()
            all_.append(alljobsinfields)
        fin = []
        for b in range(0, len(all_)):
            for c in range(0, len(all_[b])):
                punctuation = """!"#$%&'()*+:;<=>?@[]^_`{|}~"""
                edited = ""
                string = str(all_[b][c])
                for i in string:
                    if i not in punctuation: # formatting the output by the database into arrays from tuples, removing unwanted characters
                        edited += i
                edited = edited[:-2]
                fin.append(edited)
        # quallevel comparisons
        for c in range(0, len(fin)):
            fin[c] = str(fin[c])
            fin[c] = fin[c][:len(fin[c])-1]
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            cursor.execute("SELECT QUALLEVEL FROM JOBS WHERE JOBNAME LIKE ? AND IDLE = ?", ("%"+fin[c]+"%", 0)) # sql to remove the tuple status by using like.
            qualforjob = cursor.fetchall()
            handle.commit()
            handle.close()
            nameofqual = job.findcommonqual(qualforjob) # using other function to return the level of qualification
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            cursor.execute("SELECT QUALLEVEL FROM USERS WHERE USERID = ? AND USERID > ?", (ID_insert, "0"))
            userqual = cursor.fetchall() 
            handle.commit()
            handle.close() # get the qual-level from the user and if the users and jobs level match its used in the algorithm function by addition to an array
            userqual = str(userqual)
            userqual = userqual[3:len(userqual)-4]
            if userqual == nameofqual:
                joblist.append(fin[c])
        if len(joblist) > 2:
            job.workxp(joblist, recordchoices, ID_insert) # performing the algorithm to return the best suited jobs
        else:
            if joblist == []:
                job.workxp(fin, recordchoices, ID_insert) # performing the algorithm to return the best suited jobs
            else:
                handle = sql.connect("RecommendDATA.db") # if one job is left, just use that rather than still using algorithm
                cursor = handle.cursor()
                cursor.execute("SELECT JOBID FROM JOBS WHERE JOBNAME LIKE ? AND IDLE = ?", ("%"+joblist[0]+"%", 0))
                jobid = cursor.fetchall()
                jobid = str(jobid)
                jobid = jobid[2:len(jobid)-3] # recording recommendation with association between job id and the user id
                jobid = int(jobid)
                handle.commit()
                cursor.execute("INSERT INTO RECOMMEND VALUES(?,?)", (jobid, ID_insert))
                handle.commit()
                handle.close()
                job.display(joblist[0], 1, ID_insert) # calls to display the specific job

    def findcommonqual(self, qualforjob):
        qualforjob = str(qualforjob)
        qualforjob = qualforjob.split("'")
        del qualforjob[::2]
        quals = []
        for h in range(0, len(qualforjob)):
            punctuation = """!"#$%&'()*+/:;=?@[\\]^_`{|}~""" # this process is done to identify which level it is, this is due to the website being rather inconsistant in where and how its placed and the elements it corresponds to.
            edited = ""
            string = str(qualforjob[h])
            for i in string:
                if i not in punctuation:
                    edited += i
            if edited == "High School DiplomaGED": # strange website generated string alterations
                edited = edited[:-3]
            if edited == " High School Diploma": # strange website generated string alterations
                #removing first space
                edited = edited[1:]
            quals.append(edited)
        nums = []
        ext = len(quals)-1
        while ext > 0:
            numcompare = quals[ext]
            nums.append(numcompare)
            ext = ext-2
        numbers = []
        # search for largest number in quals and find the corrosponding level
        for l in range(0, len(nums)): 
            nums[l] = float(nums[l])
            numbers.append(nums[l])
        numbers.sort()
        q = len(quals)-1
        nameofqual = ""
        while q > 0:
            if numbers[len(numbers)-1] == float(quals[q]): # matching the numbers and the qualification level names to give the highest percentage at a level being representated
                nameofqual = quals[q-1]
            q=q-2
        return nameofqual
        
    def workxp(self, joblist, inputedfield, ID_insert):
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT FIELDS FROM USERS")
        fields = cursor.fetchall()
        field2 = []
        for field in fields: # get the users fields that were inputted and then format into an array
            field = str(field)
            field2.append(field[2:len(field)-3])
        sims = []
        sims2 = []
        user = re.sub('[^0-9]', '', str(inputedfield))

        for x in range(0, len(field2)):
            similar = 0
            ints = re.sub('[^0-9]', '', str(field2[x]))
            for y in range(0, len(ints)):
                try:
                    if ints[y] == user[y]: # quantifying the similarity of various other users inputs into the field selection process
                        similar += 1
                except:
                    cont = True
            sims.append(similar)
            sims2.append(similar)

        sims.sort()
        x = 0
        cont = True
        allids = []
        for x in range(1, len(sims)):
            for y in range(0, len(sims2)):
                if sims2[y] == sims[len(sims)-x]: # if the sorted matches the unsorted, this means that the position is the user that is most appropriate
                    postition = y
                    recommend_fields = field2[postition]
                    handle = sql.connect("RecommendDATA.db")
                    cursor = handle.cursor()
                    cursor.execute("SELECT USERID FROM USERS WHERE FIELDS = ? AND USERID > ?", (recommend_fields, 0)) # get the user id that corresponds to that field input
                    userid = cursor.fetchall()
                    userid = str(userid)
                    userid = userid[3:len(userid)-4] # formatting into string from a tuple
                    cursor.execute("SELECT JOBID FROM RECOMMEND WHERE USERID = ? AND JOBID > ?", (userid, 0)) # get the job ids that have been given to that user
                    jobids = cursor.fetchall()
                    if jobids == []:
                        cont = True
                    else:
                        for ids in jobids:
                            ids = str(ids)
                            ids =  ids[1:len(ids)-2]  # formatting into string from a tuple
                            if ids not in allids:
                                allids.append(ids) # adding each job id to the final array
        result_tab = ttk.Frame(tabcontrol)
        tabcontrol.add(result_tab, text="All Recommendations")
        tabcontrol.select(result_tab)
        while len(allids) > 3:
            allids.remove(allids[len(allids)-1]) # max of 3 recommended jobs by other users
        names = []
        for r in range(0, len(allids)):
            cursor.execute("SELECT JOBNAME FROM JOBS WHERE JOBID = ? AND JOBID > ?", (allids[r], 0))
            jobname = cursor.fetchall()
            jobname = str(jobname)
            jobname = jobname[3:len(jobname)-6] # getting the jobname to display to the user below
            names.append(jobname)
        handle.commit()
        handle.close()
        #
        tk.Label(result_tab, font="Ariel 15", fg="Black", text="Other Users Recommend:").grid(row=1)
        b = 2
        for u in range(0, len(names)):
            tk.Label(result_tab, font="Ariel 9", fg="Grey", text=names[u]).grid(row=b) # for each job name, display as a button with a link to each name by using static variable lambda ("lambda u=u:"")
            HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text="Enter", command = lambda u=u: [job.display(names[u], 1, ID_insert), both.closetab(result_tab)]).grid(row=b, column=1)
            b = b+2

        for name in names:
            handle = sql.connect("RecommendDATA.db") # getting all of the job ids for every job name that is in the array
            cursor = handle.cursor()
            cursor.execute("SELECT JOBID FROM JOBS WHERE JOBNAME LIKE ? AND IDLE = ?", ("%"+name+"%", 0))
            jobid = cursor.fetchall()
            jobid = str(jobid)
            jobid = jobid[2:len(jobid)-3] # formatting the tuple into a string
            jobid = int(jobid)
            handle.commit() 
            cursor.execute("INSERT INTO RECOMMEND VALUES(?,?)", (jobid, ID_insert))  # inserting the user id and job id into the recommended table
            handle.commit()
            handle.close()

            def mean(arr, postition):
                __all = 0
                for a in arr:
                    __all = __all + float(a[postition]) # calculating the mean by adding each piece of data into a total and then dividing into a mean
                return __all / len(arr)
                
            def sd(arr, postition, mean):
                __all = 0
                for b in arr:
                    __all = __all + (float(b[postition]) - mean)**2 # calculating the standard deviation within an array
                return (__all / len(arr))**0.5

            def algorithhm(array, idealcorrelation):
                handle = sql.connect("RecommendDATA.db")
                cursor = handle.cursor()
                allratings = []
                for x in range(0, 315):
                    cursor.execute("SELECT RATING FROM RATINGS WHERE JOBID = ? AND JOBID > ?", (x, 0))
                    rating = cursor.fetchall() # getting the ratings for every job in the datatabase
                    if rating == []:
                        allratings.append(3)
                    else:
                        for rate in rating:
                            rate = re.sub('[^0-9]', '', str(rate)) # , interpreting the output into a string
                            allratings.append(rate)
                length = len(allratings)
                handle.commit()
                allratings = re.sub('[^0-9]', '', str(allratings))
                total = 0
                for rate in allratings:
                    total = total + int(rate) # calculating the total and hence the mean rating of each job
                MeanRating = total / length

                cursor.execute("SELECT COUNT FROM JOBS")
                allcount = cursor.fetchall()
                length = len(allcount)
                handle.commit()
                handle.close() # selecting the count of each job which is the amount of recommendations the job has been given
                allcounts = 0
                for count in allcount:
                    count = str(count)
                    count = count[1:len(count)-2] # formatting of the count into an integer
                    if count == "'.'":
                        count = 0
                    count = int(count)
                    allcounts = allcounts + count # calculating the total recommendations and hence the mean views for all jobs combined
                MeanViews = allcounts / length

                info = []
                weight_arr = []
                weight_arr2 = []
                for jobname in array:
                    handle = sql.connect("RecommendDATA.db")
                    cursor = handle.cursor()
                    cursor.execute("SELECT JOBID FROM JOBS WHERE JOBNAME LIKE ? AND IDLE = ?", ("%"+jobname+"%", 0)) # for each job name in the array get the corresponding id integer
                    jobid = cursor.fetchall()
                    try:
                        jobid = str(jobid)
                        jobid = jobid[2:len(jobid)-3] # translating the tuple into an integer
                        jobid = int(jobid)
                        handle.commit()
                    except:
                        jobid = jobid.split(",") # if more than one job id is recieved
                        allids = []
                        if len(jobid) >= 3:
                            count = 0
                            odds = [1, 3, 5, 7, 8, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]
                            for ids in jobid:
                                ids = str(ids)
                                if count not in odds: # for every even iteration, remove the matching position of count (this is to remove unwanted pieces of data resulting from the split above)
                                    cont = True
                                else:
                                    if ids == " (256":
                                        jobid.remove(jobid[count-1]) # allow in this case specific;y as it is an outlier that contains an integer
                                    else:
                                        jobid.remove(jobid[count])
                                count += 1
                        for ids in jobid:
                            ids = re.sub('[^0-9]', '', str(ids)) # removing all but integers from a string
                            allids.append(ids)
                        lens = []
                        lens_sort = []
                        for ids in allids:
                            cursor.execute("SELECT JOBNAME FROM JOBS WHERE JOBID = ? AND IDLE = ?", (int(ids), 0))
                            name = cursor.fetchall()
                            name = str(name)
                            len1 = len(name) - len(jobname) # getting all of the job names back from the interpreted ids
                            lens.append(len1)
                            lens_sort.append(len1)
                        lens_sort.sort()
                        for p in range(0, len(lens_sort)):
                            if lens_sort[p] < 0:
                                lens_sort[p] = lens_sort[p] - lens_sort[p] - lens_sort[p] # making all of the items in that array positive (eg. -28 would go to 28)
                        for p in range(0, len(lens)):
                            if lens[p] < 0:
                                lens[p] = lens[p] - lens[p] - lens[p]             
                        for i in range(0, len(lens)):
                            if lens_sort[0] == lens[i]: # finding the appropriate id by finding the postition that matches in the array
                                position = i
                        jobid = allids[position]

                    cursor.execute("SELECT RATING FROM RATINGS WHERE JOBID = ? AND JOBID > ?", (jobid, 0))
                    ratings = cursor.fetchall() # select all of the ratings for a single job
                    handle.commit()
                    total = 0
                    ratings = re.sub('[^0-9]', '', str(ratings)) # remove all non-numeric characters
                    if ratings == " ":
                        total = 1
                    elif ratings == "": # if there is no ratings, set total to one
                        total = 1
                    else:
                        for rate in ratings:
                            total = total + int(rate) # collect all the ratings to form a total and then calculate the jobs average rating, this can be compared to the overall average ratings
                    try:
                        Rating = total / len(ratings)
                    except:
                        Rating = 3
                        
                    cursor.execute("SELECT COUNT FROM JOBS WHERE JOBID = ? AND JOBID > ?", (jobid, 0))
                    amount = cursor.fetchall()
                    handle.commit()
                    handle.close()
                    amount = re.sub('[^0-9]', '', str(amount)) # selecting the count of recommendations for that specfic job and then casting it to an integer
                    if amount == "":
                        amount = 0
                    Views = int(amount)
                    
                    m = MeanViews
                    v = Views
                    R = MeanRating
                    C = Rating
                    try:
                        weight1 = (v/m)*(R/v)
                        weight2 = (v/R)*(C/m) # performing a calculation to get numbers to rank each job against one another
                    except:
                        weight1 = (v+m)*(R+v)-25 # if dividing by 0 gives an error, use alterantive with reduced values to be less valued
                        weight2 = (v+R)*(C+m)-25
                    weight = weight1 + weight2 + (random.random()*2) # adding some random variables to it, so not static job recommendations depending on inputs (between 0-2 added to each weight)
                    weight_arr.append(weight)
                    weight_arr2.append(weight)
                    arr = [weight, jobid, jobname] # compiling all the job data into a new 2d array
                    info.append(arr)
                    
                #when weighted is identical integer, use total pythag distance for another statistic to use in the arrays
                for u in range(0, len(info)):
                    xval = info[u][0]
                    yval = info[u][1]
                    _all = 0
                    for v in range(0, len(info)):
                        xval2 = info[v][0] # x value is the weight
                        yval2 = info[v][1] # y value is the job id
                        changey = float(yval) - float(yval2) # find the difference of each x and y values, then use pythagoras theroum to find the eucliean distance
                        changex = float(xval) - float(xval2)
                        result = ((changex**2)+(changey**2))**0.5
                        _all = _all + result
                    info[u].append(_all)

            
                #cut down info list into top 20
                if len(info) > 20:
                    info2 = []
                    weights2 = []
                    weight_arr2.sort()
                    cut = weight_arr2[len(weight_arr2)-21] # the top 20 weight values are used to make the top 20 overall, by using a cut off point of a sorted place 21
                    for arr in info:
                        if cut < arr[0]:
                            info2.append(arr) # if its greater than the cut off point it's included in the following steps
                    info = info2

                def combinations(array, tuplelen, previous=[]): # previous is used to keep the last recursions array if incomplete
                    if len(previous) == tuplelen:
                        return [previous] # when enough values have been added, return the final array
                    combination = []
                    for i, val in enumerate(array): # iterate i and value so they both change depending on iteration counts
                        previous_afterappend = previous.copy() # append a new value to the previously used array
                        previous_afterappend.append(val)
                        combination = combination + [combinations(array[i+1:], tuplelen, previous_afterappend)] # appending the final array of combinations with the result of the last array to be returned 
                    return combination

                if len(info) < 7:
                    n = len(info) # if over 7, there are too many combinations for the program to run efficently
                else:
                    n = 7
                _all = []
                _all2 = []
                tests = []
                while n > 1:
                    hold = -11
                    all_combos = combinations(info, n) # function to find all of the combinations with a length of 7 at a maximum, this length decreases over iterations
                    meanx = mean(info, 0) # calculation of all the appropriate mean value for each variable
                    meany = mean(info, 1)
                    meanz = mean(info, 3)
                    sdx = sd(info, 0, meanx) # calculation of all the appropriate standard deviations for each variable
                    sdy = sd(info, 1, meany)
                    sdz = sd(info, 3, meanz)

                    allcorelations = []
                    for j in range(0, len(all_combos)):
                        totalx = 0
                        totaly = 0
                        totalz = 0
                        totalxyz = 0 # refreshing the variables between iterations
                        totalx2 = 0
                        totaly2 = 0
                        totalz2 = 0
                        cont = False
                        for k in range(0, len(all_combos[j])):
                            try:
                                xcord = float(all_combos[j][k][0])
                                xcord = xcord - meanx
                                xcord = xcord / sdx
                                ycord = float(all_combos[j][k][1]) # getting the difference from the mean for each cordinate and dividing by the standard deviation
                                ycord = ycord - meany
                                ycord = ycord / sdy
                                zcord = float(all_combos[j][k][3])
                                zcord = zcord - meanz
                                zcord = zcord / sdz
                                totalx = totalx + xcord
                                totaly = totaly + ycord # calculating some totals for all of the x/y/z coordinates
                                totalz = totalz + zcord
                                totalxyz = totalxyz + (ycord*xcord*zcord) # calculating a total of all of the coordinates combined
                                totalx2 = totalx2 + (xcord**2)
                                totaly2 = totaly2 + (ycord**2) # calculating some totals of the x/y/z coordinates squared
                                totalz2 = totalz2 + (zcord**2)
                            except:
                                cont = True
                        if cont == False:
                            numerator = (len(all_combos[j])*totalxyz)-(totalx*totaly*totalz) # implementing calaculation of the correlation by splitting into numerator and denowminator before combining them
                            denominator = ((len(all_combos[j])*totalx2)*(len(all_combos[j])*totaly2)*(len(all_combos[j])*totalz2))**0.5
                            r = numerator / denominator
                            if r < 0:
                                r = 0 - r # r is the coefficent that is calculated that is between 0 and 1 based on the strength of similarity between jobs
                            if hold < r:
                                hold = r
                            all_combos[j].append(r)
                            allcorelations.append(r) # recording outcomes of the calculations
                        else:
                            cont = True # placeholder
                    _all.append(allcorelations)
                    _all2.append(hold)
                    tests.append(all_combos)
                    n = n-1

                maximum = -2
                count = 0
                hold = 0
                for corelation in _all2:
                    if corelation > maximum: # out of all the correlations, iterate through them to find the highest possible number (the strongest posititve or negative correlation)
                        maximum = corelation
                        hold = count
                    count = count +1 
                saved_data = ""
                for g in range(0, len(tests[hold])):
                    for data in tests[hold][g]:
                        if data == maximum:
                            saved_data = tests[hold][g] # get the data that matches the highest correlation
                saved_data.remove(saved_data[len(saved_data)-1])

                eucleans = []
                for array in saved_data:
                    eucleans.append(array[3])
                eucleans.sort()
                x = 1
                allnames = []
                for x in range(0, len(eucleans)):
                    for array in saved_data:
                        if eucleans[x] == array[3]: # selecting all of the job names once they match with each of the eucliean distances so the names are sorted from start to finish by distance
                            allnames.append(array[2])

                return allnames
                
        names2 = algorithhm(joblist, 0)

        for jobname in names2:
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            cursor.execute("SELECT JOBID FROM JOBS WHERE JOBNAME LIKE ? AND IDLE = ?", ("%"+jobname+"%", 0)) # for each job name in the array get the corresponding id integer
            jobid = cursor.fetchall()
            try:
                jobid = str(jobid)
                jobid = jobid[2:len(jobid)-3] # translating the tuple into an integer
                jobid = int(jobid)
                handle.commit()
            except:
                jobid = jobid.split(",") # if more than one job id is recieved
                allids = []
                if len(jobid) >= 3:
                    count = 0
                    odds = [1, 3, 5, 7, 8, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35]
                    for ids in jobid:
                        ids = str(ids)
                        if count not in odds: # for every even iteration, remove the matching position of count (this is to remove unwanted pieces of data resulting from the split above)
                            cont = True
                        else:
                            if ids == " (256":
                                jobid.remove(jobid[count-1]) # allow in this case specific;y as it is an outlier that contains an integer
                            else:
                                jobid.remove(jobid[count])
                        count += 1
                for ids in jobid:
                    ids = re.sub('[^0-9]', '', str(ids)) # removing all but integers from a string
                    allids.append(ids)
                lens = []
                lens_sort = []
                for ids in allids:
                    cursor.execute("SELECT JOBNAME FROM JOBS WHERE JOBID = ? AND IDLE = ?", (int(ids), 0))
                    name = cursor.fetchall()
                    name = str(name)
                    len1 = len(name) - len(jobname) # getting all of the job names back from the interpreted ids
                    lens.append(len1)
                    lens_sort.append(len1)
                lens_sort.sort()
                for p in range(0, len(lens_sort)):
                    if lens_sort[p] < 0:
                        lens_sort[p] = lens_sort[p] - lens_sort[p] - lens_sort[p] # making all of the items in that array positive (eg. -28 would go to 28)
                for p in range(0, len(lens)):
                    if lens[p] < 0:
                        lens[p] = lens[p] - lens[p] - lens[p]             
                for i in range(0, len(lens)):
                    if lens_sort[0] == lens[i]: # finding the appropriate id by finding the postition that matches in the array
                        position = i
            jobid = allids[position]

        handle.commit()
        cursor.execute("INSERT INTO RECOMMEND VALUES(?,?)", (jobid, ID_insert)) # insert the user id and job ids into the recommended table
        handle.commit()
        handle.close()

        tk.Label(result_tab, font="Ariel 10", fg="Black", text=" ").grid(row=19)
        tk.Label(result_tab, font="Ariel 15", fg="Black", text="Statistical Recommendations:").grid(row=20) # creating the layout for the recommendations for the user to selecter their desired option
        b=21
        for p in range(0, len(names2)):
            tk.Label(result_tab, font="Ariel 9", fg="Grey", text=names2[p]).grid(row=b)
            HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text="Enter", command = lambda p=p: [job.display(names2[p], 1, ID_insert), both.closetab(result_tab)]).grid(row=b, column=1) # button that will redirect to the job page that the button label describes
            b = b+2
        var1 = IntVar()
        HoverButton(result_tab, activebackground='light blue', fg="White", bg="Black", text="Back", command = lambda: job.fieldq(ID_insert, result_tab)).grid(row=b+21, column=1)
        tk.Label(result_tab, font="Ariel 10", fg="Black", text=" ").grid(row=b+20)
        tk.Label(result_tab, font="Ariel 14", fg="Black", text="Feedback:").grid(row=b+21)
        tk.Radiobutton(result_tab, font="Ariel 11", text="Good", value=5, variable=var1).grid(row=b+22, columnspan=7) # these feedback options were unconnected from the functions as they aren't relevant to the job's, that is ultimately recommended, rating
        tk.Radiobutton(result_tab, font="Ariel 11", text="Bad", value=4, variable=var1).grid(row=b+33, columnspan=7)

    def display(self, job_name, countcheck, ID_insert):
        result_tab = ttk.Frame(tabcontrol)
        tabcontrol.add(result_tab, text=job_name)
        tabcontrol.select(result_tab)
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT EMPLOYEES FROM JOBS WHERE JOBNAME LIKE ? AND JOBID > ?", ("%"+job_name+"%", "0")) # selecting the data to see how many people work in America, in that specific role
        employees = cursor.fetchall()
        handle.commit()
        cursor.execute("SELECT JOBID FROM JOBS WHERE JOBNAME LIKE ? AND IDLE = ?", ("%"+job_name+"%", 0)) # selecting the job id from the job name, mainly to use to extract other pieces of information easier
        jobid = cursor.fetchall()
        if len(jobid) > 1:
            jobid = jobid[0]
        jobid = str(jobid)
        jobid = jobid[2:len(jobid)-3] # formatting to integers from a tuple
        handle.commit()
        try:
            cursor.execute("SELECT USERID FROM RECOMMEND WHERE JOBID LIKE ? AND JOBID > ?", (jobid, 0.1)) # collect all user ids that have been recommended this job
            userids = cursor.fetchall()
            handle.commit()
            for e in range(0, len(userids)):
                userids[e] = str(userids[e])
                userids[e] = userids[e][2:len(userids[e])-3] # for each user id, cast to an interger and all held within an array
            all_skills = []
            for p in range(0, len(userids)):
                cursor.execute("SELECT SKILL1, SKILL2, SKILL3 FROM USERS WHERE USERID LIKE ? AND USERID > ?", (userids[p], 0.1))
                user_skills = cursor.fetchall()
                handle.commit()
                user_skills = str(user_skills)
                user_skills = user_skills[2:len(user_skills)-2] # select all the skills from the users and formatting them appropriately
                user_skills = user_skills.split(",")
                for t in range(0, len(user_skills)):
                    if t >= 1:
                        user_skills[t] = user_skills[t][1:]
                    user_skills[t] = user_skills[t][1:len(user_skills[t])-1]
                    all_skills.append(user_skills[t])
            all_counts = []
            for y in range(0, len(all_skills)): # for every skill, count how many times it appears in the array to therefore find the most abundant skills
                count = 0
                for j in range(0, len(all_skills)):
                    if all_skills[y] == all_skills[j]:
                        count = count+1
                all_counts.append(count)
            all_counts.sort()
            topcount = all_counts[len(all_counts)-1]
            for y in range(0, len(all_skills)):
                count = 0
                for j in range(0, len(all_skills)): # perform the same operation again to see which skill name has the most repeats - that matches the amount recored in previous loop
                    if all_skills[y] == all_skills[j]:
                        count = count+1
                if count == topcount:
                    topskill = all_skills[y]
            top_skill = HoverButton(result_tab, activebackground='Light Blue', fg="Black", bg="White", text="Similar User Traits", command= lambda: job.sim_users(job_name, ID_insert)).grid(row=22, column=1) # 
        except:
            cont = True # placeholder
        if len(employees) > 1:
            employees = employees[0]
        cursor.execute("SELECT COUNT FROM JOBS WHERE JOBNAME LIKE ? AND JOBID > ?", ("%"+job_name+"%", "0"))
        count = cursor.fetchall()
        handle.commit()
        if len(count) > 1:
            count = count[0]
        count = str(count)
        count = re.sub("[^0-9]", "", count)
        if count == "":
            count = 1
        else:
            try:
                count=int(count)
                if countcheck == 1:
                    count = count+1
            except:
                count = "N/A"
        rec_count = count
        rec_count = str(rec_count)
        rec_count = "Amount of suggestions: "+rec_count
        tk.Label(result_tab, text=rec_count, font= "Ariel 11 italic").grid(row=20, column=1)
        cursor.execute("UPDATE JOBS SET COUNT = ? WHERE JOBNAME LIKE ? AND JOBID > ?", (count, "%"+job_name+"%", "0"))
        handle.commit()
        employees = str(employees)
        employees = re.sub("[^0-9]", "", employees)
        employees = employees[2:]
        if employees[:2] == "72":
            employees = employees[2:]
        if employees == "":
            employees = "uncounted quantity of"
        tk.Label(result_tab, text="Job:", font= "Ariel 12", fg="Dark Blue").grid(row=4)
        tk.Label(result_tab, text="Field:", font= "Ariel 12", fg="Dark Blue").grid(row=11)
        tk.Label(result_tab, text="Extras:", font= "Ariel 12", fg="Dark Blue").grid(row=15)
        breaktext = len(job_name)*"-"
        employees = str(employees)
        employees = employees+" people employed in this role."
        tk.Label(result_tab, text=employees, font= "Ariel 11 italic").grid(row=10, column=1)
        cursor.execute("SELECT DESCRIPTION FROM JOBS WHERE JOBNAME LIKE ? AND JOBID > ?", ("%"+job_name+"%", "0"))
        descript = cursor.fetchall()
        handle.commit()
        if len(descript) > 1:
            descript = descript[0]
        descript = str(descript)
        descript = descript[3:len(descript)-4]
        descript = descript.strip()
        descript = descript.replace("Expand", "")
        descript = descript.strip()
        try:
            des_test = "'"+descript[0]+"'"
            hold = "'\\'"
            if des_test == hold:
                descript = descript[12:]
        except:
            cont = True    
        cursor.execute("SELECT SALARY FROM JOBS WHERE JOBNAME LIKE ? AND JOBID > ?", ("%"+job_name+"%", "0"))
        salary = cursor.fetchall()
        handle.commit()
        if len(salary) > 1:
            salary = salary[0]
        salary = str(salary)
        salary = re.sub("[^0-9]", "", salary)
        number_hold = salary
        salary = "$"+salary
        HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text=salary, command = lambda: job.currency(number_hold, result_tab, job_name, salary, ID_insert)).grid(row=6, column=1)
        HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text="DESCRIPTION", command = lambda: [job.displaydescript(descript, job_name, ID_insert), both.closetab(result_tab)]).grid(row=7, column=1)
        cursor.execute("SELECT SKILLS FROM JOBS WHERE JOBNAME LIKE ? AND JOBID > ?", ("%"+job_name+"%", "0"))
        skill = cursor.fetchall()
        handle.commit()
        if len(skill) > 1:
            skill = skill[0]
        punctuation = """!"#$%&'(\/)*+:;=?@[]^_`{|}~"""
        skills = ""
        string = str(skill)
        for i in string:
            if i not in punctuation:
                skills += i
        skills = skills.split(".,")
        var = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvxyz")
        none = False
        if skills[0] == "none,":
            none = True
        if none == False:
            HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text="SKILLS", command = lambda: job.displayskills(skills, var, job_name, result_tab, ID_insert)).grid(row=8, column=1)
        cursor.execute("SELECT FIELD FROM JOBS WHERE JOBNAME LIKE ? AND JOBID > ?", ("%"+job_name+"%", "0"))
        field = cursor.fetchall()
        handle.commit()
        if len(field) > 1:
            field = field[0]
        field = str(field)
        field = field[2:len(field)-5]
        try:
            while field[0].upper() != field[0]:
                field = field[1:]
            if field[0] == "'":
                field = field[1:len(field)-1]
        except:
            cont = True
        tk.Label(result_tab, text=field, font= "Ariel 11 italic").grid(row=12, column=1)
        HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text="Field Info", command = lambda: job.field_info(result_tab, field, job_name, ID_insert)).grid(row=13, column=1)
        tk.Label(result_tab, text=" ", font= "Ariel 12 italic").grid(row=14, column=1)
        HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text="SEARCH FOR LISTINGS", command = lambda: job.listingsearch(result_tab, job_name, ID_insert)).grid(row=16, column=1)
        HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text="Qual Split", command = lambda: job.qual_split(job_name)).grid(row=17, column=1)
        HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text="Create recommendation file (PDF)", command = lambda: job.RECtemplate(job_name, result_tab, field, descript, skills, salary, ID_insert)).grid(row=18, column=1)
        HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text="SIMILAR JOBS", command = lambda: job.similar_jobs(field, job_name, result_tab, ID_insert)).grid(row=19, column=1)
        HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text="Rate this job", command = lambda: job.ratingadd(job_name, result_tab, ID_insert)).grid(row=21, column=1)
        HoverButton(result_tab, activebackground='Blue', fg="Blue", bg="White", text="MAIN MENU", command = lambda: job.mainmenu(ID_insert)).grid(row=25)
        HoverButton(result_tab, activebackground='Blue', fg="Blue", bg="White", text="CLOSE TAB", command = lambda: both.closetab(result_tab)).grid(row=27)

    def sim_users(self, job_name, ID_insert):
        similarusers = ttk.Frame(tabcontrol)
        tabcontrol.add(similarusers, text="SIMILAR USER TRAITS")
        tabcontrol.select(similarusers)
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT JOBID FROM JOBS WHERE JOBNAME LIKE ? AND IDLE = ?", ("%"+job_name+"%", 0))
        jobid = cursor.fetchall()
        if len(jobid) > 1:
            jobid = jobid[0]
        jobid = str(jobid)
        jobid = jobid[2:len(jobid)-3]
        handle.commit()
        cursor.execute("SELECT USERID FROM RECOMMEND WHERE JOBID LIKE ? AND JOBID > ?", (jobid, 0.1))
        userids = cursor.fetchall()
        handle.commit()
        for e in range(0, len(userids)):
            userids[e] = str(userids[e])
            userids[e] = userids[e][2:len(userids[e])-3]
        all_skills = []
        for p in range(0, len(userids)):
            cursor.execute("SELECT SKILL1, SKILL2, SKILL3 FROM USERS WHERE USERID LIKE ? AND USERID > ?", (userids[p], 0.1))
            user_skills = cursor.fetchall()
            handle.commit()
            user_skills = str(user_skills)
            user_skills = user_skills[2:len(user_skills)-2]
            user_skills = user_skills.split(",")
            for t in range(0, len(user_skills)):
                if t >= 1:
                    user_skills[t] = user_skills[t][1:]
                user_skills[t] = user_skills[t][1:len(user_skills[t])-1]
                all_skills.append(user_skills[t])
        all_counts = []
        for y in range(0, len(all_skills)):
            count = 0
            for j in range(0, len(all_skills)):
                if all_skills[y] == all_skills[j]:
                    count = count+1
            all_counts.append(count)
        all_counts.sort()
        topcount = all_counts[len(all_counts)-1]
        for y in range(0, len(all_skills)):
            count = 0
            for j in range(0, len(all_skills)):
                if all_skills[y] == all_skills[j]:
                    count = count+1
            if count == topcount:
                topskill = all_skills[y]
        all_non_duplicated_skills = []
        nums = []
        for l in range(0, len(all_skills)):
            if all_skills[l] not in all_non_duplicated_skills:
                all_non_duplicated_skills.append(all_skills[l])
        for y in range(0, len(all_non_duplicated_skills)):
            count = 0
            for j in range(0, len(all_skills)):
                if all_non_duplicated_skills[y] == all_skills[j]:
                    count = count+1
            nums.append(count)
        HoverButton(similarusers, activebackground='blue', fg="white", bg="black", text="Skill Split", command = lambda: job.skillsplit(all_non_duplicated_skills, nums, ID_insert)).grid(row=3)
        tk.Label(similarusers, text =job_name).grid(row=1)
        tk.Label(similarusers, text ="Top Skill: ").grid(row=2)
        tk.Label(similarusers, text =topskill).grid(row=2, column=1)
        HoverButton(similarusers, activebackground='blue', fg="white", bg="black", text ="Back", command = lambda: both.closetab(similarusers)).grid(row=15)

    def skillsplit(self, all_non_duplicated_skills, nums, ID_insert):
        try:
            import matplotlib.pyplot as plt
            import numpy as np
        except:
            cont = True
        labels = all_non_duplicated_skills
        sizes = nums
        explode = [0.5]*len(sizes)
        fig1, ax1 = plt.subplots()
        ax1.pie(nums, explode=explode, labels=all_non_duplicated_skills, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')
        plt.suptitle("Skill Split", fontsize = 22)
        plt.show()
        
    def displaydescript(self, descript, job_name, ID_insert):
        result_tab = ttk.Frame(tabcontrol)
        tabcontrol.add(result_tab, text="JOB DESCRIPTION")
        tabcontrol.select(result_tab)
        count = 0
        count2 = 0
        count3 = []
        for char in descript:
            count2 +=1
            if char == " ":
                count3.append(count2-1)
                count+=1
        if len(count3) >= 10 and len(count3) <= 19:
            tk.Label(result_tab, text=descript[:count3[9]]).grid(row=3, columnspan=7)
            tk.Label(result_tab, text=descript[count3[9]+1:]).grid(row=4, columnspan=7)
        elif len(count3) > 19:
            tk.Label(result_tab, text=descript[:count3[9]]).grid(row=3, columnspan=7)
            tk.Label(result_tab, text=descript[count3[9]+1:count3[18]]).grid(row=4, columnspan=7)
            tk.Label(result_tab, text=descript[count3[18]+1:]).grid(row=5, columnspan=7)
        else:
            tk.Label(result_tab, text=descript).grid(row=3)
        tk.Label(result_tab, font="Ariel 15", fg="Light Blue", text="Description: ").grid(row=1, columnspan=7)
        tk.Label(result_tab, text=" ").grid(row=2)
        tk.Label(result_tab, text=" ").grid(row=19)
        HoverButton(result_tab, activebackground='Light Blue', fg="white", bg="black", text="Back", command = lambda: [both.closetab(result_tab), job.display(job_name, 0, ID_insert)]).grid(row=20, columnspan=7)
   
    def RECtemplate(self, job_name, result_tab, field, descript, skills, salary, ID_insert):
        try:
            from fpdf import FPDF
            file_handle = job_name+".pdf"
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=8)
            pdf.cell(200, 10, txt=job_name, ln=1, align="C")
            pdf.cell(200, 10, txt=salary, ln=1, align="L")
            field_content = "Field: "+field
            pdf.cell(200, 10, txt=field_content, ln=3, align="L")
            pdf.cell(200, 10, txt=descript, ln=5, align="L")
            linesplit = 0
            condition = ['none,']
            if skills != condition:
                pdf.cell(200, 10, txt="Skills:", ln=7, align="L")
                pdf.set_font("Arial", size=6)
                for c in range(0, len(skills)):
                    pdf.cell(200, 10, txt=skills[c], ln=linesplit+8, align="L")
                    linesplit = linesplit+2
            pdf.output(file_handle, "F")
            tk.Message(result_tab, text="File Created, Should be in the same folder as this file.").grid(row=8, column=1)
        except:
            tk.Message(result_tab, text="File error, file could not be produced.").grid(row=8, column=1)
        
    def similar_jobs(self, field, job_name, result_tab, ID_insert):
        result_tab.destroy()
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT JOBNAME FROM JOBS WHERE FIELD LIKE ? AND JOBID > ?", ("%"+field+"%", "0"))
        joblist = cursor.fetchall()
        handle.commit()
        fin = []
        for b in range(0, len(joblist)):
            punctuation = """!"#$%&'()*+:;<=>?@[]^`{|}~"""
            string = str(joblist[b])
            new = ""
            for i in string:
                if i not in punctuation:
                    new = new+i
            new = new[:len(new)-2]
            fin.append(new)
        for v in range(0, len(fin)):
            fin[v] = fin[v].rstrip('\\')
        fin.remove(job_name)
        cursor.execute("SELECT QUALLEVEL FROM JOBS WHERE JOBNAME LIKE ? AND JOBID > ?", ("%"+job_name+"%", "0"))
        quals = cursor.fetchall()
        handle.commit()
        if len(quals)>1:
            quals = quals[1]
        nameofqual = job.findcommonqual(quals)
        final = []
        for i in range(0, len(fin)):
            cursor.execute("SELECT QUALLEVEL FROM JOBS WHERE JOBNAME LIKE ? AND JOBID > ?", ("%"+fin[i]+"%", "0"))
            jobqual = cursor.fetchall()
            handle.commit()
            jobqualname = job.findcommonqual(jobqual)
            if jobqualname == nameofqual:
                final.append(fin[i])
        if final == []:
            while len(fin) > 5:
                fin.remove(fin[random.randint(0, len(fin)-1)])
            final = fin
        similar_tab = ttk.Frame(tabcontrol)
        tabcontrol.add(similar_tab, text="Similar Jobs")
        tabcontrol.select(similar_tab)
        var3 = StringVar()
        var3.set(fin[random.randint(0, len(fin)-1)])
        tk.Label(similar_tab, text ="Similar roles: ").grid(row=2, column=4)
        tk.OptionMenu(similar_tab, var3, *fin).grid(row=2, column=5)
        HoverButton(similar_tab, activebackground='blue', fg="white", bg="black", text="Continue", command = lambda: [job.var3confirm(var3, ID_insert), both.closetab(similar_tab)]).grid(row=3)
        HoverButton(similar_tab, activebackground='blue', fg="white", bg="black", text="Back", command = lambda: [job.display(job_name, 0, ID_insert), both.closetab(similar_tab)]).grid(row=4)

    def var3confirm(self, var3, ID_insert):
        job_name = var3.get()
        job.display(job_name, 0, ID_insert)
        
    def ratingadd(self, job_name, result_tab, ID_insert):
        result_tab.destroy()
        result_tab = ttk.Frame(tabcontrol)
        title = "Rate " + job_name
        tabcontrol.add(result_tab, text=title)
        tabcontrol.select(result_tab)
        one_to_five = [1, 2, 3, 4, 5]
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT JOBID FROM JOBS WHERE JOBNAME LIKE ? AND JOBID > ?", ("%"+job_name+"%", 0))
        jobid = cursor.fetchall()
        jobid = re.sub('[^0-9]', '', str(jobid))
        cursor.execute("SELECT RATING FROM RATINGS WHERE JOBID = ? AND JOBID > ?", (jobid, 0))
        ratings = cursor.fetchall()
        handle.commit()
        handle.close()
        total = 0
        ratings = re.sub('[^0-9]', '', str(ratings))
        try:
            for rate in ratings:
                total = total + int(rate)
            total = total / len(ratings)
        except:
            total = 3
        average = total
        average = str(average)
        av_rate = "Average rating: " + average
        tk.Label(result_tab, text =av_rate).grid(row=1, column=5)
        stars = IntVar()
        stars.set(3)
        tk.Label(result_tab, text ="Rating: ").grid(row=2, column=4)
        tk.OptionMenu(result_tab, stars, *one_to_five).grid(row=2, column=5)
        tk.Label(result_tab, text ="Comment: ").grid(row=3, column=4)
        comment = tk.Entry(result_tab)
        comment.grid(row=3, column=5)
        HoverButton(result_tab, activebackground='blue', fg="white", bg="black", text="Back", command = lambda: [job.display(job_name, 0, ID_insert), both.closetab(result_tab)]).grid(row=5, column=4)
        HoverButton(result_tab, activebackground='blue', fg="white", bg="black", text="Enter", command = lambda: job.ratingadd2(job_name, comment, stars, result_tab, ID_insert)).grid(row=5, column=5)

    def ratingadd2(self, job_name, comment, stars, result_tab, ID_insert):
        stars_ = stars.get()
        comment_ = comment.get()
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT JOBID FROM JOBS WHERE JOBNAME LIKE ? AND IDLE = ?", ("%"+job_name+"%", 0))
        jobID = cursor.fetchall()
        handle.commit()
        if len(jobID) > 1:
            jobID = jobID[1]
        jobID = str(jobID)
        jobID = jobID[2:len(jobID)-3]
        cursor.execute("INSERT INTO RATINGS VALUES(?,?,?)", (jobID, stars_, comment_))
        handle.commit()
        handle.close()
        result_tab.destroy()
        job.display(job_name, 0, ID_insert)
        
    def qual_split(self, job_name):
        try:
            import matplotlib.pyplot as plt
            import numpy as np
        except:
            cont = True
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT QUALLEVEL FROM JOBS WHERE JOBNAME LIKE ? AND JOBID > ?", ("%"+job_name+"%", "0"))
        qualforjob = cursor.fetchall()
        handle.commit()
        handle.close()
        qualforjob = str(qualforjob)
        qualforjob = qualforjob.split("'")
        del qualforjob[::2]
        quals = []
        for h in range(0, len(qualforjob)):
            punctuation = """!"#$%&'()*+-/:;=?@[\\]^_`{|}~"""
            edited = ""
            string = str(qualforjob[h])
            for i in string:
                if i not in punctuation:
                    edited += i
                if edited == "High School DiplomaGED":
                    edited = edited[:-3]
                if edited == " High School Diploma":
                    #removing first space
                    edited = edited[1:]
            quals.append(edited)
        length = len(quals)/2
        length = int(length)
        repeat = 0
        names = []
        nums = []
        for i in range(0, length):
            names.append(quals[repeat])
            nums.append(quals[repeat+1])
            repeat = repeat+2
        labels = names
        sizes = nums
        explode = [0.5]*len(sizes)
        fig1, ax1 = plt.subplots()
        ax1.pie(nums, explode=explode, labels=names, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')
        plt.suptitle("Quallevel Split", fontsize = 22)
        plt.show()
        
    def field_info(self, result_tab, field, job_name, ID_insert):
        result_tab.destroy()
        fieldinfo_tab = ttk.Frame(tabcontrol)
        tabcontrol.add(fieldinfo_tab, text="Field Info")
        tabcontrol.select(fieldinfo_tab)
        tk.Label(fieldinfo_tab, text=field).grid(row=1)
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT COUNT FROM JOBS WHERE IDLE = ? AND FIELD LIKE ?", (0, "%"+field+"%"))
        counts = cursor.fetchall()
        handle.commit()
        total_count = 0
        for i in range(0, len(counts)):
            try:
                counts[i] = str(counts[i])
                counts[i] = counts[i][1:len(counts[i])-2]
                counts[i] = int(counts[i])
                total_count = total_count + counts[i]
            except:
                cont = True
        total_count = str(total_count)
        total_count = re.sub("[^0-9]", "", total_count)
        total_count = "Total field-wide suggestions: " + total_count
        tk.Label(fieldinfo_tab, text=total_count).grid(row=2)

        cursor.execute("SELECT JOBNAME FROM JOBS WHERE IDLE = ? AND FIELD LIKE ?", (0, "%"+field+"%"))
        names = cursor.fetchall()
        handle.commit()
        all_names = []
        for name in names:
            name = str(name)
            name = name[2:len(name)-5]
            all_names.append(name)
        vars_ = StringVar()
        vars_.set(all_names[random.randint(0, len(all_names)-1)])
        tk.Label(fieldinfo_tab, text="All jobs in the field:").grid(row=3)
        tk.OptionMenu(fieldinfo_tab, vars_, *all_names).grid(row=4)
        HoverButton(fieldinfo_tab, activebackground='blue', fg="white", bg="black", text="Confirm", command = lambda: [both.closetab(fieldinfo_tab), job.display(vars_.get(), 0, ID_insert)]).grid(row=4, column=1)
        handle.close()
        HoverButton(fieldinfo_tab, activebackground='blue', fg="white", bg="black", text="Back", command = lambda: [both.closetab(fieldinfo_tab), job.display(job_name, 0, ID_insert)]).grid(row=10, column=1)
        
    def currency(self, number_hold, result_tab, job_name, salary, ID_insert):
        result_tab.destroy()
        urlof_live = "https://transferwise.com/gb/currency-converter/usd-to-~-rate?amount=#"
        urlof_live = urlof_live.replace("#", number_hold)
        currency_tab = ttk.Frame(tabcontrol)
        tabcontrol.add(currency_tab, text="Currency Change")
        tabcontrol.select(currency_tab)
        tk.Label(currency_tab, text = salary).grid(row=2)
        list_of_currency = ["GBP", "INR", "ISK", "CAD", "EUR", "SDG", "AUD", "MXN", "SEK", "NOK", "JPY", "BRL"]
        vars_ = StringVar()
        vars_.set(list_of_currency[random.randint(0, len(list_of_currency)-1)])
        tk.OptionMenu(currency_tab, vars_, *list_of_currency).grid(row=3)
        HoverButton(currency_tab, activebackground='blue', fg="white", bg="black", text="Confirm", command = lambda: job.use_currency(urlof_live, currency_tab, job_name, number_hold, vars_, ID_insert, salary)).grid(row=4)
        HoverButton(currency_tab, activebackground='blue', fg="white", bg="black", text="Back", command = lambda: [both.closetab(currency_tab), job.display(job_name, 0, ID_insert)]).grid(row=4, column=1)

    def use_currency(self, urlof_live, currency_tab, job_name, number_hold, vars_, ID_insert, salary):
        currency_tab.destroy()
        vars_ = vars_.get()
        vars2 = vars_
        try:
            vars_ = vars_.lower()
            urlof_live = urlof_live.replace("~", vars_)
            try:
                from bs4 import BeautifulSoup # modules that allow access to html parser of any url
                import requests
            except:
                cont = True
            response = requests.get(urlof_live) # request to the website for access
            soup = BeautifulSoup(response.content, "html.parser") # gathering the html file
            soup.prettify() # cleaning the html file
            sal = soup.find("div", {"class": "col-xs-12 col-md-6 text-xs-center"}).text
            new_sal = ""
            for y in range(0, len(sal)):
                try:
                    int(sal[y])
                    new_sal = new_sal+sal[y]
                    if sal[y+1] == ".":
                        new_sal = new_sal+sal[y+1]
                except:
                    cont = True
            sal = new_sal[2:len(new_sal)-4]
            sal = float(sal)
            number_hold = float(number_hold)
            sal = sal*number_hold
            sal = str(sal)
            vars_ = vars_.upper()
            sal = sal + " " + vars_
        except:
            statics = {"GBP":0.77, "INR":73.48,"ISK":127.27, "CAD":1.34, "EUR":0.89, "SDG":55.25, "AUD":1.52, "MXN":19.75, "SEK":9.46, "NOK":9.28, "JPY":106.83, "BRL":4.63}
            salary = salary[1:]
            sal = int(salary) * statics[vars2]
        currency_tab2 = ttk.Frame(tabcontrol)
        tabcontrol.add(currency_tab2, text="Currency Result")
        tabcontrol.select(currency_tab2)
        tk.Label(currency_tab2, text = sal).grid(row=1)
        tk.Label(currency_tab2, text = vars_).grid(row=1, column=1)
        HoverButton(currency_tab2, activebackground='blue', fg="white", bg="black", text="Back", command = lambda: [both.closetab(currency_tab2), job.display(job_name, 0, ID_insert)]).grid(row=2)
        
    def listingsearch(self, result_tab, job_name, ID_insert):
        result_tab.destroy()
        f = open("adaptive-listings.txt")
        name = []
        url = []
        rep = []
        for i in range(0, 1):
            temp = f.readline()
            temp = str(temp)
            temp = temp[:len(temp)-1]
            name.append(temp)
            temp = f.readline()
            temp = str(temp)
            temp = temp[:len(temp)-1]
            url.append(temp)
            temp = f.readline()
            temp = str(temp)
            temp = temp[:len(temp)-1]
            rep.append(temp)
        job.listings_(job_name, name, url, rep, ID_insert)
        
    def copytoclip(self, url):
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(url)
        r.update()
        r.destroy()
        
    def listings_(self, job_name, name, url, rep, ID_insert):
        VAR = "Indeed"
        pos = []
        for c in range(0, len(name)):
            if VAR == name[c]:
                pos.append(c)
        c = pos[0]
        url = url[c]
        name = name[c]
        rep = rep[c]
        hold = job_name
        job_name = job_name.replace(" ", rep)
        job_name = job_name.replace("\\", " ")
        job_name = job_name.replace("/", " ")
        job_name = job_name.replace("-", " ")
        job_name = job_name.replace(",", " ")
        url = url.replace("~", job_name)
        job.listingmenu(url, hold, VAR, ID_insert)

    def listingmenu(self, url, hold, VAR, ID_insert):
        try:
            from bs4 import BeautifulSoup # modules that allow access to html parser of any url
            import requests
        except:
            cont = True
        response = requests.get(url) # request to the website for access
        soup = BeautifulSoup(response.content, "html.parser") # gathering the html file
        soup.prettify() # cleaning the html file
        no_result_test = soup.findAll("div", {"class": "bad_query"})
        if no_result_test != []:
            skill_tab = ttk.Frame(tabcontrol)
            tabcontrol.add(skill_tab, text="No Results")
            tabcontrol.select(skill_tab)
            HoverButton(skill_tab, activebackground='blue', fg="white", bg="black", text="Back", command = lambda: [both.closetab(skill_tab), job.display(hold, 0, ID_insert)]).grid(row=2)
        else:
            try:
                namesofjobs = soup.findAll("div", {"class": "title"})
                locationsofjobs = soup.findAll("div", {"class": "recJobLoc"})
                href = soup.findAll("div", {"class": "title"})
            except:
                carryerror = True
            hrefs = []
            for div in href:
                link = div.find("a")["href"]
                link = "https://www.indeed.co.uk"+link
                hrefs.append(link)
            locationsofjobs = str(locationsofjobs)
            locationsofjobs = locationsofjobs.split("=")
            locations = []
            for u in range(0, len(locationsofjobs)):
                if locationsofjobs[u][0] == '"':
                    locations.append(locationsofjobs[u])
            del locations [::2]
            newlocations = locations
            all_location = []
            try:
                for k in range(0, len(locations)-1):
                    if locations[k][len(locations[k])-2:] == "id":
                        locations[k] = locations[k][1:len(locations[k])-4]
                        all_location.append(locations[k])
            except:
                cont = True
            namesofjobs = str(namesofjobs)
            namesofjobs = namesofjobs.split('title="')
            jobnames = []
            for p in range(0, len(namesofjobs)):
                cont = True
                string = ""
                for char in namesofjobs[p]:
                    if char == '"':
                        cont = False
                    if cont == True:
                        string = string+char
                jobnames.append(string)
            jobnames.remove(jobnames[0])
            jobresults = ttk.Frame(tabcontrol)
            tabcontrol.add(jobresults, text="Results")
            tabcontrol.select(jobresults)
            count = 1
            allnames = []
            while len(jobnames) > 18:
                jobnames.remove(jobnames[len(jobnames)-1])
            for x in range(0, len(jobnames)):
                jobnames[x] = jobnames[x] + " --- " + all_location[x]
                allnames.append(jobnames[x])
                HoverButton(jobresults, activebackground='blue', fg="white", bg="black", text=jobnames[x], command = lambda x=x: [job.joblisting_indeed(hold, hrefs, jobnames, jobnames[x], ID_insert), both.closetab(jobresults)]).grid(row=count+1, columnspan=7)
                count = count+2
            tk.Label(jobresults, text = "Select position of interest: ").grid(row=1, columnspan=7)
            HoverButton(jobresults, activebackground='blue', fg="Black", bg="White", text="BACK", command = lambda: [job.display(hold, 0, ID_insert), both.closetab(jobresults)]).grid(row=count+10, columnspan=7)

    def joblisting_indeed(self, hold, hrefs, jobnames, jobname, ID_insert):
        listname = jobname
        for g in range(0, len(jobnames)):
            if listname == jobnames[g]:
                href = hrefs[g]
        list_tab = ttk.Frame(tabcontrol)
        tabcontrol.add(list_tab, text="Listing")
        tabcontrol.select(list_tab)
        tk.Label(list_tab, text = listname, fg="Blue").grid(row=1, columnspan=3)
        HoverButton(list_tab, activebackground='blue', fg="white", bg="black", text="Copy URL to Clipboard", command = lambda: job.copytoclip(href)).grid(row=2, column=1)
        HoverButton(list_tab, activebackground='blue', fg="white", bg="black", text="Open URL", command = lambda: job.openurl(href)).grid(row=3, column=1)
        HoverButton(list_tab, activebackground='blue', fg="white", bg="black", text="Back", command = lambda: [job.display(hold, 0, ID_insert), both.closetab(list_tab)]).grid(row=4, column=1)

    def openurl(self, href):
        try:
            import webbrowser
        except:
            cont = True
        webbrowser.open(href)
        
    def displayskills(self, skills, var, job_name, result_tab, ID_insert):
        result_tab.destroy()
        skill_tab = ttk.Frame(tabcontrol)
        tabcontrol.add(skill_tab, text="JOB SKILLS")
        tabcontrol.select(skill_tab)
        r = 0
        for n in range(0, len(skills)-1):
            spaces = []
            iterate = 0
            for char in skills[n]:
                if char == " ":
                    spaces.append(iterate)
                iterate+=1
            if len(spaces) >= 10 and len(spaces) <= 19:
                tk.Label(skill_tab, font="Verdana 7", text=skills[n][:spaces[9]]).grid(row=r+3, column=7)
                tk.Label(skill_tab, font="Verdana 7", text=skills[n][spaces[9]+1:]).grid(row=r+4, column=7)
            elif len(spaces) > 19:
                tk.Label(skill_tab, font="Verdana 7", text=skills[n][:spaces[9]]).grid(row=r+3, column=7)
                tk.Label(skill_tab, font="Verdana 7", text=skills[n][spaces[9]+1:spaces[18]]).grid(row=r+4, column=7)
                tk.Label(skill_tab, font="Verdana 7", text=skills[n][spaces[18]+1:]).grid(row=r+5, column=7)
            else:
                tk.Label(skill_tab, font="Verdana 7", text=skills[n]).grid(row=r+3, column=7)
            r = r+6
            tk.Label(skill_tab, font="Ariel 5", text=" ").grid(row=r)
        HoverButton(skill_tab, activebackground='blue', fg="white", bg="black", text="BACK", command = lambda: [job.display(job_name, 0, ID_insert), both.closetab(skill_tab)]).grid(row=r+7, columnspan=10)
                                                                                        
    def search(self, searchjobentry, tab1, ID_insert):
        #search in database word by word of each job and use LIKE and % wildcards to widen critera. If no results, option to add a job to be reviewed.
        searchjobentry = searchjobentry.get()
        searchjobentry = searchjobentry.split(" ")
        results = []
        for c in range(0, len(searchjobentry)):
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            cursor.execute("SELECT JOBNAME FROM JOBS WHERE JOBNAME LIKE ? AND IDLE = ?", ("%"+searchjobentry[c]+"%", 0))
            jobnames = cursor.fetchall()
            handle.commit()
            handle.close()
            results.append(jobnames)
        if results == [[]]:
            job.missingjob1(tab1, ID_insert)
        else:
            tab1.destroy()
            job.searchmenu(results, ID_insert)

    def searchmenu(self, results, ID_insert):
        results = results[0]
        punctuation = """!"#$%&'()*+:;=?@[]^_`{|'}~"""
        new = ""
        string = str(results)
        for i in string:
            if i not in punctuation:
                new += i
        new = new.split(",,")
        for t in range(0, len(new)):
            new[t] = new[t][:len(new[t])-1]
        new[len(new)-1] = new[len(new)-1][:len(new[t])-1]
        variables = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        while len(new) > 1:
            new.remove(new[random.randint(0, len(new)-1)])
        job_name = new[0]
        a = True
        try:
            if job_name[0] == " ":
                job_name = job_name[1:]
            if job_name[len(job_name)-1] == "\\":
                job_name = job_name[:len(job_name)-1]
        except:
            tab1 = ttk.Frame(tabcontrol)
            a = False
            job.missingjob1(tab1, ID_insert)
        if a == True:
            job.display(job_name, 0, ID_insert)

    def deletealltabs(self, variables, new):
        for u in range(0, len(new)):
            variables[u].destroy()
        
    def missingjob1(self, tab1, ID_insert):
        tab1.destroy()
        #give options 
        missing = ttk.Frame(tabcontrol)
        tabcontrol.add(missing, text="ADD JOB")
        tabcontrol.select(missing)
        tk.Label(missing, font="Verdana 17", fg="Black", text="THERE WAS NO FOUND JOBS").grid(row=1, columnspan=7)
        tk.Label(missing, font="Verdana 15", fg="Black", text="add a job to be reviewed by an Admin.").grid(row=2, columnspan=7)
        tk.Label(missing, font="Verdana 12 italic", fg="Black", text="JOBNAME:").grid(row=4)
        JOB__name = tk.Entry(missing, font="Verdana 11", fg="Black")
        JOB__name.grid(row=4, column=1)
        tk.Label(missing, font="Verdana 12 italic", fg="Black", text="DESCRIPTION:").grid(row=6)
        JOB__des = tk.Entry(missing, font="Verdana 11", fg="Black")
        JOB__des.grid(row=6, column=1)
        tk.Label(missing, font="Verdana 12 italic", fg="Black", text="FIELD:").grid(row=8)
        JOB__field = tk.Entry(missing, font="Verdana 11", fg="Black")
        JOB__field.grid(row=8, column=1)
        HoverButton(missing, activebackground='Light Blue', fg="white", bg="Blue", text="Back", command = lambda: [both.closetab(missing), job.mainmenu(ID_insert)]).grid(row=10)
        HoverButton(missing, activebackground='Light Blue', fg="white", bg="black", text="Confirm", command = lambda: job.missingjob2(JOB__name, missing, JOB__des, JOB__field, ID_insert)).grid(row=10, column=1)
        tk.Label(missing, font="Verdana 15", fg="Black", text=" ").grid(row=3, column=6)
        tk.Label(missing, font="Verdana 15", fg="Black", text=" ").grid(row=5, column=5)
        tk.Label(missing, font="Verdana 15", fg="Black", text=" ").grid(row=7, column=4)
        tk.Label(missing, font="Verdana 15", fg="Black", text=" ").grid(row=9, column=3)
        
    def missingjob2(self, JOB__name, missing, JOB__des,  JOB_field, ID_insert):
        #add info from missingjob1 into database to be reviewed by an admin (aka. me)
        JOB_field = JOB_field.get()
        JOB__name = JOB__name.get()
        JOB__des = JOB__des.get()
        missing.destroy()
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("INSERT INTO USER_RECOMMENDATIONS VALUES(?,?,?)", (JOB__name, JOB__des, JOB_field))
        handle.commit()
        handle.close()
        job.mainmenu(ID_insert)
        
    def popular(self, tab1, ID_insert):
        tab1.destroy()
        # uses count of recommendations for each job
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT COUNT FROM JOBS")
        counts = cursor.fetchall()
        handle.commit()
        handle.close()
        counts_array = []
        for t in range(0, len(counts)):
            counts[t] = str(counts[t])
            counts[t] = re.sub('[^0-9]', '', counts[t])
            counts_array.append(counts[t])
        counts = counts_array
        counts.sort()
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        names = []
        for t in range(0, 8):
            cursor.execute("SELECT JOBNAME FROM JOBS WHERE COUNT = ? AND IDLE = ?", (counts[len(counts)-t-1], 0))
            job_name = cursor.fetchall()
            handle.commit()
            if len(job_name) > 1:
                try:
                    job_name = job_name[t]
                except:
                    job_name = job_name[random.randint(0, 1)]
            job_name = str(job_name)
            job_name = job_name[2: len(job_name)-5]
            if job_name == "":
                cont = True
            else:
                if job_name[0] == "'":
                    job_name = job_name[1:]
                if job_name[len(job_name)-1] == "\\":
                    job_name = job_name[:len(job_name)-1]
                if job_name not in names:
                    names.append(job_name)
        handle.close()
        new_tab = ttk.Frame(tabcontrol)
        tabcontrol.add(new_tab, text="POPULAR JOBS")
        tabcontrol.select(new_tab)
        tk.Label(new_tab, text= " ").grid(row=1)
        tk.Label(new_tab, text= " ").grid(row=3)
        tk.Label(new_tab, text= " ").grid(row=5)
        tk.Label(new_tab, text= "Popular Roles", font="Verdana 30 italic").grid(row=2, column=3)
        VAR = StringVar()
        VAR.set(names[random.randint(0, len(names)-1)])
        tk.OptionMenu(new_tab, VAR, *names).grid(row=4, columnspan=7)
        HoverButton(new_tab, activebackground='Light Blue', fg="white", bg="Black", text="Confirm", command = lambda: [job.popular2(VAR, ID_insert), both.closetab(new_tab)]).grid(row=6, column=3)
        HoverButton(new_tab, activebackground='Light Blue', fg="white", bg="Blue", text="Back", command = lambda: [both.closetab(new_tab), job.mainmenu(ID_insert)]).grid(row=6, column=1)
        
    def popular2(self, VAR, ID_insert):
        job_name = VAR.get()
        job.display(job_name, 0, ID_insert)
        
    def fieldstart(self, tab1, ID_insert):
        txts = ["Science.txt", "Agri.txt", "Arch.txt", "Business.txt", "Arts.txt", "Finance.txt", "Gov.txt", "Health.txt", "Hospit.txt", "Human.txt", "IT.txt", "Law.txt", "Manufact.txt", "Market.txt", "Transport.txt", "Edu.txt"]
        fields = []
        for x in range(0, len(txts)):
            file = open(txts[x])
            fieldjob = file.readlines()
            fieldname = fieldjob[0]
            fields.append(fieldname)
        # finds all jobs in a chosen field, simple sequel statement
        tab1.destroy()
        fieldsearch = ttk.Frame(tabcontrol)
        tabcontrol.add(fieldsearch, text="FIELD SEARCH")
        tabcontrol.select(fieldsearch)
        tk.Label(fieldsearch, font="Verdana 25", text= "Choose a Field").grid(row=2, column=3)
        variance = StringVar()
        variance.set(fields[random.randint(0, len(fields)-1)])
        tk.OptionMenu(fieldsearch, variance, *fields).grid(row=4, column=3)
        tk.Label(fieldsearch, text="   ").grid(row=1, column=1)
        tk.Label(fieldsearch, text="   ").grid(row=3, column=2)
        tk.Label(fieldsearch, text="   ").grid(row=5, column=3)
        HoverButton(fieldsearch, activebackground='Light Blue', fg="white", bg="Black", text="Confirm", command = lambda: job.field_data(variance, fieldsearch, ID_insert)).grid(row=6, column=3)
        HoverButton(fieldsearch, activebackground='Light Blue', fg="white", bg="Blue", text="Back", command = lambda: [both.closetab(fieldsearch), job.mainmenu(ID_insert)]).grid(row=6, column=2)

    def field_data(self, variance, fieldsearch, ID_insert):
        variance = variance.get()
        fieldsearch.destroy()
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute(("SELECT JOBNAME FROM JOBS WHERE FIELD = ? AND IDLE = ?"), (variance, 0))
        names = cursor.fetchall()
        handle.commit()
        handle.close()
        punctuation = """!"#$%&'()*+:;=?@[\\]^_`{|'}~"""
        new = ""
        string = str(names)
        for i in string:
            if i not in punctuation:
                new += i
        new = new.split(",,")
        for t in range(0, len(new)):
            new[t] = new[t][:len(new[t])-1]
        new[len(new)-1] = new[len(new)-1][:len(new[t])-1]
        vars_ = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        # need to show a menu with all jobs that is clickable into an individual menu
        var_job = StringVar()
        var_job.set(new[random.randint(0, len(new)-1)])
        results_field = ttk.Frame(tabcontrol)
        tabcontrol.add(results_field, text="FIELD RESULTS")
        tabcontrol.select(results_field)
        tk.Label(results_field, text="   ").grid(row=1, column=1)
        tk.Label(results_field, text=variance, font="Verdana 13").grid(row=2, columnspan=7)
        tk.Label(results_field, text="   ").grid(row=3, column=1)
        tk.Label(results_field, text="   ").grid(row=5, column=1)
        tk.OptionMenu(results_field, var_job, *new).grid(row=4, column=3)
        HoverButton(results_field, activebackground='Light Blue', fg="white", bg="black", text="Confirm", command = lambda: job.getresultoffield_search(var_job, results_field, ID_insert)).grid(row=6, column=3)
        tab1 = ttk.Frame(tabcontrol)
        HoverButton(results_field, activebackground='Light Blue', fg="white", bg="Blue", text="Back", command= lambda: [job.fieldstart(tab1, ID_insert), job.delete_fieldresults(tab1, results_field)]).grid(row=6, column=2)

    def delete_fieldresults(self, tab1, results_field):
        tab1.destroy()
        results_field.destroy()
        
    def getresultoffield_search(self, var_job, results_field, ID_insert):
        var_job = var_job.get()
        results_field.destroy()
        job_name = var_job
        if job_name[0] == " ":
            job_name = job_name[1:]
        job.display(job_name, 0, ID_insert)

    def rating(self, tab1, ID_insert):
        tab1.destroy() # after recommendation, user gives feedback rating 0-5 and this will search jobs
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT JOBID FROM RATINGS")
        ids = cursor.fetchall()
        handle.commit()
        handle.close()
        ident = []
        cont = True
        for h in range(0, len(ids)):
            cont = True
            ids[h] = re.sub('[^0-9]', '', str(ids[h]))
            for v in range(0, len(ident)):
                if ident[v] == ids[h]:
                    cont = False
            if cont == True:
                ident.append(ids[h])
        averages = []
        for l in range(0, len(ident)):
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            cursor.execute("SELECT RATING FROM RATINGS WHERE JOBID = ? AND JOBID > ?", (ident[l], 0))
            ratings = cursor.fetchall()
            handle.commit()
            handle.close()
            total = 0
            for g in range(0, len(ratings)):
                ratings[g] = re.sub('[^0-9]', '', str(ratings[g]))
                total = total + int(ratings[g])
            average = total / len(ratings)
            averages.append(average)
        temp = averages
        averages.sort()
        sort_averages = averages
        averages = temp
        top5 = []
        pos = []
        if len(sort_averages) > 5:
            number = 5
        elif len(sort_averages) < 5 and len(sort_averages) > 1:
            number = len(sort_averages)
        else:
            number = 1
        for y in range(0, number):
            top5.append(sort_averages[len(sort_averages)-y-1])
        for a in range(0, len(averages)):
            for b in range(0, len(top5)):
                if averages[a] == top5[b]:
                    pos.append(a)
        final_ids = []
        for o in range(0, len(pos)):
            position = pos[o]
            id_ = ident[position]
            final_ids.append(id_)
        final_ids2 = []
        for k in range(0, len(final_ids)):
            if final_ids[k] not in final_ids2:
                final_ids2.append(final_ids[k])
        job_names = []
        for q in range(0, len(final_ids2)):
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            cursor.execute("SELECT JOBNAME FROM JOBS WHERE JOBID = ? AND JOBID > ?", (final_ids2[q], 0))
            job_name = cursor.fetchall()
            handle.commit()
            handle.close()
            job_name = str(job_name)
            job_name = job_name[3:len(job_name)-6]
            job_names.append(job_name)
        results_field = ttk.Frame(tabcontrol)
        tabcontrol.add(results_field, text="JOB RESULTS")
        tabcontrol.select(results_field)
        var = StringVar()
        var.set(job_names[random.randint(0, len(job_names)-1)])
        tk.Label(results_field, text="Highly rated jobs: ").grid(row=2)
        OptionMenu(results_field, var, *job_names).grid(row=2, column=1)
        HoverButton(results_field, activebackground='blue', fg="white", bg="black", text="Continue", command= lambda: [both.closetab(results_field), job.popular2(var, ID_insert)]).grid(row=3, column=1)
        HoverButton(results_field, activebackground='blue', fg="white", bg="black", text="Back", command= lambda: [both.closetab(results_field), job.mainmenu(ID_insert)]).grid(row=3)

class schools:
    def home(self, IDinsert):
        self.__tab = ttk.Frame(tabcontrol)
        tabcontrol.add(self.__tab, text="Schools")
        tabcontrol.select(self.__tab)
        tk.Label(self.__tab, text="  ").grid(row=2, column=1)
        tk.Label(self.__tab, text="  ").grid(row=4, column=3)
        tk.Label(self.__tab, text="  ").grid(row=4, column=4)
        tk.Label(self.__tab, text="  ").grid(row=6)
        tk.Label(self.__tab, text="  ").grid(row=9)
        tk.Label(self.__tab, text="  ").grid(row=19)
        tk.Label(self.__tab, text="Nearest School:", font="Verdana 12 bold italic", fg="black").grid(row=3)
        tk.Label(self.__tab, fg="grey", text="School Home", font="Verdana 29").grid(row=1, columnspan=7)
        Postcodeentry = tk.Entry(self.__tab, font="Ariel 12")
        Postcodeentry.insert(END, "PostCode")
        Postcodeentry.grid(row=4, column=2)
        HoverButton(self.__tab, activebackground='black', fg="white", bg="grey", text="ENTER", command = lambda: schools.run(self, Postcodeentry, self.__tab, IDinsert)).grid(row=5, column=2)
        HoverButton(self.__tab, height=5, width=70, activebackground='Grey', fg="white", bg="Black", text="Home", command = lambda: [both.closetab(self.__tab), both.home(IDinsert)]).grid(row=20, columnspan=7)
        area_entry = tk.Entry(self.__tab, font="Ariel 12")
        area_entry.insert(END, "Area Name")
        area_entry.grid(row=7, column=2)
        HoverButton(self.__tab, activebackground='black', fg="white", bg="grey", text="ENTER", command = lambda: schools.area(self, area_entry, self.__tab, IDinsert)).grid(row=8, column=2)
        tk.Label(self.__tab, text="Search School:", font="Verdana 12 bold italic", fg="black").grid(row=10)
        searchingentry = tk.Entry(self.__tab, font="Ariel 12")
        searchingentry.insert(END, "Name")
        searchingentry.grid(row=11, column=2)
        HoverButton(self.__tab, activebackground='black', fg="white", bg="grey", text="ENTER", command = lambda: schools.search(self, searchingentry, self.__tab, IDinsert)).grid(row=12, column=2)

    def area(self, area_entry, tab, IDinsert):
        area_entry = area_entry.get()
        both.closetab(tab)
        handle = sql.connect("Schools.db")
        cursor = handle.cursor()
        cursor.execute("SELECT LOCATION FROM DATA")
        areas = cursor.fetchall()
        handle.commit()
        handle.close()
        all_areas = []
        repeatlist = []
        for ar in areas:
            ar = str(ar)
            ar = ar[2:len(ar)-3]
            if ar not in all_areas:
                all_areas.append(ar)
        area_entry = area_entry.upper()
        for l in range(0, len(all_areas)):
            all_areas[l] = all_areas[l].upper()
            repeats = 0
            for p in range(0, len(all_areas[l])):
                try:
                    letter = all_areas[l][p]
                    if area_entry[p] == letter:
                        repeats = repeats+1
                except:
                    cont=True
            repeatlist.append(repeats)
        repeatlist.sort()
        highestrepeat = repeatlist[len(repeatlist)-1]
        school =[]
        for l in range(0, len(all_areas)):
            repeats = 0
            for p in range(0, len(all_areas[l])):
                try:
                    letter = all_areas[l][p]
                    if area_entry[p] == letter:
                        repeats = repeats+1
                except:
                    cont=True
            if repeats == highestrepeat:
                school.append(all_areas[l])
        new_tab = ttk.Frame(tabcontrol)
        tabcontrol.add(new_tab, text="Areas")
        tabcontrol.select(new_tab)
        tk.Label(new_tab, text= " ").grid(row=1)
        tk.Label(new_tab, text= " ").grid(row=3)
        tk.Label(new_tab, text= " ").grid(row=5)
        tk.Label(new_tab, text= "Search Result", font="Verdana 30 italic").grid(row=2, column=3)
        VAR = StringVar()
        VAR.set(school[random.randint(0, len(school)-1)])
        tk.OptionMenu(new_tab, VAR, *school).grid(row=4, columnspan=7)
        HoverButton(new_tab, activebackground='Black', fg="white", bg="Grey", text="Confirm", command = lambda: schools.areas2(self, VAR, new_tab, IDinsert)).grid(row=6, column=3)
        HoverButton(new_tab, activebackground='Black', fg="white", bg="Grey", text="Back", command = lambda: [both.closetab(new_tab), schools.home(self, IDinsert)]).grid(row=6, column=1)

    def areas2(self, area, tab, IDinsert):
        area = area.get()
        both.closetab(tab)
        handle = sql.connect("Schools.db")
        cursor = handle.cursor()
        cursor.execute("SELECT NAME FROM DATA WHERE LOCATION LIKE ? AND NAME != ?", (area, ""))
        all_names = cursor.fetchall()
        handle.commit()
        handle.close()
        all_names2 = []
        for name in all_names:
            name = str(name)
            name = name[2:len(name)-3]
            all_names2.append(name)
        all_names = all_names2
        new_tab = ttk.Frame(tabcontrol)
        tabcontrol.add(new_tab, text="Schools in the chosen area:")
        tabcontrol.select(new_tab)
        tk.Label(new_tab, text= " ").grid(row=1)
        tk.Label(new_tab, text= " ").grid(row=3)
        tk.Label(new_tab, text= " ").grid(row=5)
        tk.Label(new_tab, text= "Schools", font="Verdana 30 italic").grid(row=2, column=3)
        VAR = StringVar()
        VAR.set(all_names[random.randint(0, len(all_names)-1)])
        tk.OptionMenu(new_tab, VAR, *all_names).grid(row=4, columnspan=7)
        HoverButton(new_tab, activebackground='Black', fg="white", bg="Grey", text="Confirm", command = lambda: schools.area3(self, new_tab, VAR, IDinsert)).grid(row=6, column=3)
        HoverButton(new_tab, activebackground='Black', fg="white", bg="Grey", text="Back", command = lambda: [both.closetab(new_tab), schools.home(self, IDinsert)]).grid(row=6, column=1)
    
    def search(self, search, tab, IDinsert):
        search = search.get()
        both.closetab(tab)
        entrybox = search.upper()
        repeatlist = []
        all_names = []
        handle = sql.connect("Schools.db")
        cursor = handle.cursor()
        cursor.execute("SELECT NAME FROM DATA")
        names = cursor.fetchall()
        handle.commit()
        handle.close()
        for name in names:
            name = str(name)
            name = name[2:len(name)-3]
            all_names.append(name)
        for l in range(0, len(all_names)):
            all_names[l] = all_names[l].upper()
            repeats = 0
            for p in range(0, len(all_names[l])):
                try:
                    letter = all_names[l][p]
                    if entrybox[p] == letter:
                        repeats = repeats+1
                except:
                    cont=True
            repeatlist.append(repeats)
        repeatlist.sort()
        highestrepeat = repeatlist[len(repeatlist)-1]
        school =[]
        for l in range(0, len(all_names)):
            repeats = 0
            for p in range(0, len(all_names[l])):
                try:
                    letter = all_names[l][p]
                    if entrybox[p] == letter:
                        repeats = repeats+1
                except:
                    cont=True
            if repeats == highestrepeat:
                school.append(all_names[l])
        if len(school) > 3:
            while len(school) > 3:
                school.remove(school[len(school)-1])
        for r in range(0, len(school)):
            schoolname = school[r]
            schools.display(self, schoolname, IDinsert)
        
    def area3(self, tab, schoolname, IDinsert):
        schoolname = schoolname.get()
        both.closetab(tab)
        schools.display(self, schoolname, IDinsert)

    def display(self, schoolname, IDinsert):
        handle = sql.connect("Schools.db")
        cursor = handle.cursor()
        cursor.execute("SELECT SCHOOLID, NAME, LOCATION, TYPE, GENDER, LONG, LATIT, EAST, NORTH, LOWAGE, HIGHAGE, OPEN, WEBSITE FROM DATA WHERE NAME LIKE ? AND NAME != ?", (schoolname, ""))
        details = cursor.fetchall()
        handle.commit()
        handle.close()
        details = str(details[0])
        details = details[1:len(details)-1]
        details = details.split(",")
        for u in range(0, len(details)):
            if details[u][0] == " " and details[u][1] == "'":
                details[u] = details[u][2:len(details[u])-1]
            elif details[u][0] == " ":
                details[u] = details[u][1:]
            elif details[u][0] == "'":
                details[u] = details[u][1:len(details[u])-1]
        handle = sql.connect("Schools.db")
        cursor = handle.cursor()
        cursor.execute("INSERT INTO RECOMMEND3 VALUES(?,?)", (details[0], IDinsert))
        handle.commit()
        handle.close()
        tab1 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab1, text=details[1])
        tabcontrol.select(tab1)
        tk.Label(tab1, text="Name:", font="Ariel 14", fg="Grey").grid(row=3, column=1)
        tk.Label(tab1, text=details[1], font="Ariel 14", fg="Red").grid(row=3, column=2)
        tk.Label(tab1, text="Area:", font="Ariel 14", fg="Grey").grid(row=4, column=1)
        tk.Label(tab1, text=details[2], font="Ariel 14", fg="Red").grid(row=4, column=2)
        tk.Label(tab1, text="Level:", font="Ariel 14", fg="Grey").grid(row=5, column=1)
        tk.Label(tab1, text=details[3], font="Ariel 14", fg="Red").grid(row=5, column=2)
        tk.Label(tab1, text="Type:", font="Ariel 14", fg="Grey").grid(row=8, column=1)
        tk.Label(tab1, text=details[4], font="Ariel 14", fg="Red").grid(row=8, column=2)
        tk.Label(tab1, text="Website:", font="Ariel 14", fg="Grey").grid(row=10, column=1)
        HoverButton(tab1, activebackground='black', fg="white", bg="grey", text=details[len(details)-1], command = lambda: job.openurl(details[len(details)-1])).grid(row=10, column=2)
        tk.Label(tab1, text="*some websites are not always functional as", font="Ariel 10", fg="Black").grid(row=11, column=2)
        tk.Label(tab1, text="schools havent been logged with new information yet", fg="Black", font="Ariel 10").grid(row=12, column=2)
        tk.Label(tab1, text="Status:", font="Ariel 14", fg="Grey").grid(row=14, column=1)
        tk.Label(tab1, text=details[len(details)-2], font="Ariel 14", fg="Red").grid(row=14, column=2)
        tk.Label(tab1, text="LowAge:", font="Ariel 14", fg="Grey").grid(row=6, column=1)
        tk.Label(tab1, text=details[9], font="Ariel 14", fg="Red").grid(row=6, column=2)
        tk.Label(tab1, text="HighAge:", font="Ariel 14", fg="Grey").grid(row=7, column=1)
        tk.Label(tab1, text=details[10], font="Ariel 14", fg="Red").grid(row=7, column=2)
        tk.Label(tab1, text=" ").grid(row=9, column=2)
        tk.Label(tab1, text=" ").grid(row=13, column=2)
        tk.Label(tab1, text=" ").grid(row=19, column=2)
        tk.Label(tab1, text=" ").grid(row=2, column=2)
        tk.Label(tab1, text="Search Result", font="Verdana 26", fg="Black").grid(row=1, columnspan=7)
        HoverButton(tab1, width=70, height=2, activebackground='Grey', fg="white", bg="Black", text="Home", command = lambda: [schools.home(self, IDinsert), both.closetab(tab1)]).grid(row=20, columnspan=7)
        HoverButton(tab1, width=70, height=2, activebackground='Grey', fg="white", bg="Black", text="Close Tab", command = lambda: [both.closetab(tab1)]).grid(row=19, columnspan=7)

    def run(self, post, tab, IDinsert):
        post = post.get()
        both.closetab(tab)
        tab1 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab1, text="Schools")
        tabcontrol.select(tab1)
        try:
            nomi = pgeocode.Nominatim('GB')
            info = nomi.query_postal_code(post)
            lat = info[9]
            longit = info[10]
        except:
            lat = 0
            longit = 0
        x2 = lat
        y2 = longit
        handle = sql.connect("Schools.db")
        cursor = handle.cursor()
        cursor.execute("SELECT LATIT, LONG FROM DATA")
        latlong = cursor.fetchall()
        handle.commit()
        handle.close()
        hold = 99999999999999999999
        data = []
        for y in range(0, len(latlong)):
            dist = job.jobcentre.distance(self, y2, x2, latlong[y][1], latlong[y][0])
            if float(dist) <= float(hold):
                hold = dist
                data.append(latlong[y][0])
                data.append(latlong[y][1])
        try:
            handle = sql.connect("Schools.db")
            cursor = handle.cursor()
            cursor.execute("SELECT SCHOOLID, NAME, LOCATION, TYPE, GENDER, LONG, LATIT, EAST, NORTH, LOWAGE, HIGHAGE, OPEN, WEBSITE FROM DATA WHERE LONG = ? AND LATIT = ?", (data[len(data)-1], data[len(data)-2]))
            details = cursor.fetchall()
            handle.commit()
            handle.close()
            details = str(details[0])
            details = details[1:len(details)-1]
            details = details.split(",")
            for u in range(0, len(details)):
                if details[u][0] == " " and details[u][1] == "'":
                    details[u] = details[u][2:len(details[u])-1]
                elif details[u][0] == " ":
                    details[u] = details[u][1:]
                elif details[u][0] == "'":
                    details[u] = details[u][1:len(details[u])-1]
            handle = sql.connect("Schools.db")
            cursor = handle.cursor()
            cursor.execute("INSERT INTO RECOMMEND3 VALUES(?,?)", (details[0], IDinsert))
            handle.commit()
            handle.close()
            tk.Label(tab1, text="Name:", font="Ariel 14", fg="Grey").grid(row=3, column=1)
            tk.Label(tab1, text=details[1], font="Ariel 14", fg="Red").grid(row=3, column=2)
            tk.Label(tab1, text="Area:", font="Ariel 14", fg="Grey").grid(row=4, column=1)
            tk.Label(tab1, text=details[2], font="Ariel 14", fg="Red").grid(row=4, column=2)
            tk.Label(tab1, text="Level:", font="Ariel 14", fg="Grey").grid(row=5, column=1)
            tk.Label(tab1, text=details[3], font="Ariel 14", fg="Red").grid(row=5, column=2)
            tk.Label(tab1, text="Type:", font="Ariel 14", fg="Grey").grid(row=8, column=1)
            tk.Label(tab1, text=details[4], font="Ariel 14", fg="Red").grid(row=8, column=2)
            tk.Label(tab1, text="Website:", font="Ariel 14", fg="Grey").grid(row=10, column=1)
            HoverButton(tab1, activebackground='black', fg="white", bg="grey", text=details[len(details)-1], command = lambda: job.openurl(details[len(details)-1])).grid(row=10, column=2)
            tk.Label(tab1, text="*some websites are not always functional as", font="Ariel 10", fg="Black").grid(row=11, column=2)
            tk.Label(tab1, text="schools havent been logged with new information yet", fg="Black", font="Ariel 10").grid(row=12, column=2)
            tk.Label(tab1, text="Status:", font="Ariel 14", fg="Grey").grid(row=14, column=1)
            tk.Label(tab1, text=details[len(details)-2], font="Ariel 14", fg="Red").grid(row=14, column=2)
            tk.Label(tab1, text="LowAge:", font="Ariel 14", fg="Grey").grid(row=6, column=1)
            tk.Label(tab1, text=details[9], font="Ariel 14", fg="Red").grid(row=6, column=2)
            tk.Label(tab1, text="HighAge:", font="Ariel 14", fg="Grey").grid(row=7, column=1)
            tk.Label(tab1, text=details[10], font="Ariel 14", fg="Red").grid(row=7, column=2)
        except:
            tk.Label(tab1, text="Invalid Postcode Input", font="Verdana 20", fg="Red").grid(row=4, columnspan=7)
        tk.Label(tab1, text=" ").grid(row=9, column=2)
        tk.Label(tab1, text=" ").grid(row=13, column=2)
        tk.Label(tab1, text=" ").grid(row=19, column=2) # blank for spacing / structure of the UI
        tk.Label(tab1, text=" ").grid(row=2, column=2)
        tk.Label(tab1, text="Your Nearest Institution", font="Verdana 26", fg="Black").grid(row=1, columnspan=7)
        HoverButton(tab1, width=70, height=5, activebackground='Grey', fg="white", bg="Black", text="Home", command = lambda: [schools.home(self, IDinsert), both.closetab(tab1)]).grid(row=20, columnspan=7)

    def run2(self, tab, name, ID_insert):
        tab.destroy()
        tab1 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab1, text="Schools") # making a new tkinter tab to display all of the school data
        tabcontrol.select(tab1)
        handle = sql.connect("Schools.db")
        cursor = handle.cursor()
        cursor.execute("SELECT SCHOOLID, NAME, LOCATION, TYPE, GENDER, LONG, LATIT, EAST, NORTH, LOWAGE, HIGHAGE, OPEN, WEBSITE FROM DATA WHERE NAME = ? AND NAME != ?", (name, " "))
        details = cursor.fetchall()
        handle.commit() # getting all of the data about a school in the table DATA from it's name
        handle.close()
        details = str(details[0])
        details = details[1:len(details)-1]
        details = details.split(",")
        for u in range(0, len(details)):
            if details[u][0] == " " and details[u][1] == "'": # formatting the information by splitting each piece of data and cleaning off unwanted characters
                details[u] = details[u][2:len(details[u])-1]
            elif details[u][0] == " ":
                details[u] = details[u][1:]
            elif details[u][0] == "'":
                details[u] = details[u][1:len(details[u])-1]

        # creating / designing the schools layout with every bit of data retrived from the database 
        tk.Label(tab1, text="Name:", font="Ariel 14", fg="Grey").grid(row=3, column=1)
        tk.Label(tab1, text=details[1], font="Ariel 14", fg="Red").grid(row=3, column=2) # providing the name of the school
        tk.Label(tab1, text="Area:", font="Ariel 14", fg="Grey").grid(row=4, column=1)
        tk.Label(tab1, text=details[2], font="Ariel 14", fg="Red").grid(row=4, column=2) # providing the area of the school
        tk.Label(tab1, text="Level:", font="Ariel 14", fg="Grey").grid(row=5, column=1)
        tk.Label(tab1, text=details[3], font="Ariel 14", fg="Red").grid(row=5, column=2) # providing the level of the school, such as secondary
        tk.Label(tab1, text="Type:", font="Ariel 14", fg="Grey").grid(row=8, column=1)
        tk.Label(tab1, text=details[4], font="Ariel 14", fg="Red").grid(row=8, column=2) # providing the type of the school, such as independant
        tk.Label(tab1, text="Website:", font="Ariel 14", fg="Grey").grid(row=10, column=1)
        HoverButton(tab1, activebackground='black', fg="white", bg="grey", text=details[len(details)-1], command = lambda: job.openurl(details[len(details)-1])).grid(row=10, column=2) # calling openurl sub-routine upon click of button
        tk.Label(tab1, text="*some websites are not always functional as", font="Ariel 10", fg="Black").grid(row=11, column=2)
        tk.Label(tab1, text="schools havent been logged with new information yet", fg="Black", font="Ariel 10").grid(row=12, column=2)
        tk.Label(tab1, text="Status:", font="Ariel 14", fg="Grey").grid(row=14, column=1)
        tk.Label(tab1, text=details[len(details)-2], font="Ariel 14", fg="Red").grid(row=14, column=2) # providing the status of the school, such as open or close
        tk.Label(tab1, text="LowAge:", font="Ariel 14", fg="Grey").grid(row=6, column=1)
        tk.Label(tab1, text=details[9], font="Ariel 14", fg="Red").grid(row=6, column=2) # providing the age of arriving at the school
        tk.Label(tab1, text="HighAge:", font="Ariel 14", fg="Grey").grid(row=7, column=1)
        tk.Label(tab1, text=details[10], font="Ariel 14", fg="Red").grid(row=7, column=2) # providing the age of leaving from the school
        tk.Label(tab1, text=" ").grid(row=9, column=2)
        tk.Label(tab1, text=" ").grid(row=13, column=2)
        tk.Label(tab1, text=" ").grid(row=19, column=2) # gaps to separate labels and buttons for a clear layout
        tk.Label(tab1, text=" ").grid(row=2, column=2)
        tk.Label(tab1, text="Your Nearest Institution", font="Verdana 26", fg="Black").grid(row=1, columnspan=7)
        HoverButton(tab1, width=70, height=5, activebackground='Grey', fg="white", bg="Black", text="Home", command = lambda: [schools.home(self, ID_insert), both.closetab(tab1)]).grid(row=20, columnspan=7)


#create main menu upon staring program
if __name__ == "__main__": # allows to be imported into another file and doesnt run instantly
    window=tk.Tk() # Form a tkinter window
    window.title("Recommender") # naming the entire tkinter window "Recommender"
    tabcontrol = ttk.Notebook(window) # creating a method that controls how tabs are managed
    both = both()
    uni = uni()
    job = job() # creating all of the objects so the __init__ has ran first
    sk = schools()
    both.loginhome() # creates a tkinter tab
    window.geometry("500x500") # to set size of every tkinter window
    window.resizable(0, 0) # so all tabs and windows are a set size consistently
    tabcontrol.pack(expand=1, fill="both") # 
    window.mainloop() # create the updated tkinter window
