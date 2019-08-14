import sqlite3 as sql
import tkinter as tk
from tkinter import ttk
from tkinter import *
import time
import re
import urllib3
import hashlib
import os
import binascii
import random

def mainmenu():
    tab1 = ttk.Frame(tabcontrol)
    tabcontrol.add(tab1, text="MAIN MENU")
    tabcontrol.select(tab1)
    attempts = 0
    hold = tk.Label(tab1, text=" ").grid(row=1)
    popularjobs = tk.Button(tab1, text = "POPULAR JOBS", command = lambda: popular(tab1)).grid(row=2)
    highrated = tk.Button(tab1, text = "HIGHLY RATED", command = lambda: rating(tab1)).grid(row=2, column=1)
    fieldjobs = tk.Button(tab1, text = "SEARCH FIELDS", command = lambda: fieldstart(tab1)).grid(row=2, column=2)
    hold_ = tk.Label(tab1, text=" ").grid(row=3)
    searchjobs = tk.Label(tab1, text="SEARCH JOBS:").grid(row=4)
    searchjobentry = tk.Entry(tab1)
    searchjobentry.grid(row=4, column=1)
    entersearch = tk.Button(tab1, text="ENTER", command= lambda: search(searchjobentry, tab1)).grid(row=4, column=2)
    hold___ = tk.Label(tab1, text=" ").grid(row=7)
    loginlabel = tk.Label(tab1, text="LOGIN:").grid(row=8)
    IDENTenter = tk.Label(tab1, text="ID:").grid(row=9)
    IDENTentry = tk.Entry(tab1)
    IDENTentry.grid(row=9, column=1)
    Passwordenter = tk.Label(tab1, text="Password:").grid(row=10)
    Passwordentry = tk.Entry(tab1)
    Passwordentry.grid(row=10, column=1)
    #resetpin = tk.Button(tab1, text="FORGOT PIN", command = lambda: reset()).grid(row=7, column=3)
    loginbutton = tk.Button(tab1, text="ENTER", command= lambda: login(attempts, tab1, IDENTentry, Passwordentry)).grid(row=11, column=1)
    hold__ = tk.Label(tab1, text=" ").grid(row=12)
    usernew = tk.Label(tab1, text="NEW USER:").grid(row=13)
    IDenter = tk.Label(tab1, text="ID: ").grid(row=15)
    IDentry = tk.Entry(tab1)
    IDentry.grid(row=15, column=1)
    choices = ["< High School Diploma", "High School Diploma", "Master", "Bachelor", "Associate", "Some College", "Doctoral Degree", "Vocational Certificate"]
    buttonconfirm = tk.Button(tab1, text="ENTER", command = lambda: user1(IDentry, tab1, choices)).grid(row=15, column=2)
 
def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def deleteinvalid(errorlogin):
    errorlogin.destroy()
    
def login(attempts, tab1, IDENTentry, Passwordentry):
    IDENT_insert = IDENTentry.get()
    PIN_insert = Passwordentry.get()
    handle = sql.connect("NEA.db")
    cursor = handle.cursor()
    cursor.execute("SELECT USERS.USERID FROM USERS")
    ids = cursor.fetchall()
    handle.commit()
    z = 0
    idsclean = []
    for x in range(0, len(ids)):
        a = str(ids[z])
        b = a.strip('(),/\'')
        idsclean.append(b)
        z = z+1
    ids = idsclean
    i = 0
    k = 0
    for x in range(0, len(ids)):
        if ids[i] == IDENT_insert:
            cursor.execute("SELECT USERS.PASSWORD FROM USERS WHERE USERS.USERID = ?", (IDENT_insert,))
            PINrecieved = cursor.fetchall()
            handle.commit()
            PINrecieved = PINrecieved[0]
            PINrecieved = str(PINrecieved)
            PINrecieved = PINrecieved.strip("/'(),'")
            TrueorFalse = verify_password(PINrecieved, PIN_insert)
            if TrueorFalse == True:
                changelogin(tab1, IDENT_insert, PIN_insert)
                k = 8
        i = i+1
    attempt=attempts+1
    # incorrect entry tab with a back to main menu button
    tab1.destroy()
    if k != 8:
        errorlogin = ttk.Frame(tabcontrol)
        tabcontrol.add(errorlogin, text="INVALID")
        incorrect = tk.Label(errorlogin, text="ID or Password is incorrect").grid(row=1)
        backtomain = tk.Button(errorlogin, text="Back to Main Menu", command= lambda: [deleteinvalid(errorlogin), mainmenu()]).grid(row=2)
    
def changelogin(tab1, IDENT_insert, PIN_insert):
    tab1.destroy()
    #give option to change details (other than id/password)
    tab4 = ttk.Frame(tabcontrol)
    tabcontrol.add(tab4, text="Step 2")
    tabcontrol.select(tab4)
    ID_insert = IDENT_insert
    change = tk.Button(tab4, text="edit your data", command = lambda: changingdata(ID_insert, PIN_insert, tab4)).grid(row=1)
    cont = tk.Button(tab4, text="Find Personalised Reccomendations", command = lambda: fieldq(ID_insert, tab4)).grid(row=2)

def changingdata(ID_insert, PIN_insert, tab4):
    tab4.destroy()
    tab4 = ttk.Frame(tabcontrol)
    tabcontrol.add(tab4, text="Update Info")
    tabcontrol.select(tab4)
    handle = sql.connect("NEA.db")
    cursor = handle.cursor()
    cursor.execute("SELECT USERID, NAME, QUALLEVEL, SKILL1, SKILL2, SKILL3, CURRENTJOB FROM USERS WHERE USERID = ? AND USERID > ?;", (ID_insert, "0"))
    userinfo = cursor.fetchall()
    handle.commit()
    handle.close()
    for h in range(0, len(userinfo)):
        punctuation = """!"#$%&'()*+-/:;<=>?@[\\]^_`{|}~"""
        user_info = ""
        string = str(userinfo[h])
        for e in string:
            if e not in punctuation:
                user_info += e
    user_info = user_info.split(",")
    identlabel = tk.Label(tab4, text="Name:").grid(row=1)
    ident = tk.Entry(tab4)
    ident.insert(0,user_info[1])
    ident.grid(row=1, column=1)
    quallabel = tk.Label(tab4, text="Qual:").grid(row=2)
    qual = tk.Entry(tab4)
    qual.insert(0,user_info[2])
    qual.grid(row=2, column=1)
    skilllabel = tk.Label(tab4, text="SKILL:").grid(row=3)
    skilldoc = open("keyskills.txt")
    skill_list = []
    read = "/n"
    while read != "":
        read = skilldoc.readline()
        read = read.rstrip()
        skill_list.append(read)
    skill_list.sort()
    skill_list.remove("")
    skilldoc.close()
    vara = StringVar()
    vara.set(user_info[3])
    varb = StringVar()
    varb.set(user_info[4])
    varc = StringVar()
    varc.set(user_info[5])
    skillopt1 = OptionMenu(tab4 , vara, *skill_list)
    skillopt1.grid(row=3, column=1)
    skillopt2 = OptionMenu(tab4 , varb, *skill_list)
    skillopt2.grid(row=3, column=2)
    skillopt3 = OptionMenu(tab4 , varc, *skill_list)
    skillopt3.grid(row=3, column=3)
    currlabel = tk.Label(tab4, text="Current Job:").grid(row=4)
    current = tk.Entry(tab4)
    current.insert(0,user_info[6])
    current.grid(row=4, column=1)
    continuebutton = tk.Button(tab4, text="Commit Changes", command = lambda: updatechanges(vara, varb, varc, qual, ID_insert, PIN_insert, ident, current, tab4)).grid(row=5)

def updatechanges(vara, varb, varc, qual, ID_insert, PIN_insert, ident, current, tab4):
    skill1 = vara.get()
    skill2 = varb.get()
    skill3 = varc.get()
    qual = qual.get()
    name = ident.get()
    current = current.get()
    handle = sql.connect("NEA.db")
    cursor = handle.cursor()
    cursor.execute("UPDATE USERS SET QUALLEVEL = ?, NAME = ?, CURRENTJOB = ?, SKILL1 = ?, SKILL2 = ?, SKILL3 = ? WHERE USERID = ?", (qual, name, current, skill1, skill2, skill3, ID_insert))
    handle.commit()
    handle.close()
    tab4.destroy()
    tab4 = ttk.Frame(tabcontrol)
    tabcontrol.add(tab4, text="DELETE ME")
    fieldq(ID_insert, tab4)

def deletetabs(error):
    error.destroy()
    
def user1(IDentry, tab1, choices):
    z = False
    ID_insert = IDentry.get()
    if ID_insert == "":
        ID_insert = "1"
    handle = sql.connect("NEA.db")
    cursor = handle.cursor()
    cursor.execute("SELECT USERID FROM USERS")
    allids = cursor.fetchall()
    handle.commit()
    handle.close()
    idsclean=[]
    tab1.destroy()
    for j in range(0, len(allids)):
        #call for new id if already exists, new tab with back button to main menu.
        a = str(allids[j])
        b = a.strip('(),')
        idsclean.append(b)
    nodup = 0
    for r in range(0, len(idsclean)):
        idsclean[r] = idsclean[r][1:len(idsclean[r])-1]
        if idsclean[r] == ID_insert:
            z = True
            nodup = nodup+1
            if nodup == 1:
                error = ttk.Frame(tabcontrol)
                tabcontrol.add(error, text="Id taken")
                tabcontrol.select(error)
                labelerror = tk.Label(error, text="ID is already taken...").grid(row=1)
                continuebutton = tk.Button(error, text="Back to Main Menu", command = lambda: [closetab(error), mainmenu()]).grid(row=2)
    if z == False:
        tab6 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab6, text="CREATE USER")
        tabcontrol.select(tab6)
        nameenter = tk.Label(tab6, text="NAME: ").grid(row=1)
        nameentry = tk.Entry(tab6)
        nameentry.grid(row=1, column=1)
        tkvar = StringVar()
        tkvar.set(choices[random.randint(0, len(choices)-1)])
        quallevel = tk.Label(tab6, text="CHOOSE HIGHEST QULAIFICATION LEVEL ACHIEVED:").grid(row=2)
        quallevelopt = tk.OptionMenu(tab6 , tkvar, *choices)
        quallevelopt.grid(row=2, column=1)
        skilldoc = open("keyskills.txt")
        skill_list = []
        read = "/n"
        while read != "":
            read = skilldoc.readline()
            read = read.rstrip()
            skill_list.append(read)
        skill_list.sort()
        skill_list.remove("")
        abvar = StringVar()
        set1 = skill_list[random.randint(0, len(skill_list)-1)]
        skill_list_temp = skill_list
        skill_list_temp.remove(set1)
        abvar.set(set1)
        acvar = StringVar()
        set2 = skill_list_temp[random.randint(0, len(skill_list_temp)-1)]
        skill_list_temp.remove(set2)
        acvar.set(set2)
        advar = StringVar()
        set3 = skill_list_temp[random.randint(0, len(skill_list_temp)-1)]
        advar.set(set3)
        keyskillenter = Label(tab6, text="MOST APPLICABLE SKILLS FOR YOU:").grid(row=3)
        keyskillopt1 = OptionMenu(tab6 , abvar, *skill_list)
        keyskillopt1.grid(row=3, column=1)
        keyskillopt2 = OptionMenu(tab6 , acvar, *skill_list)
        keyskillopt2.grid(row=3, column=2)
        keyskillopt3 = OptionMenu(tab6 , advar, *skill_list)
        keyskillopt3.grid(row=3, column=3)
        currententer = tk.Label(tab6, text="CURRENT JOB (N IF NO JOB): ").grid(row=4)
        currententry = tk.Entry(tab6)
        currententry.grid(row=4, column=1)
        Passwordenter = tk.Label(tab6, text="Password: ").grid(row=5)
        Password = tk.Entry(tab6)
        Password.grid(row=5, column=1)
        tab1 = ttk.Frame(tabcontrol)
        button = tk.Button(tab6, text="ENTER", command= lambda: loguser(ID_insert, tab6, nameentry, tkvar, abvar, acvar, advar, currententry, Password, IDentry, tab1, choices)).grid(row=5, column=2)

def loguser(ID_insert, tab6, nameentry, tkvar, abvar, advar, acvar, currententry, Password, IDentry, tab1, choices):
    username_insert = nameentry.get()
    quallevel_insert = tkvar.get()
    skill1_insert = abvar.get()
    skill2_insert = acvar.get()
    skill3_insert = advar.get()
    current_insert = currententry.get()
    Password_insert = Password.get()
    # conditions of passwords
    while len(Password_insert) < 6:
        Password_insert = Password_insert+"_"
    Password_insert = str(Password_insert)
    Password_insert1 = hash_password(Password_insert)
    if username_insert == "":
        username_insert = "NULL"
    if current_insert == "":
        current_insert = "N"
    tab6.destroy()
    handle = sql.connect("NEA.db")
    cursor = handle.cursor()
    cursor.execute("INSERT INTO USERS VALUES(?,?,?,?,?,?,?,?,?,?)", (ID_insert, username_insert, Password_insert1, quallevel_insert, skill1_insert, skill2_insert, skill3_insert, ".", current_insert, "."))
    handle.commit()
    handle.close()
    #could delete if not required and just run field function
    tab4 = ttk.Frame(tabcontrol)
    tabcontrol.add(tab4, text="REMEMBER THIS")
    tabcontrol.select(tab4)
    infotoremember = tk.Label(tab4, text="Remember these to login in next time to avoid re-completing the questions")
    IDprovide = tk.Label(tab4, text="ID:")
    ID2provide = tk.Label(tab4, text=ID_insert)
    PINprovide = tk.Label(tab4, text="Password:")
    counted = 0
    for char in Password_insert:
        if char == "_":
            counted = counted+1
    if counted > 1:
        counted = str(counted)
        Password_insert = str(Password_insert)
        Password_insert = Password_insert + " with " + counted + " underscores."
    PIN2provide = tk.Label(tab4, text=Password_insert)
    button = tk.Button(tab4, text="Let's answer some questions", command= lambda: fieldq(ID_insert, tab4))
    infotoremember.grid(row=1)
    IDprovide.grid(row=2)
    ID2provide.grid(row=2, column=1)
    PINprovide.grid(row=3)
    PIN2provide.grid(row=3, column=1)
    button.grid(row=4, column=1)

def fieldq(ID_insert, tab4):
    tab4.destroy()
    tab3 = ttk.Frame(tabcontrol)
    tabcontrol.add(tab3, text="Field Choice")
    tabcontrol.select(tab3)
    file = open("fieldlist.txt", "r")
    fields = []
    for r in range(0, 16):
        field = file.readline()
        fields.append(field)
    countofiterations = 0
    recordchoices = []
    var1 = IntVar()
    label = tk.Label(tab3, text=" ").grid(row=1, column=1)
    recurfield(ID_insert, tab3, fields, countofiterations, recordchoices, var1, label)

def recurfield(ID_insert, tab3, fields, countofiterations, recordchoices, var1, label):
    if countofiterations == 0:
        intro = tk.Label(tab3, text="Choose a proirity of each field so recommendation can be more appropriate.").grid(row=1)
    else:
        var1=var1.get()
        recordchoices.append(var1)
        label.destroy()
    if countofiterations == len(fields):
        updatefields(ID_insert, recordchoices, fields, tab3)
    try:
        label = tk.Label(tab3, text=fields[countofiterations])
        label.grid(row=2)
        progress = tk.Label(tab3, text=str(countofiterations)+"/"+str(len(fields)-1)).grid(row=2, column=1)
        countofiterations=countofiterations+1
        var1 = IntVar()
        radio1 = tk.Radiobutton(tab3, text="Very Interested", value=5, variable=var1).grid(row=3)
        radio2 = tk.Radiobutton(tab3, text="Interested", value=4, variable=var1).grid(row=4)
        radio3 = tk.Radiobutton(tab3, text="Neutral", value=3, variable=var1).grid(row=5)
        radio4 = tk.Radiobutton(tab3, text="Not Interested", value=2, variable=var1).grid(row=6)
        radio5 = tk.Radiobutton(tab3, text="Avoid", value=1, variable=var1).grid(row=7)
        nextbutton = tk.Button(tab3, text="NEXT FIELD", command= lambda: recurfield(ID_insert, tab3, fields, countofiterations, recordchoices, var1, label)).grid(row=8)
        skipbutton = tk.Button(tab3, text="SKIP ALL", command= lambda: Increasefield(ID_insert, tab3, fields, countofiterations, recordchoices, var1, label)).grid(row=8, column=2)
    except:
        hold = 0

def Increasefield(ID_insert, tab3, fields, countofiterations, recordchoices, var1, label):
    while countofiterations < 16:
        countofiterations=countofiterations+1
    recurfield(ID_insert, tab3, fields, countofiterations, recordchoices, var1, label)

def updatefields(ID_insert, recordchoices, fields, tab3):
    recordchoices.reverse()
    tab3.destroy()
    recordchoices.pop()
    recordchoices.reverse()
    handle = sql.connect("NEA.db")
    cursor = handle.cursor()
    cursor.execute("UPDATE USERS SET FIELDS = ? WHERE USERID = ?;", (str(recordchoices), ID_insert))
    handle.commit()
    handle.close()
    usedata(recordchoices, fields, ID_insert)# the array is 5 - very interested to 1 - avoid per field

def usedata(recordchoices, fields, ID_insert): #decide job by field, quallevel, work experience, if this is identical compare skills of the users that were recommended this to the current user. Then choose by the ratings of recommendations and count of recommendations.
    if recordchoices == []:
        recordchoices = ["5"]*len(fields)
    store=[]
    joblist = []
    #find highest interest fields
    sorts = recordchoices
    sorts.sort()
    if len(sorts) == "0":
        skip = True
    else:
        high = sorts[len(sorts)-1]
        for c in range(0, len(sorts)):
            if recordchoices[c] == high:
                store.append(c)
        while len(store) < 2:
            high = high-1
            for c in range(0, len(sorts)):
                if recordchoices[c] == high:
                    store.append(c)
        finalfields = []
        for i in range(0, len(store)):
            finalfields.append(fields[store[i]])
    all_ = []
    for e in range(0, len(finalfields)):
        handle = sql.connect("NEA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT JOBNAME FROM JOBS WHERE FIELD = ?;", (finalfields[e],))
        alljobsinfields = cursor.fetchall()
        handle.commit()
        handle.close()
        all_.append(alljobsinfields)
    fin = []
    for b in range(0, len(all_)):
        for c in range(0, len(all_[b])):
            punctuation = """!"#$%&'()*+-:;<=>?@[]^_`{|}~"""
            edited = ""
            string = str(all_[b][c])
            for i in string:
                if i not in punctuation:
                    edited += i
            edited = edited[:-2]
            fin.append(edited)
    # quallevel comparisons
    for c in range(0, len(fin)):
        fin[c] = str(fin[c])
        fin[c] = fin[c][:len(fin[c])-1]
        handle = sql.connect("NEA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT QUALLEVEL FROM JOBS WHERE JOBNAME LIKE ? AND IDLE = ?", ("%"+fin[c]+"%", 0)) # sql to remove the tuple status by using like.
        qualforjob = cursor.fetchall()
        handle.commit()
        handle.close()
        nameofqual = findcommonqual(qualforjob)
        handle = sql.connect("NEA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT QUALLEVEL FROM USERS WHERE USERID = ? AND USERID > ?", (ID_insert, "0"))
        userqual = cursor.fetchall()
        handle.commit()
        handle.close()
        userqual = str(userqual)
        userqual = userqual[3:len(userqual)-4]
        if userqual == nameofqual:
            joblist.append(fin[c])
    if len(joblist) > 2:
        workxp(joblist)
    else:
        display(job_list[0])

def findcommonqual(qualforjob):
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
        if numbers[len(numbers)-1] == float(quals[q]):
            nameofqual = quals[q-1]
        q=q-2
    return nameofqual
    
def workxp(joblist):
    if len(joblist) <= 15:
        worktab = ttk.Frame(tabcontrol)
        tabcontrol.add(worktab, text="WORK EXPERIENCE")
        tabcontrol.select(worktab)
        workxplabel = tk.Label(worktab, text=" ").grid(row=1)
        worklabel = tk.Label(worktab, text="Do you have any work experience in the following roles?").grid(row=2) 
        optionsforwork = ["3+ years", "1-3 years", "< 1 year"]
        varnames = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        namesofvariables = ["S"]*250
        for c in range(0, len(joblist)):
            varnames[c] = StringVar()
            varnames[c].set(optionsforwork[2])
            namesofvariables[c] = tk.Label(worktab, text=joblist[c]).grid(row=c+3)
            namesofvariables[c+1] = OptionMenu(worktab , varnames[c], *optionsforwork)
            namesofvariables[c+1].grid(row=c+3, column=1)
        finalise = tk.Button(worktab, text="Confirm", command= lambda: usingworkexp(varnames, joblist, worktab)).grid(row=294)
    else:
        joblist.remove(joblist[random.randint(0, len(joblist)-1)])
        workxp(joblist)
        
def usingworkexp(varnames, joblist, worktab):
    worktab.destroy()
    VAR = []
    final_list = []
    for r in range(0, len(joblist)):
        VAR.append(varnames[r].get())
    for p in range(0, len(joblist)):
        handle = sql.connect("NEA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT WORKEXP FROM JOBS WHERE JOBNAME LIKE ? AND IDLE = ?", ("%"+joblist[p]+"%", 0))
        workexp = cursor.fetchall()
        handle.commit()
        exp=""
        handle.close()
        punctuation = """!"#$%&'()*+-/:;=?@[\\]^_`{|}~"""
        edited = ""
        string = str(workexp)
        for i in string:
            if i not in punctuation:
                edited += i
        edited = edited.split(" ")
        edited[0] = str(edited[0])
        if edited[0] == "none,":
            exp = "< 1 year"
        elif edited[0] == "Little":
            exp = "< 1 year"
        elif edited[0] == "Extensive":
            exp = "3+ years"
        else:
            exp = "1-3 years"
        if VAR[p] == "1-3 years":
            if exp == "1-3 years":
                final_list.append(joblist[p])
            elif exp == "3+ years":
                final_list.append(joblist[p])
        elif exp == "< 1 year":
            final_list.append(joblist[p])
        elif VAR[p] == "3+ years":
            if exp == "< 1 year":
                no_overlap = True
            else:
                final_list.append(joblist[p])
    compare = []
    num = []
    if len(final_list) > 1: # sorting by amount of people the job employees (based on projected 2018 stats).
        for r in range(0, len(final_list)):
            handle = sql.connect("NEA.db")
            cursor = handle.cursor()
            cursor.execute("SELECT EMPLOYEES FROM JOBS WHERE JOBNAME LIKE ? AND JOBID > ?", ("%"+final_list[r]+"%", "0"))
            employ = cursor.fetchall()
            handle.commit()
            handle.close()
            punctuation = """!"#$%&'()*+-/, :;=?@[\\]^_`{|}~"""
            edited = ""
            string = str(employ)
            for i in string:
                if i not in punctuation:
                    edited += i
            employees = edited
            employees = re.sub("[^0-9]", "", employees)
            employees = employees[2:]
            if employees[:3] == "710":
                employees = employees[3:]
            compare.append(final_list[r])
            num.append(employees)
            compare.append(employees)
        num.sort()
        final_list = []
        for m in range(0, len(num)):
            for b in range(0, len(compare)):
                if num[m] == compare[b]:
                    final_list.append(compare[b-1])
        final_list.reverse()
    list_ = []
    a = False
    if final_list == []:
        final_list = joblist
    if len(final_list) > 3:
        list_.append(final_list[0])
        list_.append(final_list[1])
        list_.append(final_list[2])
        a = True
    if a == True:
        final_list = list_
    for l in range(0, len(final_list)):
        job_name = final_list[l]
        if job_name[0] == " ":
            job_name = job_name[1:]
        if job_name[len(job_name)-1] == "\\":
            job_name = job_name[:len(job_name)-1]
        display(job_name)

def display(job_name):
    result_tab = ttk.Frame(tabcontrol)
    tabcontrol.add(result_tab, text=job_name)
    tabcontrol.select(result_tab)
    handle = sql.connect("NEA.db")
    cursor = handle.cursor()
    cursor.execute("SELECT EMPLOYEES FROM JOBS WHERE JOBNAME LIKE ? AND JOBID > ?", ("%"+job_name+"%", "0"))
    employees = cursor.fetchall()
    handle.commit()
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
            count = count+1
        except:
            count = "N/A"
    rec_count = count
    rec_count = str(rec_count)
    rec_count = "Amount of suggestions: "+rec_count
    counting = tk.Label(result_tab, text=rec_count).grid(row=5, column=2)
    cursor.execute("UPDATE JOBS SET COUNT = ? WHERE JOBNAME LIKE ? AND JOBID > ?", (count, "%"+job_name+"%", "0"))
    handle.commit()
    employees = str(employees)
    employees = re.sub("[^0-9]", "", employees)
    employees = employees[2:]
    if employees[:2] == "72":
        employees = employees[2:]
    if employees == "":
        employees = "uncounted quantity of"
    jobname = tk.Label(result_tab, text=job_name).grid(row=1, column=1)
    employees = str(employees)
    employees = employees+" people employed in this role."
    jobemp = tk.Message(result_tab, text=employees).grid(row=2, column=2)
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
    sal = tk.Label(result_tab, text = salary).grid(row=3, column=2)
    currencyupdate = tk.Button(result_tab, text="Change Currency", command = lambda: currency(number_hold, result_tab, job_name, salary)).grid(row=4, column=2)
    jobdes = tk.Message(result_tab, text=descript).grid(row=2, column=1)
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
        SKILL_ = tk.Button(result_tab, text="SKILLS", command = lambda: displayskills(skills, var, job_name, result_tab)).grid(row=3, column=1)
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
    fields_ = tk.Label(result_tab, text=field).grid(row=4, column=1)
    fieldinfo = tk.Button(result_tab, text="Field Info", command = lambda: field_info(result_tab, field, job_name)).grid(row=5, column=1)
    searchlisting = tk.Button(result_tab, text="SEARCH FOR LISTINGS", command = lambda: listingsearch(result_tab, job_name)).grid(row=6, column=2)
    qualsbutton = tk.Button(result_tab, text="Qual Split", command = lambda: qual_split(job_name)).grid(row=6, column=1)
    TEMP_CV_button = tk.Button(result_tab, text="Create recommendation file (PDF)", command = lambda: RECtemplate(job_name, result_tab, field, descript, skills, salary)).grid(row=7, column=1)
    similarbutton = tk.Button(result_tab, text="SIMILAR JOBS", command = lambda: similar_jobs(field, job_name, result_tab)).grid(row=1, column=2)
    rating_button = tk.Button(result_tab, text="Rate this job", command = lambda: ratingadd(job_name, result_tab)).grid(row=1, column=4)
    space = tk.Label(result_tab, text ="").grid(row=19, column=2)
    _button = tk.Button(result_tab, text="MAIN MENU", command = lambda: mainmenu()).grid(row=20, column=2)
    tab_button = tk.Button(result_tab, text="CLOSE TAB", command = lambda: closetab(result_tab)).grid(row=20, column=1)

def RECtemplate(job_name, result_tab, field, descript, skills, salary):
    try:
        from fpdf import FPDF
        file_handle = job_name+".pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
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
        fileinfolder = tk.Message(result_tab, text="File Created, Should be in the same folder as this file.").grid(row=8, column=1)
    except:
        fileinfoldererror = tk.Message(result_tab, text="File error, file could not be produced.").grid(row=8, column=1)
    
def similar_jobs(field, job_name, result_tab):
    result_tab.destroy()
    handle = sql.connect("NEA.db")
    cursor = handle.cursor()
    cursor.execute("SELECT JOBNAME FROM JOBS WHERE FIELD LIKE ? AND JOBID > ?", ("%"+field+"%", "0"))
    joblist = cursor.fetchall()
    handle.commit()
    fin = []
    for b in range(0, len(joblist)):
        punctuation = """!"#$%&'()*+-:;<=>?@[]^_`{|}~"""
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
    nameofqual = findcommonqual(quals)
    final = []
    for i in range(0, len(fin)):
        cursor.execute("SELECT QUALLEVEL FROM JOBS WHERE JOBNAME LIKE ? AND JOBID > ?", ("%"+fin[i]+"%", "0"))
        jobqual = cursor.fetchall()
        handle.commit()
        jobqualname = findcommonqual(jobqual)
        if jobqualname == nameofqual:
            final.append(fin[i])
    if final == []:
        while len(fin) > 5:
            fin.remove(fin[random.randint(0, len(fin)-1)])
        final = fin
    similar_tab = ttk.Frame(tabcontrol)
    tabcontrol.add(similar_tab, text="Similar Jobs")
    tabcontrol.select(similar_tab)
    for o in range(0, len(fin)):
        labels = tk.Label(similar_tab, text=fin[o]).grid(row=o+1)
    back = tk.Button(similar_tab, text="Back", command = lambda: [display(job_name), closetab(similar_tab)]).grid(row=len(fin)+1)
    
def ratingadd(job_name, result_tab):
    one_to_five = [1, 2, 3, 4, 5]
    stars = IntVar()
    stars.set(3)
    ratinglabel = tk.Label(result_tab, text ="Rating: ").grid(row=2, column=4)
    star_rating = tk.OptionMenu(result_tab, stars, *one_to_five).grid(row=2, column=5)
    commentlabel = tk.Label(result_tab, text ="Comment: ").grid(row=3, column=4)
    comment = tk.Entry(result_tab)
    comment.grid(row=3, column=5)
    Enter_button = tk.Button(result_tab, text="Enter", command = lambda: ratingadd2(job_name, comment, stars, result_tab)).grid(row=5, column=5)

def ratingadd2(job_name, comment, stars, result_tab):
    stars_ = stars.get()
    comment_ = comment.get()
    handle = sql.connect("NEA.db")
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
    display(job_name)
    
def qual_split(job_name):
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except:
        cont = True
    handle = sql.connect("NEA.db")
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
    
        
def field_info(result_tab, field, job_name):
    result_tab.destroy()
    fieldinfo_tab = ttk.Frame(tabcontrol)
    tabcontrol.add(fieldinfo_tab, text="Field Info")
    tabcontrol.select(fieldinfo_tab)
    fields_ = tk.Label(fieldinfo_tab, text=field).grid(row=1)
    handle = sql.connect("NEA.db")
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
    fields_ = tk.Label(fieldinfo_tab, text=total_count).grid(row=2)
    back = tk.Button(fieldinfo_tab, text="Back", command = lambda: [closetab(fieldinfo_tab), display(job_name)]).grid(row=4, column=1)
    
def currency(number_hold, result_tab, job_name, salary):
    result_tab.destroy()
    urlof_live = "https://transferwise.com/gb/currency-converter/usd-to-~-rate?amount=#"
    urlof_live = urlof_live.replace("#", number_hold)
    currency_tab = ttk.Frame(tabcontrol)
    tabcontrol.add(currency_tab, text="Currency Change")
    tabcontrol.select(currency_tab)
    Sal_set = tk.Label(currency_tab, text = salary).grid(row=2)
    list_of_currency = ["GBP", "INR", "ISK", "CAD", "EUR", "SDG", "AUD", "MXN", "SEK", "NOK", "JPY", "BRL"]
    vars_ = StringVar()
    vars_.set(list_of_currency[random.randint(0, len(list_of_currency)-1)])
    opti = tk.OptionMenu(currency_tab, vars_, *list_of_currency).grid(row=3)
    confirming = tk.Button(currency_tab, text="Confirm", command = lambda: use_currency(urlof_live, currency_tab, job_name, number_hold, vars_)).grid(row=4)
    back = tk.Button(currency_tab, text="Back", command = lambda: [closetab(currency_tab), display(job_name)]).grid(row=4, column=1)

def use_currency(urlof_live, currency_tab, job_name, number_hold, vars_):
    currency_tab.destroy()
    vars_ = vars_.get()
    vars_ = vars_.lower()
    urlof_live = urlof_live.replace("~", vars_)
    try:
        from bs4 import BeautifulSoup
        import requests
    except:
        cont = True
    response = requests.get(urlof_live)
    soup = BeautifulSoup(response.content, "html.parser")
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
    currency_tab2 = ttk.Frame(tabcontrol)
    tabcontrol.add(currency_tab2, text="Currency Result")
    tabcontrol.select(currency_tab2)
    finalsum = tk.Label(currency_tab2, text = sal).grid(row=1)
    back = tk.Button(currency_tab2, text="Back", command = lambda: [closetab(currency_tab2), display(job_name)]).grid(row=2)
    
def listingsearch(result_tab, job_name):
    result_tab.destroy()
    f = open("adaptive-listings.txt")
    name = []
    url = []
    rep = []
    for i in range(0, 6):
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
    rep[len(rep)-1] = rep[len(rep)-1]+"0"
    options_tab = ttk.Frame(tabcontrol)
    tabcontrol.add(options_tab, text="What site?")
    tabcontrol.select(options_tab)
    tabcontrol.select(options_tab)
    VAR = StringVar()
    VAR.set(name[random.randint(0, len(name)-1)])
    opt = tk.OptionMenu(options_tab, VAR, *name).grid(row=1)
    confirm = tk.Button(options_tab, text="Confirm", command= lambda: [closetab(options_tab), listings_(job_name, name, url, rep, VAR)]).grid(row=2)
    back =  tk.Button(options_tab, text="Back", command= lambda: [closetab(options_tab), display(job_name)]).grid(row=3)

def copytoclip(url):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(url)
    r.update()
    r.destroy()
    
def listings_(job_name, name, url, rep, VAR):
    VAR = VAR.get()
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
    url = url.replace("~", job_name)
    jobresults = ttk.Frame(tabcontrol)
    tabcontrol.add(jobresults, text="JOBS FROM LISTINGS")
    tabcontrol.select(jobresults)
    url_label = tk.Label(jobresults, text= url).grid(row=1)
    copytoclip_ = tk.Button(jobresults, text="Copy Url to Clipboard", command = lambda: copytoclip(url)).grid(row=2)
    result_tab = ttk.Frame(tabcontrol)
    back_button = tk.Button(jobresults, text="Back", command = lambda: [closetab(jobresults), listingsearch(result_tab, hold)]).grid(row=9)

def displayskills(skills, var, job_name, result_tab):
    result_tab.destroy()
    skill_tab = ttk.Frame(tabcontrol)
    tabcontrol.add(skill_tab, text="JOB SKILLS")
    tabcontrol.select(skill_tab)
    tag = job_name + " skills:"
    label = tk.Label(skill_tab, text=tag).grid(row=1)
    labelgap = tk.Label(skill_tab, text=" ").grid(row=2)
    for n in range(0, len(skills)-1):
            var[n] = tk.Label(skill_tab, text=skills[n]).grid(row=n+3)
    backbutton = tk.Button(skill_tab, text="BACK", command = lambda: [display(job_name), closetab(skill_tab)]).grid(row=20)
            
def closetab(result_tab):
    result_tab.destroy()
                                                                         
def search(searchjobentry, tab1):
    #search in database word by word of each job and use LIKE and % to widen critera. If no results, option to add a job to be reviewed.
    searchjobentry = searchjobentry.get()
    searchjobentry = searchjobentry.split(" ")
    results = []
    for c in range(0, len(searchjobentry)):
        handle = sql.connect("NEA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT JOBNAME FROM JOBS WHERE JOBNAME LIKE ? AND IDLE = ?", ("%"+searchjobentry[c]+"%", 0))
        jobnames = cursor.fetchall()
        handle.commit()
        handle.close()
        results.append(jobnames)
    if results == [[]]:
        missingjob1(tab1)
    else:
        tab1.destroy()
        searchmenu(results)

def searchmenu(results):
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
    if job_name[0] == " ":
        job_name = job_name[1:]
    if job_name[len(job_name)-1] == "\\":
        job_name = job_name[:len(job_name)-1]
    display(job_name)

def deletealltabs(variables, new):
    for u in range(0, len(new)):
        variables[u].destroy()
    
def missingjob1(tab1):
    tab1.destroy()
    #give options 
    missing = ttk.Frame(tabcontrol)
    tabcontrol.add(missing, text="ADD JOB")
    tabcontrol.select(missing)
    JOB_ = tk.Label(missing, text="THERE WAS NO FOUND JOBS, add a job to be reviewed by an Admin.").grid(row=1, column=1)
    JOB_name = tk.Label(missing, text="JOBNAME:").grid(row=2)
    JOB__name = tk.Entry(missing)
    JOB__name.grid(row=2, column=1)
    JOB_des = tk.Label(missing, text="DESCRIPTION:").grid(row=3)
    JOB__des = tk.Entry(missing)
    JOB__des.grid(row=3, column=1)
    JOB_field = tk.Label(missing, text="FIELD:").grid(row=4)
    JOB__field = tk.Entry(missing)
    JOB__field.grid(row=4, column=1)
    JOB_button = tk.Button(missing, text="Back", command = lambda: [closetab(missing), mainmenu()]).grid(row=5)
    JOB_button = tk.Button(missing, text="Confirm", command = lambda: missingjob2(JOB__name, missing, JOB__des, JOB_field)).grid(row=5, column=1)
    
def missingjob2(JOB__name, missing, JOB__des,  JOB_field):
    #add info from missingjob1 into database to be reviewed by an admin (aka. me)
    JOB__name = JOB__name.get()
    JOB__des = JOB__des.get()
    missing.destroy()
    handle = sql.connect("NEA.db")
    cursor = handle.cursor()
    cursor.execute("INSERT INTO USER_RECOMMENDATIONS VALUES(?,?,?)", (JOB__name, JOB__des, JOB_field))
    handle.commit()
    handle.close()
    mainmenu()
    
def popular(tab1):
    tab1.destroy()
    # uses count of recommendations for each job
    handle = sql.connect("NEA.db")
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
    handle = sql.connect("NEA.db")
    cursor = handle.cursor()
    names = []
    for t in range(0, 5):
        cursor.execute("SELECT JOBNAME FROM JOBS WHERE COUNT = ? AND IDLE = ?", (counts[len(counts)-t-1], 0))
        job_name = cursor.fetchall()
        handle.commit()
        if len(job_name) > 1:
            try:
                job_name = job_name[t]
            except:
                job_name = job_name[random.randint(0,1)]
        job_name = str(job_name)
        job_name = job_name[2: len(job_name)-5]
        if job_name[0] == "'":
            job_name = job_name[1:]
        if job_name[len(job_name)-1] == "\\":
            job_name = job_name[:len(job_name)-1]
        names.append(job_name)
    handle.close()
    new_tab = ttk.Frame(tabcontrol)
    tabcontrol.add(new_tab, text="POPULAR JOBS")
    tabcontrol.select(new_tab)
    label= tk.Label(new_tab, text= "POPULAR JOBS:").grid(row=1)
    VAR = StringVar()
    VAR.set(names[random.randint(0, len(names)-1)])
    options = tk.OptionMenu(new_tab, VAR, *names).grid(row=1, column=1)
    confirmation = tk.Button(new_tab, text="Confirm", command = lambda: [popular2(VAR), del_popularselect(new_tab)]).grid(row=2)
    back_main = tk.Button(new_tab, text="Back", command = lambda: [del_popularselect(new_tab), mainmenu()]).grid(row=3)

def del_popularselect(new_tab):
    new_tab.destroy()
    
def popular2(VAR):
    job_name = VAR.get()
    display(job_name)
    
def fieldstart(tab1):
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
    label= tk.Label(fieldsearch, text= "Choose a Field").grid(row=1)
    variance = StringVar()
    variance.set(fields[random.randint(0, len(fields)-1)])
    options = tk.OptionMenu(fieldsearch, variance, *fields).grid(row=2)
    confirmation = tk.Button(fieldsearch, text="Confirm", command = lambda: field_data(variance, fieldsearch)).grid(row=3)
    back_main = tk.Button(fieldsearch, text="Back", command = lambda: [del_fieldsearch(fieldsearch), mainmenu()]).grid(row=4)

def del_fieldsearch(fieldsearch):
    fieldsearch.destroy()
    
def field_data(variance, fieldsearch):
    variance = variance.get()
    fieldsearch.destroy()
    handle = sql.connect("NEA.db")
    cursor = handle.cursor()
    cursor.execute(("SELECT JOBNAME FROM JOBS WHERE FIELD = ? AND IDLE = ?"), (variance, 0))
    names = cursor.fetchall()
    handle.commit()
    handle.close()
    punctuation = """!"#$%&'()*+-:;=?@[\\]^_`{|'}~"""
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
    options = tk.OptionMenu(results_field, var_job, *new).grid(row=1)
    confirm= tk.Button(results_field, text="Confirm", command = lambda: getresultoffield_search(var_job, results_field)).grid(row=2)
    tab1 = ttk.Frame(tabcontrol)
    back= tk.Button(results_field, text="Back", command= lambda: [fieldstart(tab1), delete_fieldresults(tab1, results_field)]).grid(row=3)

def delete_fieldresults(tab1, results_field):
    tab1.destroy()
    results_field.destroy()
    
def getresultoffield_search(var_job, results_field):
    var_job = var_job.get()
    results_field.destroy()
    job_name = var_job
    if job_name[0] == " ":
        job_name = job_name[1:]
    display(job_name)

def rating(tab1):
    tab1.destroy() # after recommendation, user gives feedback rating 0-5 and this will search jobs
    handle = sql.connect("NEA.db")
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
        handle = sql.connect("NEA.db")
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
    for y in range(0, 5):
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
        handle = sql.connect("NEA.db")
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
    label = tk.Label(results_field, text="Highly rated jobs: ").grid(row=2)
    options = OptionMenu(results_field, var, *job_names).grid(row=2, column=1)
    cont = tk.Button(results_field, text="Continue", command= lambda: [closetab(results_field), getvar(var)]).grid(row=3, column=1)
    back = tk.Button(results_field, text="Back", command= lambda: [closetab(results_field), mainmenu()]).grid(row=3)

def getvar(var):
    var = var.get()
    display(var)

def loaddata():
    txts = ["Science.txt", "Agri.txt", "Arch.txt", "Business.txt", "Arts.txt", "Finance.txt", "Gov.txt", "Health.txt", "Hospit.txt", "Human.txt", "IT.txt", "Law.txt", "Manufact.txt", "Market.txt", "Transport.txt", "Edu.txt"]
    counttxt = 0
    alljobs = []
    fields = []
    jobid = 0
    for x in range(0, len(txts)):
        file = open(txts[counttxt])
        fieldjob = file.readlines()
        fieldname = fieldjob[0]
        fields.append(fieldname)
        a = 1
        aruntime = len(fieldjob)-1
        aruntime = aruntime/2
        aruntime = int(aruntime)
        for x in range(0, aruntime):
            name = fieldjob[a]
            url = fieldjob[a+1]
            a = a+2
            jobid = jobid+1
            handle = sql.connect("NEA.db")
            cursor = handle.cursor()
            cursor.execute("INSERT INTO JOBS VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (jobid, name, url, ".", ".", ".", ".", ".", fieldname,".", ".", "0"))
            handle.commit()
            handle.close()
        counttxt = counttxt+1
    counts = -1
    fieldlist=[]
    for x in range(0, len(fields)):
        counts=counts+1
        item = fields[counts]
        item = item.rstrip()
        fieldlist.append(item)
    return fieldlist
    
def getskillslist():
    handle = sql.connect("NEA.db")
    cursor = handle.cursor()
    cursor.execute("SELECT JOBS.URL FROM JOBS WHERE JOBS.JOBID > 0")
    URLlist = cursor.fetchall()
    handle.commit()
    handle.close()
    URLs=[]
    counts=0
    count = 1
    for p in range(0, len(URLlist)):
        link = URLlist[counts]
        link = str(link)
        link = link.replace(")", "")
        link = link.replace("(", "")
        link = link.replace("\"", "")
        link = link.rstrip('\n')
        link = link.replace("'", "")
        link = link.replace(",", "")
        if link[len(link)-1] == 'n':
            link = link[:-2]
        counts=counts+1
        URLs.append(link)
    iterate = 0
    try:
        from bs4 import BeautifulSoup
        import requests
    except:
        cont = True
    for job in range(0, len(URLs)):
        websiteurl = URLs[iterate]
        response = requests.get(websiteurl)
        soup = BeautifulSoup(response.content, "html.parser")
        soup.prettify()
        mydivs = soup.findAll("div", {"class": "careerSummaryValue"})
        salary = re.sub('[^0-9]', '', str(mydivs))
        if salary == "": # all salaries are per year in dollars
            salary = 46000
        #print(salary, iterate, websiteurl)
        try:
            quallevel = soup.find("div", {"class": "careerSummaryTip"}).find('a')
        except:
            quallevel = soup.find("div", {"class": "careerSummaryTip"})
        strquallevel = str(quallevel)
        quallevelfirst = strquallevel[167:495]
        fullstops = 0
        firsttwo = []
        loop = True
        for char in quallevelfirst:
            if loop == True:
                if char == "&":
                    fullstops=fullstops+1
                elif fullstops == 1:
                        loop = False
                else:
                    firsttwo.append(char)
        stringoutput = ""
        for i in range(0, len(firsttwo)):
            a = firsttwo[i]
            stringoutput = stringoutput+a
        if stringoutput == "" or len(stringoutput) == 1:
            stringoutput = "none"
        #print(stringoutput) #amount of work experience required
        try:
            keyskills = soup.find("div", {"class": "careerTopSkills"}).text
            keyskills = "".join([s for s in keyskills.strip().splitlines(True) if s.strip("\r\n").strip()])
            keyskills = keyskills.splitlines()
            #print(keyskills) #top skills, job specific
        except:
            keyskills = "none"
            #print(keyskills)
        try:
            educat = soup.find("div", {"class": "careerEducationContainer"}).find("script")
            educat = str(educat)
            educat = educat[600:1700]
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
                cert1 = ''.join(map(str, cert1))
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
            education = "Bachelor"
        #print(store)# education level needed in percentage ratios
        description = soup.find("div", {"class": "careerSnapshotContainer"}).text
        description = str(description)
        description = description[42:300]
        description = list(description)
        des = []
        loop = True
        for char in description:
            if loop == True:
                if char == ".":
                    des.append(char)
                    loop = False
                else:
                    des.append(char)
        des = ''.join(map(str, des))
        #print(des) #description of job
        # get total employed in that professtion
        employ = 0
        websiteurl = URLs[iterate]
        response = requests.get(websiteurl+"/outlook/")
        soup = BeautifulSoup(response.content, "html.parser")
        soup.prettify()
        employment = soup.find("div", {"class": "generalMainContentCol"}).find("script").text
        employment = employment[2000:2500]
        employment = re.sub("[^0-9]", "", employment)
        employ = str(employment[21:len(employment)])
        employ = list(employ)
        new_employ = []
        set_ = False
        for c in range(0, len(employ)):
            if employ[c] == "0":
                set_ = True
                new_employ.append(employ[c])
            elif set_ == True:
                new_employ.append(employ[c])
        try:
            new_employ.remove(new_employ[0])
        except:
            continue_ = True
        employ = str(new_employ)
        #print(employ)
        handle = sql.connect("NEA.db")
        cursor = handle.cursor()
        cursor.execute("UPDATE JOBS SET SKILLS = ?, QUALLEVEL = ?, DESCRIPTION = ?, SALARY = ?, WORKEXP = ?, EMPLOYEES = ? WHERE JOBID = ?;", (str(keyskills), str(store), des, salary, stringoutput, employ, count))
        handle.commit()
        count=count+1
        iterate = iterate+1

try:
    handle = sql.connect("NEA.db")
    cursor = handle.cursor()
    cursor.execute("CREATE TABLE JOBS(JOBID INT, JOBNAME TEXT, URL TEXT, SKILLS TEXT, QUALLEVEL TEXT, WORKEXP TEXT, SALARY INT, DESCRIPTION TEXT, FIELD TEXT, COUNT INT, EMPLOYEES INT, IDLE INT)")
    cursor.execute("CREATE TABLE USERS(USERID TEXT, NAME TEXT, PASSWORD TEXT, QUALLEVEL TEXT, SKILL1 TEXT, SKILL2 TEXT, SKILL3 TEXT, FIELDS TEXT, CURRENTJOB TEXT, ANSWERS BLOB)")
    cursor.execute("CREATE TABLE RATINGS(JOBID INT, RATING INT, COMMENT TEXT)")
    cursor.execute("CREATE TABLE WEBLIST(WEBID INT, WEBURL TEXT)")
    cursor.execute("CREATE TABLE USER_RECOMMENDATIONS(JOBNAME TEXT, DESCRIPTION TEXT, FIELD TEXT)")
    handle.commit()
    handle.close()
    fieldlist = loaddata()
    getskillslist()
except:
    cont = True

#create main menu upon staring program
window=tk.Tk()
window.title("JOB FINDER")
tabcontrol = ttk.Notebook(window)
mainmenu()

tabcontrol.pack(expand=1, fill="both")
window.mainloop()
