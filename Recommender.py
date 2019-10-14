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

class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground

class both:
    def home(self):
            tab0 = ttk.Frame(tabcontrol)
            tabcontrol.add(tab0, text="HOME")
            tabcontrol.select(tab0)
            HoverButton(tab0, height = 10, width = 30 , activebackground='black', fg="white", bg="red", text="UNIVERSITY", command = lambda: [both.closetab(tab0), uni.unimenu()]).grid(row=1)
            HoverButton(tab0, height = 10, width = 30 , activebackground='black', fg="white", bg="blue", text="FIND JOBS", command = lambda: [both.closetab(tab0), job.mainmenu()]).grid(row=1, column=1)

    def closetab(self, result_tab):
            result_tab.destroy()

    def hash_password(self, password):
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
        
    def verify_password(self, stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

    def login(self, attempts, tab1, IDENTentry, Passwordentry, uniorjob):
        IDENT_insert = IDENTentry.get()
        PIN_insert = Passwordentry.get()
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT USERS.USERID FROM USERS")
        ids = cursor.fetchall()
        handle.commit()
        idsclean = []
        for x in range(0, len(ids)):
            a = str(ids[x])
            b = a.strip('(),/\'')
            idsclean.append(b)
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
                TrueorFalse = both.verify_password(PINrecieved, PIN_insert)
                if TrueorFalse == True:
                    both.changelogin(tab1, IDENT_insert, PIN_insert, uniorjob)
                    k = 8
            i = i+1
        attempt=attempts+1
        # incorrect entry tab with a back to main menu button
        tab1.destroy()
        if k != 8:
            errorlogin = ttk.Frame(tabcontrol)
            tabcontrol.add(errorlogin, text="INVALID")
            tk.Label(errorlogin, text="ID or Password is incorrect", font="Ariel 15 bold italic", fg="blue").grid(row=1)
            HoverButton(errorlogin, text="Back to Main Menu", activebackground='blue', fg="white", bg="black", command= lambda: [both.closetab(errorlogin), job.mainmenu()]).grid(row=2)
            
    def changelogin(self, tab1, IDENT_insert, PIN_insert, uniorjob):
        tab1.destroy()
        #give option to change details (other than id/password)
        tab4 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab4, text="Step 2")
        tabcontrol.select(tab4)
        ID_insert = IDENT_insert
        HoverButton(tab4, activebackground='blue', fg="white", bg="black", text="edit your data", command = lambda: both.changingdata(ID_insert, PIN_insert, tab4, uniorjob)).grid(row=1)
        if uniorjob == False:
            HoverButton(tab4, activebackground='blue', fg="white", bg="black", text="Find Personalised Reccomendations", command = lambda: job.fieldq(ID_insert, tab4)).grid(row=2)
        elif uniorjob == True:
            HoverButton(tab4, activebackground='blue', fg="white", bg="black", text="Find Personalised Reccomendations", command = lambda: uni.uni_quals(ID_insert, tab4)).grid(row=2)

    def changingdata(self, ID_insert, PIN_insert, tab4, uniorjob):
        tab4.destroy()
        tab4 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab4, text="Update Info")
        tabcontrol.select(tab4)
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT USERID, NAME, QUALLEVEL, SKILL1, SKILL2, SKILL3, CURRENTJOB FROM USERS WHERE USERID = ? AND USERID > ?;", (ID_insert, "0"))
        userinfo = cursor.fetchall()
        handle.commit()
        handle.close()
        for h in range(0, len(userinfo)):
            punctuation = """!"#$%&'()*+/:;<=>?@[\\]^_`{|}~"""
            user_info = ""
            string = str(userinfo[h])
            for e in string:
                if e not in punctuation:
                    user_info += e
        user_info = user_info.split(",")
        tk.Label(tab4, text="Name:").grid(row=1)
        ident = tk.Entry(tab4)
        ident.insert(0,user_info[1])
        ident.grid(row=1, column=1)
        tk.Label(tab4, text="Qual:").grid(row=2)
        qual = tk.Entry(tab4)
        qual.insert(0,user_info[2])
        qual.grid(row=2, column=1)
        tk.Label(tab4, text="SKILL:").grid(row=3)
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
        OptionMenu(tab4 , vara, *skill_list).grid(row=3, column=1)
        OptionMenu(tab4 , varb, *skill_list).grid(row=3, column=2)
        OptionMenu(tab4 , varc, *skill_list).grid(row=3, column=3)
        tk.Label(tab4, text="Current Job:").grid(row=4)
        current = tk.Entry(tab4)
        current.insert(0,user_info[6])
        current.grid(row=4, column=1)
        HoverButton(tab4, activebackground='blue', fg="white", bg="black", text="Commit Changes", command = lambda: both.updatechanges(vara, varb, varc, qual, ID_insert, PIN_insert, ident, current, tab4, uniorjob)).grid(row=5)

    def updatechanges(self, vara, varb, varc, qual, ID_insert, PIN_insert, ident, current, tab4, uniorjob):
        skill1 = vara.get()
        skill2 = varb.get()
        skill3 = varc.get()
        qual = qual.get()
        name = ident.get()
        current = current.get()
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("UPDATE USERS SET QUALLEVEL = ?, NAME = ?, CURRENTJOB = ?, SKILL1 = ?, SKILL2 = ?, SKILL3 = ? WHERE USERID = ?", (qual, name, current, skill1, skill2, skill3, ID_insert))
        handle.commit()
        handle.close()
        tab4.destroy()
        tab4 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab4, text="DELETE ME")
        if uniorjob == False:
            job.fieldq(ID_insert, tab4)
        elif uniorjob == True:
            uni.uni_quals(ID_insert, tab4)
            
    def loguser(self, ID_insert, tab6, nameentry, tkvar, abvar, advar, acvar, currententry, Password, IDentry, tab1, choices, uniorjob):
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
            Password_insert1 = both.hash_password(Password_insert)
            if username_insert == "":
                username_insert = "NULL"
            if current_insert == "":
                current_insert = "N"
            tab6.destroy()
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            cursor.execute("INSERT INTO USERS VALUES(?,?,?,?,?,?,?,?,?)", (ID_insert, username_insert, Password_insert1, quallevel_insert, skill1_insert, skill2_insert, skill3_insert, ".", current_insert))
            handle.commit()
            handle.close()
            #could delete if not required and just run field function
            tab4 = ttk.Frame(tabcontrol)
            tabcontrol.add(tab4, text="REMEMBER THIS")
            tabcontrol.select(tab4)
            tk.Label(tab4, text="Remember these to login in next time to avoid re-completing the questions").grid(row=1)
            tk.Label(tab4, text="ID:").grid(row=2)
            tk.Label(tab4, text=ID_insert).grid(row=2, column=1)
            tk.Label(tab4, text="Password:").grid(row=3)
            counted = 0
            for char in Password_insert:
                if char == "_":
                    counted = counted+1
            if counted > 1:
                counted = str(counted)
                Password_insert = str(Password_insert)
                Password_insert = Password_insert + " with " + counted + " underscores."
            tk.Label(tab4, text=Password_insert).grid(row=3, column=1)
            if uniorjob == False:
                HoverButton(tab4, activebackground='blue', fg="white", bg="black", text="Let's answer some questions", command= lambda: job.fieldq(ID_insert, tab4)).grid(row=4, column=1)
            elif uniorjob == True:
                HoverButton(tab4, activebackground='blue', fg="white", bg="black", text="Let's answer some questions", command= lambda: uni.uni_quals(ID_insert, tab4)).grid(row=4, column=1)

    def user1(self, IDentry, tab1, uniorjob):
        choices = ["< High School Diploma", "High School Diploma", "Master", "Bachelor", "Associate", "Some College", "Doctoral Degree", "Vocational Certificate"]
        z = False
        ID_insert = IDentry.get()
        handle = sql.connect("RecommendDATA.db")
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
                    tk.Label(error, text="ID is already taken...").grid(row=1)
                    HoverButton(error, activebackground='blue', fg="white", bg="black", text="Back to Main Menu", command = lambda: [closetab(error), job.mainmenu()]).grid(row=2)
        if z == False:
            tab6 = ttk.Frame(tabcontrol)
            tabcontrol.add(tab6, text="CREATE USER")
            tabcontrol.select(tab6)
            tk.Label(tab6, text="NAME: ").grid(row=1)
            nameentry = tk.Entry(tab6)
            nameentry.grid(row=1, column=1)
            tkvar = StringVar()
            tkvar.set(choices[random.randint(0, len(choices)-1)])
            tk.Label(tab6, text="CHOOSE HIGHEST QULAIFICATION LEVEL ACHIEVED:").grid(row=2)
            tk.OptionMenu(tab6 , tkvar, *choices).grid(row=2, column=1)
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
            tk.Label(tab6, text="MOST APPLICABLE SKILLS FOR YOU:").grid(row=3)
            OptionMenu(tab6 , abvar, *skill_list).grid(row=3, column=1)
            OptionMenu(tab6 , acvar, *skill_list).grid(row=3, column=2)
            OptionMenu(tab6 , advar, *skill_list).grid(row=3, column=3)
            tk.Label(tab6, text="CURRENT JOB (N IF NO JOB): ").grid(row=4)
            currententry = tk.Entry(tab6)
            currententry.grid(row=4, column=1)
            tk.Label(tab6, text="Password: ").grid(row=5)
            Password = tk.Entry(tab6)
            Password.grid(row=5, column=1)
            tab1 = ttk.Frame(tabcontrol)
            HoverButton(tab6, activebackground='blue', fg="white", bg="black", text="ENTER", command= lambda: both.loguser(ID_insert, tab6, nameentry, tkvar, abvar, acvar, advar, currententry, Password, IDentry, tab1, choices, uniorjob)).grid(row=5, column=2)


class uni:
    def unimenu(self):
        attempts = 0
        uniorjob = True
        tab0 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab0, text="Uni Menu")
        tabcontrol.select(tab0)
        tk.Label(tab0, fg="red", text="University Research Tool", font="Ariel 18").grid(row=2+1, columnspan=3)
        tk.Label(tab0, text=" ").grid(row=3+1)
        HoverButton(tab0, activebackground='red', fg="white", bg="black", text="Overall Rankings", command = lambda: [both.closetab(tab0), uni.overallranking()]).grid(row=4+1)
        tk.Label(tab0, text=" ").grid(row=5+1)
        tk.Label(tab0, text= "SEARCH UNI:", font= "Ariel 15 bold italic", fg="Black").grid(row=6+1, column=1)
        entrybox = tk.Entry(tab0)
        entrybox.insert(END, "University Name")
        entrybox.grid(row=7+1, column=1)
        HoverButton(tab0, activebackground='red', fg="white", bg="black", text="ENTER", command = lambda: uni.searchbyuni(entrybox, tab0)).grid(row=8+1, column=1)
        HoverButton(tab0, activebackground='red', fg="white", bg="black", text="Subject Search", command = lambda: [both.closetab(tab0), uni.searchbysub()]).grid(row=4+1, column=2)
        tk.Label(tab0, text=" ").grid(row=9+1)
        tk.Label(tab0, text="LOGIN:", font="Ariel 15 bold italic", fg="red").grid(row=10+1, column=1)
        IDENTentry = tk.Entry(tab0)
        IDENTentry.insert(END, "ID")
        IDENTentry.grid(row=11+1, column=1)
        Passwordentry = tk.Entry(tab0)
        Passwordentry.insert(END, "Password")
        Passwordentry.grid(row=12+1, column=1)
        #resetpin = tk.Button(tab1, text="FORGOT PIN", command = lambda: reset()).grid(row=7, column=3)
        HoverButton(tab0, activebackground='red', fg="white", bg="red", text="ENTER", command= lambda: both.login(attempts, tab0, IDENTentry, Passwordentry, uniorjob)).grid(row=13+1, column=1)
        tk.Label(tab0, text=" ").grid(row=14+1)
        tk.Label(tab0, text="NEW USER:", font="Ariel 15 bold italic", fg="red").grid(row=15+1, column=1)
        IDentry = tk.Entry(tab0)
        IDentry.insert(END, "ID")
        IDentry.grid(row=19+1, column=1)
        HoverButton(tab0, activebackground='black', fg="white", bg="red", text="ENTER", command = lambda: both.user1(IDentry, tab0, uniorjob)).grid(row=20+1, column=1)
        tk.Label(tab0, text = " ").grid(row=25+1)
        HoverButton(tab0, activebackground='black', fg="white", bg="blue", text="Home", command = lambda: [both.closetab(tab0), both.home()]).grid(row=26+1, column=1)

    def uni_quals(self, ID_insert, tab4):
        both.closetab(tab4)
        tab0 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab0, text="Enter Grades")
        tabcontrol.select(tab0)
        tk.Label(tab0, text= "Total UCAS points = ").grid(row=1)
        digit3 = IntVar()
        digit3.set("1")
        zero_to_nine = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        OptionMenu(tab0, digit3, *zero_to_nine).grid(row=1, column=2)
        digit2 = IntVar()
        digit2.set("5")
        OptionMenu(tab0, digit2, *zero_to_nine).grid(row=1, column=3)
        digit1 = IntVar()
        digit1.set("0")
        OptionMenu(tab0, digit1, *zero_to_nine).grid(row=1, column=4)
        arts_var = StringVar()
        yesno = ["Yes", "No"]
        arts_var.set(yesno[1])
        OptionMenu(tab0, arts_var, *yesno).grid(row=2, column=2)
        tk.Label(tab0, text = "Are you interested in studying arts, drama or music related cources?").grid(row=2, column=1)
        HoverButton(tab0, activebackground='black', fg="white", bg="blue", text="ENTER", command = lambda: uni.calculate_uni(ID_insert, digit3, digit2, digit1, tab0, arts_var)).grid(row=3, column=4)
        
    def calculate_uni(self, ID_insert, digit1, digit2, digit3, tab0, arts_var):
        digit1 = digit1.get()
        digit2 = digit2.get()
        digit3 = digit3.get()
        arts_var = arts_var.get()
        points = str(digit1)+str(digit2)+str(digit3)
        points = int(points)
        both.closetab(tab0)
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT UNINAME FROM UNIENTRY WHERE UCAS <= ? AND  UCAS != ?;", (points, "0"))
        entry = cursor.fetchall()
        handle.commit()
        handle.close()
        for x in range(0, len(entry)):
            entry[x] = str(entry[x])
            entry[x] = entry[x][2:len(entry[x])-3]
        if len(entry) > 3:
            ranks = []
            for q in range(0, len(entry)):
                handle = sql.connect("RecommendDATA.db")
                cursor = handle.cursor()
                cursor.execute("SELECT RANK FROM RANKINGS WHERE UNINAME LIKE ? AND  RANK != ?;", (entry[q], ""))
                ranking = cursor.fetchall()
                handle.commit()
                handle.close()
                ranking = str(ranking)
                ranking = ranking[8:len(ranking)-4]
                ranks.append(ranking)
            new = []
            if arts_var == "Yes":
                for c in range(0, len(ranks)):
                    if ranks[c][0] == "A":
                        new.append(ranks[c])
            elif arts_var == "No":
                for c in range(0, len(ranks)):
                    if ranks[c][0] == "L":
                        ranks[c] = re.sub("[^0-9]", "", ranks[c])
                        new.append(ranks[c])
            allofranks = []
            for c in range(0, len(ranks)):
                if ranks[c][0] == "L":
                    ranks[c] = re.sub("[^0-9]", "", ranks[c])
                allofranks.append(ranks[c])
            temp = allofranks
            old = new
            highest = 0
            for t in range(0, len(old)):
                val = len(old[t])
                if val < highest:
                    highest = val
            for n in range(0, len(old)-1):
                try:
                    old[n] = str(old[n])
                    #old[n] = str(old[n])[-2:]
                    if len(old[n]) != highest:
                        old.remove(old[n])
                except:
                    cont = True
            new = old
            new = complex.sort(new).nums()
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
                for p in range(0, len(temp)):
                    if newv2[r] == temp[p]:
                        final.append(entry[p])
            for r in range(0, len(final)):
                uniname = final[r]
                uni.display_uni(uniname)
            
    def overallranking(self):
        url= "https://www.thecompleteuniversityguide.co.uk/league-tables/rankings"
        try:
            from bs4 import BeautifulSoup
            import requests
        except:
            cont = True
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        soup.prettify()
        name = soup.find_all("td", class_="league-table-institution-name")
        for t in range(0, len(name)):
            name[t] = str(name[t])
            name[t] = name[t].split('title="')
            name[t] = name[t][1][2:len(name[t][1])-10]
        tabres = ttk.Frame(tabcontrol)
        tabcontrol.add(tabres, text="Rankings For Universities")
        tabcontrol.select(tabres)
        tk.Label(tabres, text="Overall Rankings").grid(row=1)
        count = 1
        if len(name) > 40:
            while len(name)> 40:
                name.remove(name[len(name)-1])
        for v in range(0, len(name)):
            count = str(count)
            string = count+". "+name[v]
            count = int(count)
            tk.Label(tabres, text=string).grid(row=count+1)
            count = count+1
        HoverButton(tabres, activebackground='black', fg="white", bg="red", text="Menu", command = lambda: [both.closetab(tabres), uni.unimenu()]).grid(row=count+2, column=1)

    def searchbyuni(self, entrybox, tab0):
        entrybox = entrybox.get()
        both.closetab(tab0)
        f = open("NamesOfUnis.txt")
        subjects = []
        try:
            for j in range(0,140):
                subjects.append(f.readline())
        except:
            cont= True
        for i in range(0, len(subjects)-1):
            subjects[i] = subjects[i][:len(subjects[i])-1]
        all_names = subjects
        uni.searchresults_uni(entrybox, all_names)
        
    def searchresults_uni(self, entrybox, all_names):
        entrybox = entrybox.upper()
        repeatlist = []
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
        unis =[]
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
                unis.append(all_names[l])
        if len(unis) > 3:
            while len(unis) > 3:
                unis.remove(unis[len(unis)-1])
        for r in range(0, len(uni)):
            uniname = unis[r]
            uni.display_uni(uniname)
            
    def display_uni(self, uniname):
        name = uniname
        uniname = uniname.lower()
        uniname = uniname.split(",")
        uniname = uniname[0]
        uniname = uniname.replace(" ", "-")
        url = "https://www.thecompleteuniversityguide.co.uk/"
        url = url+uniname
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT RANK FROM RANKINGS WHERE UNINAME LIKE ? AND  RANK != ?;", (name, ""))
        ranks = cursor.fetchall()
        cursor.execute("SELECT UCAS FROM UNIENTRY WHERE UNINAME LIKE ? AND  UCAS != ?;", (name, ""))
        points = cursor.fetchall()
        handle.commit()
        handle.close()
        points = str(points)
        points = points[2:len(points)-3]
        pointint = points
        points = "Average UCAS Entry Requirements: "+points
        ranks = str(ranks)
        ranks = ranks[3:len(ranks)-4]
        unitab = ttk.Frame(tabcontrol)
        tabcontrol.add(unitab, text=name)
        tabcontrol.select(unitab)
        tk.Label(unitab, fg="red", text=name, font="Ariel 17 italic").grid(row=2, columnspan=3)
        tk.Label(unitab, fg="black", text=points, font="Ariel 12 italic").grid(row=4, column=1)
        tk.Label(unitab, fg="black", text=ranks, font="Ariel 10 italic").grid(row=3, column=1)
        HoverButton(unitab, activebackground='red', fg="white", bg="black", text="Similar Universities", command = lambda: uni.similar_uni(name, pointint, unitab)).grid(row=5, column=1)
        HoverButton(unitab, activebackground='black', fg="white", bg="red", text="Menu", command = lambda: uni.unimenu()).grid(row=8, column=1)
        HoverButton(unitab, activebackground='black', fg="white", bg="red", text="Close Tab", command = lambda: [both.closetab(unitab)]).grid(row=9, column=1)

    def similar_uni(self, name, pointint, unitab):
        tab39 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab39, text="Similar Universities")
        tabcontrol.select(tab39)
        pointint = int(pointint)
        point = pointint-21
        similar = []
        for b in range(0, 20):
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
                    names = names[0]
                names = str(names)
                names = names[2:len(names)-3]
                if names[0] == "'":
                    names = names[1:len(names)-1]
                similar.append(names)
        if similar == []:
            tk.Label(tab39, text="No Similar Universities.").grid(row=5, column=1)
        else:
            variable = StringVar()
            variable.set(similar[random.randint(0, len(similar)-1)])
            OptionMenu(tab39, variable, *similar).grid(row=5, column=1)
            HoverButton(tab39, activebackground='black', fg="white", bg="red", text="ENTER", command = lambda: uni.continue_similar_uni(variable, name, tab39)).grid(row=6, column=1)
        HoverButton(tab39, activebackground='black', fg="white", bg="red", text="Back", command = lambda: both.closetab(tab39)).grid(row=8, column=1)

    def continue_similar_uni(self, variable, name, tab39):
        tab39.destroy()
        variable = variable.get()
        uni.display_uni(variable)
        
    def searchbysub(self):
        tab0 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab0, text="Select Subject")
        tabcontrol.select(tab0)
        f = open("Subjects.txt")
        subjects = []
        try:
            for j in range(0,70):
                subjects.append(f.readline())
        except:
            cont= True
        for i in range(0, len(subjects)-1):
            subjects[i] = subjects[i][:len(subjects[i])-1]
        opt = StringVar()
        opt.set(subjects[random.randint(0, len(subjects)-1)])
        OptionMenu(tab0, opt, *subjects).grid(row=1, column=1)
        HoverButton(tab0, activebackground="Black", fg="White", bg="Red", text="Enter", command = lambda: [uni.displaysubjectsearch(opt), both.closetab(tab0)]).grid(row=2, column=1)
        HoverButton(tab0, activebackground='black', fg="white", bg="red", text="Menu", command = lambda: [both.closetab(tab0), uni.unimenu()]).grid(row=4)

    def displaysubjectsearch(self, opt):
        opt = opt.get()
        subjectname = opt
        opt= str(opt)
        opt = opt.replace(" ", "+")
        opt = opt.replace("&", "%26")
        url= "https://www.thecompleteuniversityguide.co.uk/league-tables/rankings?s="
        url = url+opt
        try:
            from bs4 import BeautifulSoup
            import requests
        except:
            cont = True
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        soup.prettify()
        name = soup.find_all("td", class_="league-table-institution-name")
        for t in range(0, len(name)):
            name[t] = str(name[t])
            name[t] = name[t].split('title="')
            name[t] = name[t][1][2:len(name[t][1])-10]
        tabres = ttk.Frame(tabcontrol)
        tabcontrol.add(tabres, text="Rankings For Subject")
        tabcontrol.select(tabres)
        tk.Label(tabres, text=subjectname).grid(row=1)
        count = 1
        if len(name) > 25:
            while len(name)> 25:
                name.remove(name[len(name)-1])
        for v in range(0, len(name)):
            count = str(count)
            string = count+". "+name[v]
            count = int(count)
            tk.Label(tabres, text=string).grid(row=count+1)
            count = count+1
        HoverButton(tabres, activebackground='black', fg="white", bg="red", text="Menu", command = lambda: [both.closetab(tabres), uni.unimenu()]).grid(row=count+2, column=1)
    
    def getucaspoints(self):
        f = open("NamesOfUnis.txt")
        names = []
        try:
            for j in range(0,140):
                names.append(f.readline())
        except:
            cont= True
        for i in range(0, len(names)-1):
            names[i] = names[i][:len(names[i])-1]
            uniname = names[i]
            uniname = uniname.lower()
            uniname = uniname.split(",")
            uniname = uniname[0]
            uniname = uniname.replace(" ", "-")
            url = "https://www.thecompleteuniversityguide.co.uk/$/performance"
            url = url.replace("$", uniname)
            try:
                from bs4 import BeautifulSoup
                import requests
            except:
                cont = True
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            soup.prettify()
            try:
                ranks = soup.find("div", class_="institution-header-league-table").text
                ranks = ranks.strip()
            except:
                ranks = ""
            try:
                entrypoint = soup.find("span", class_="league-table-score-value")
            except:
                entrypoint= ""
            entrypoint = str(entrypoint)
            entrypoint = re.sub("[^0-9]", "", entrypoint)
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

class job:   
    def mainmenu(self):
        uniorjob = False
        tab1 = ttk.Frame(tabcontrol)
        tabcontrol.add(tab1, text="Jobs")
        tabcontrol.select(tab1)
        attempts = 0
        tk.Label(tab1, text="Job Research Tool", font= "Ariel 18", fg="blue").grid(row=2+1, columnspan=3)
        tk.Label(tab1, text=" ").grid(row=3+1)
        HoverButton(tab1, activebackground='blue', fg="white", bg="black", text = "POPULAR JOBS", command = lambda: job.popular(tab1)).grid(row=4+1)
        HoverButton(tab1, activebackground='blue', fg="white", bg="black", text = "HIGHLY RATED", command = lambda: job.rating(tab1)).grid(row=4+1, column=1)
        HoverButton(tab1, activebackground='blue', fg="white", bg="black", text = "SEARCH FIELDS", command = lambda: job.fieldstart(tab1)).grid(row=4+1, column=2)
        tk.Label(tab1, text=" ").grid(row=5+1)
        tk.Label(tab1, text="SEARCH JOBS:", font="Ariel 15 bold italic", fg="black").grid(row=6+1, columnspan=3)
        searchjobentry = tk.Entry(tab1)
        searchjobentry.insert(END, "Job Title")
        searchjobentry.grid(row=7+1, column=1)
        HoverButton(tab1, activebackground='blue', fg="white", bg="black", text="ENTER", command= lambda: job.search(searchjobentry, tab1)).grid(row=8+1, column=1)
        tk.Label(tab1, text=" ").grid(row=9+1)
        tk.Label(tab1, text="LOGIN:", font="Ariel 15 bold italic", fg="blue").grid(row=10+1, columnspan=3)
        IDENTentry = tk.Entry(tab1)
        IDENTentry.insert(END, "ID")
        IDENTentry.grid(row=11+1, column=1)
        Passwordentry = tk.Entry(tab1)
        Passwordentry.insert(END, "Password")
        Passwordentry.grid(row=12+1, column=1)
        #resetpin = tk.Button(tab1, text="FORGOT PIN", command = lambda: reset()).grid(row=7, column=3)
        HoverButton(tab1, activebackground='black', fg="white", bg="blue", text="ENTER", command= lambda: both.login(attempts, tab1, IDENTentry, Passwordentry, uniorjob)).grid(row=13+1, column=1)
        tk.Label(tab1, text=" ").grid(row=14+1)
        tk.Label(tab1, text="NEW USER:", font="Ariel 15 bold italic", fg="blue").grid(row=15+1, columnspan=3)
        IDentry = tk.Entry(tab1)
        IDentry.insert(END, "ID")
        IDentry.grid(row=19+1, column=1)
        HoverButton(tab1, activebackground='black', fg="white", bg="blue", text="ENTER", command = lambda: both.user1(IDentry, tab1, uniorjob)).grid(row=20+1, column=1)
        tk.Label(tab1, text=" ").grid(row=21+1)
        HoverButton(tab1, activebackground='black', fg="white", bg="red", text="Home", command = lambda: [both.closetab(tab1), both.home()]).grid(row=22+1, column=1)
    
    def fieldq(self, ID_insert, tab4):
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
        tk.Label(tab3, text=" ").grid(row=1, column=1)
        job.recurfield(ID_insert, tab3, fields, countofiterations, recordchoices, var1)

    def recurfield(self, ID_insert, tab3, fields, countofiterations, recordchoices, var1):
        if countofiterations == 0:
            tk.Label(tab3, text="Choose a proirity of each field so recommendation can be more appropriate.").grid(row=1)
        else:
            var1=var1.get()
            recordchoices.append(var1)
        if countofiterations == len(fields):
            job.updatefields(ID_insert, recordchoices, fields, tab3)
        try:
            label = tk.Label(tab3, text=fields[countofiterations])
            label.grid(row=2)
            tk.Label(tab3, text=str(countofiterations)+"/"+str(len(fields)-1)).grid(row=2, column=1)
            countofiterations=countofiterations+1
            var1 = IntVar()
            tk.Radiobutton(tab3, text="Very Interested", value=5, variable=var1).grid(row=3)
            tk.Radiobutton(tab3, text="Interested", value=4, variable=var1).grid(row=4)
            tk.Radiobutton(tab3, text="Neutral", value=3, variable=var1).grid(row=5)
            tk.Radiobutton(tab3, text="Not Interested", value=2, variable=var1).grid(row=6)
            tk.Radiobutton(tab3, text="Avoid", value=1, variable=var1).grid(row=7)
            HoverButton(tab3, activebackground='blue', fg="white", bg="black", text="NEXT FIELD", command= lambda: [job.recurfield(ID_insert, tab3, fields, countofiterations, recordchoices, var1), both.closetab(label)]).grid(row=8)
            HoverButton(tab3, activebackground='blue', fg="white", bg="black", text="SKIP ALL", command= lambda: job.Increasefield(ID_insert, tab3, fields, countofiterations, recordchoices, var1)).grid(row=8, column=2)
        except:
            hold = 0

    def Increasefield(self, ID_insert, tab3, fields, countofiterations, recordchoices, var1):
        while countofiterations < 16:
            countofiterations=countofiterations+1
        job.recurfield(ID_insert, tab3, fields, countofiterations, recordchoices, var1)

    def updatefields(self, ID_insert, recordchoices, fields, tab3):
        recordchoices.reverse()
        tab3.destroy()
        recordchoices.pop()
        recordchoices.reverse()
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("UPDATE USERS SET FIELDS = ? WHERE USERID = ?;", (str(recordchoices), ID_insert))
        handle.commit()
        handle.close()
        job.usedata(recordchoices, fields, ID_insert)# the array is 5 - very interested to 1 - avoid per field

    def usedata(self, recordchoices, fields, ID_insert): #decide job by field, quallevel, work experience, if this is identical compare skills of the users that were recommended this to the current user. Then choose by the ratings of recommendations and count of recommendations.
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
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            cursor.execute("SELECT JOBNAME FROM JOBS WHERE FIELD = ?;", (finalfields[e],))
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
                    if i not in punctuation:
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
            nameofqual = job.findcommonqual(qualforjob)
            handle = sql.connect("RecommendDATA.db")
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
            job.workxp(joblist, ID_insert)
        else:
            if joblist == []:
                job.workxp(fin, ID_insert)
            else:
                handle = sql.connect("RecommendDATA.db")
                cursor = handle.cursor()
                cursor.execute("SELECT JOBID FROM JOBS WHERE JOBNAME LIKE ? AND IDLE = ?", ("%"+joblist[0]+"%", 0))
                jobid = cursor.fetchall()
                jobid = str(jobid)
                jobid = jobid[2:len(jobid)-3]
                jobid = int(jobid)
                handle.commit()
                cursor.execute("INSERT INTO RECOMMEND VALUES(?,?)", (jobid, ID_insert))
                handle.commit()
                handle.close()
                job.display(joblist[0])

    def findcommonqual(self, qualforjob):
        qualforjob = str(qualforjob)
        qualforjob = qualforjob.split("'")
        del qualforjob[::2]
        quals = []
        for h in range(0, len(qualforjob)):
            punctuation = """!"#$%&'()*+/:;=?@[\\]^_`{|}~"""
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
        
    def workxp(self, joblist, ID_insert):
        if len(joblist) <= 10:
            worktab = ttk.Frame(tabcontrol)
            tabcontrol.add(worktab, text="WORK EXPERIENCE")
            tabcontrol.select(worktab)
            tk.Label(worktab, text=" ").grid(row=1)
            tk.Label(worktab, text="Do you have any work experience in the following roles?").grid(row=2) 
            optionsforwork = ["3+ years", "1-3 years", "< 1 year"]
            varnames = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
            namesofvariables = ["S"]*250
            for c in range(0, len(joblist)):
                handle = sql.connect("RecommendDATA.db")
                cursor = handle.cursor()
                cursor.execute("SELECT WORKEXP FROM JOBS WHERE JOBNAME LIKE ? AND IDLE = ?", ("%"+joblist[c]+"%", 0))
                workexp = cursor.fetchall()
                handle.commit()
                exp=""
                handle.close()
                punctuation = """!"#$%&'()*+/:;=?@[\\]^_`{|}~"""
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
                jobgiven = joblist[c] + " - Requires " + exp + " experience in similar positions."
                varnames[c] = StringVar()
                varnames[c].set(optionsforwork[2])
                tk.Label(worktab, text=jobgiven).grid(row=c+3)
                tk.Label(worktab, text="Your Level: ").grid(row=c+3, column=1)
                OptionMenu(worktab , varnames[c], *optionsforwork).grid(row=c+3, column=2)
            tk.Label(worktab, text="Work Experience * Includes Training that is job specific : The experience that a person already has of working, a period of time in which a student temporarily works for an employer to get experience.").grid(row=293)
            HoverButton(worktab, activebackground='blue', fg="white", bg="black", text="Confirm", command= lambda: job.usingworkexp(varnames, joblist, worktab, ID_insert)).grid(row=294)
        else:
            joblist.remove(joblist[random.randint(0, len(joblist)-1)])
            job.workxp(joblist, ID_insert)
            
    def usingworkexp(self, varnames, joblist, worktab, ID_insert):
        worktab.destroy()
        VAR = []
        final_list = []
        for r in range(0, len(joblist)):
            VAR.append(varnames[r].get())
        for p in range(0, len(joblist)):
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            cursor.execute("SELECT WORKEXP FROM JOBS WHERE JOBNAME LIKE ? AND IDLE = ?", ("%"+joblist[p]+"%", 0))
            workexp = cursor.fetchall()
            handle.commit()
            exp=""
            handle.close()
            punctuation = """!"#$%&'()*+/:;=?@[\\]^_`{|}~"""
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
                handle = sql.connect("RecommendDATA.db")
                cursor = handle.cursor()
                cursor.execute("SELECT EMPLOYEES FROM JOBS WHERE JOBNAME LIKE ? AND JOBID > ?", ("%"+final_list[r]+"%", "0"))
                employ = cursor.fetchall()
                handle.commit()
                handle.close()
                punctuation = """!"#$%&'()*+/, :;=?@[\\]^_`{|}~"""
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
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            cursor.execute("SELECT JOBID FROM JOBS WHERE JOBNAME LIKE ? AND IDLE = ?", ("%"+job_name+"%", 0))
            jobid = cursor.fetchall()
            if len(jobid) > 1:
                jobid = jobid[0]
            jobid = str(jobid)
            jobid = jobid[2:len(jobid)-3]
            jobid = int(jobid)
            handle.commit()
            cursor.execute("INSERT INTO RECOMMEND VALUES(?,?)", (jobid, ID_insert))
            handle.commit()
            handle.close()
            job.display(job_name)

    def display(self, job_name):
        result_tab = ttk.Frame(tabcontrol)
        tabcontrol.add(result_tab, text=job_name)
        tabcontrol.select(result_tab)
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("SELECT EMPLOYEES FROM JOBS WHERE JOBNAME LIKE ? AND JOBID > ?", ("%"+job_name+"%", "0"))
        employees = cursor.fetchall()
        handle.commit()
        cursor.execute("SELECT JOBID FROM JOBS WHERE JOBNAME LIKE ? AND IDLE = ?", ("%"+job_name+"%", 0))
        jobid = cursor.fetchall()
        if len(jobid) > 1:
            jobid = jobid[0]
        jobid = str(jobid)
        jobid = jobid[2:len(jobid)-3]
        handle.commit()
        try:
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
            top_skill = HoverButton(result_tab, activebackground='Light Blue', fg="Black", bg="White", text="Similar User Traits", command= lambda: job.sim_users(job_name)).grid(row=22, column=1)
        except:
            cont = True
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
        tk.Label(result_tab, text=rec_count, font= "Ariel 12 italic").grid(row=20, column=1)
        cursor.execute("UPDATE JOBS SET COUNT = ? WHERE JOBNAME LIKE ? AND JOBID > ?", (count, "%"+job_name+"%", "0"))
        handle.commit()
        employees = str(employees)
        employees = re.sub("[^0-9]", "", employees)
        employees = employees[2:]
        if employees[:2] == "72":
            employees = employees[2:]
        if employees == "":
            employees = "uncounted quantity of"
        tk.Label(result_tab, text=job_name, font= "Ariel 30", fg="blue").grid(row=2, columnspan=3)
        tk.Label(result_tab, text="Job:", font= "Ariel 20", fg="Dark Blue").grid(row=4)
        tk.Label(result_tab, text="Field:", font= "Ariel 20", fg="Dark Blue").grid(row=11)
        tk.Label(result_tab, text="Extras:", font= "Ariel 20", fg="Dark Blue").grid(row=15)
        breaktext = len(job_name)*"-"
        tk.Label(result_tab, text=breaktext, font= "Ariel 30", fg="Light Blue").grid(row=3, columnspan=3)
        tk.Label(result_tab, text=breaktext, font= "Ariel 30", fg="Light Blue").grid(row=1, columnspan=3)
        employees = str(employees)
        employees = employees+" people employed in this role."
        tk.Label(result_tab, text=employees, font= "Ariel 12 italic").grid(row=10, column=1)
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
        HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text=salary, command = lambda: job.currency(number_hold, result_tab, job_name, salary)).grid(row=6, column=1)
        HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text="DESCRIPTION", command = lambda: [job.displaydescript(descript, job_name), both.closetab(result_tab)]).grid(row=7, column=1)
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
            HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text="SKILLS", command = lambda: job.displayskills(skills, var, job_name, result_tab)).grid(row=8, column=1)
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
        tk.Label(result_tab, text=field, font= "Ariel 12 italic").grid(row=12, column=1)
        HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text="Field Info", command = lambda: job.field_info(result_tab, field, job_name)).grid(row=13, column=1)
        tk.Label(result_tab, text=" ", font= "Ariel 12 italic").grid(row=14, column=1)
        HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text="SEARCH FOR LISTINGS", command = lambda: job.listingsearch(result_tab, job_name)).grid(row=16, column=1)
        HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text="Qual Split", command = lambda: job.qual_split(job_name)).grid(row=17, column=1)
        HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text="Create recommendation file (PDF)", command = lambda: job.RECtemplate(job_name, result_tab, field, descript, skills, salary)).grid(row=18, column=1)
        HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text="SIMILAR JOBS", command = lambda: job.similar_jobs(field, job_name, result_tab)).grid(row=19, column=1)
        HoverButton(result_tab, activebackground='light blue', fg="Black", bg="White", text="Rate this job", command = lambda: job.ratingadd(job_name, result_tab)).grid(row=21, column=1)
        HoverButton(result_tab, activebackground='Blue', fg="Blue", bg="White", text="MAIN MENU", command = lambda: job.mainmenu()).grid(row=25)
        HoverButton(result_tab, activebackground='Blue', fg="Blue", bg="White", text="CLOSE TAB", command = lambda: both.closetab(result_tab)).grid(row=27)

    def sim_users(self, job_name):
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
        HoverButton(similarusers, activebackground='blue', fg="white", bg="black", text="Skill Split", command = lambda: job.skillsplit(all_non_duplicated_skills, nums)).grid(row=3)
        tk.Label(similarusers, text =job_name).grid(row=1)
        tk.Label(similarusers, text ="Top Skill: ").grid(row=2)
        tk.Label(similarusers, text =topskill).grid(row=2, column=1)
        HoverButton(similarusers, activebackground='blue', fg="white", bg="black", text ="Back", command = lambda: both.closetab(similarusers)).grid(row=15)

    def skillsplit(self, all_non_duplicated_skills, nums):
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
        
    def displaydescript(self, descript, job_name):
        result_tab = ttk.Frame(tabcontrol)
        tabcontrol.add(result_tab, text="JOB DESCRIPTION")
        tabcontrol.select(result_tab)
        tk.Label(result_tab, text ="Description: ").grid(row=1)
        tk.Label(result_tab, text =descript).grid(row=2)
        HoverButton(result_tab, activebackground='blue', fg="white", bg="black", text="Back", command = lambda: [both.closetab(result_tab), job.display(job_name)]).grid(row=20, column=1)
        
    def RECtemplate(self, job_name, result_tab, field, descript, skills, salary):
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
        
    def similar_jobs(self, field, job_name, result_tab):
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
        HoverButton(similar_tab, activebackground='blue', fg="white", bg="black", text="Continue", command = lambda: [job.var3confirm(var3), both.closetab(similar_tab)]).grid(row=3)
        HoverButton(similar_tab, activebackground='blue', fg="white", bg="black", text="Back", command = lambda: [job.display(job_name), both.closetab(similar_tab)]).grid(row=4)

    def var3confirm(self, var3):
        job_name = var3.get()
        job.display(job_name)
        
    def ratingadd(self, job_name, result_tab):
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
        if ratings == "":
            average = "N/A"
        else:
            total = total + int(ratings)
            average = total / len(ratings)
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
        HoverButton(result_tab, activebackground='blue', fg="white", bg="black", text="Enter", command = lambda: ratingadd2(job_name, comment, stars, result_tab)).grid(row=5, column=5)

    def ratingadd2(self, job_name, comment, stars, result_tab):
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
        job.display(job_name)
        
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
        
    def field_info(self, result_tab, field, job_name):
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
        HoverButton(fieldinfo_tab, activebackground='blue', fg="white", bg="black", text="Back", command = lambda: [both.closetab(fieldinfo_tab), job.display(job_name)]).grid(row=4, column=1)
        
    def currency(self, number_hold, result_tab, job_name, salary):
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
        HoverButton(currency_tab, activebackground='blue', fg="white", bg="black", text="Confirm", command = lambda: job.use_currency(urlof_live, currency_tab, job_name, number_hold, vars_)).grid(row=4)
        HoverButton(currency_tab, activebackground='blue', fg="white", bg="black", text="Back", command = lambda: [both.closetab(currency_tab), job.display(job_name)]).grid(row=4, column=1)

    def use_currency(self, urlof_live, currency_tab, job_name, number_hold, vars_):
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
        tk.Label(currency_tab2, text = sal).grid(row=1)
        HoverButton(currency_tab2, activebackground='blue', fg="white", bg="black", text="Back", command = lambda: [both.closetab(currency_tab2), job.display(job_name)]).grid(row=2)
        
    def listingsearch(self, result_tab, job_name):
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
        job.listings_(job_name, name, url, rep)
        
    def copytoclip(self, url):
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(url)
        r.update()
        r.destroy()
        
    def listings_(self, job_name, name, url, rep):
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
        job.listingmenu(url, hold, VAR)

    def listingmenu(self, url, hold, VAR):
        try:
            from bs4 import BeautifulSoup
            import requests
        except:
            cont = True
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        soup.prettify()
        no_result_test = soup.findAll("div", {"class": "bad_query"})
        if no_result_test != []:
            skill_tab = ttk.Frame(tabcontrol)
            tabcontrol.add(skill_tab, text="No Results")
            tabcontrol.select(skill_tab)
            HoverButton(skill_tab, activebackground='blue', fg="white", bg="black", text="Back", command = lambda: [both.closetab(skill_tab), job.display(hold)]).grid(row=2)
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
            for x in range(0, len(jobnames)):
                jobnames[x] = jobnames[x] + " --- " + all_location[x]
                allnames.append(jobnames[x])
                tk.Label(jobresults, text=jobnames[x]).grid(row=count+1)
                count = count+2
            VAR = StringVar()
            VAR.set(allnames[random.randint(0, len(allnames)-1)])
            tk.Label(jobresults, text = "Select position interest: ").grid(row=1)
            HoverButton(jobresults, activebackground='blue', fg="white", bg="black", text="Continue", command = lambda: [job.joblisting_indeed(hold, hrefs, jobnames, VAR), both.closetab(jobresults)]).grid(row=2, column=1)
            tk.OptionMenu(jobresults, VAR, *allnames).grid(row=1, column=1)
            HoverButton(jobresults, activebackground='blue', fg="white", bg="black", text="BACK", command = lambda: [job.display(hold), both.closetab(jobresults)]).grid(row=count+10)

    def joblisting_indeed(self, hold, hrefs, jobnames, VAR):
        listname = VAR.get()
        for g in range(0, len(jobnames)):
            if listname == jobnames[g]:
                href = hrefs[g]
        list_tab = ttk.Frame(tabcontrol)
        tabcontrol.add(list_tab, text="Listing")
        tabcontrol.select(list_tab)
        tk.Label(list_tab, text = listname, font= "Ariel 15 italic", fg="Blue").grid(row=1, columnspan=3)
        HoverButton(list_tab, activebackground='blue', fg="white", bg="black", text="Copy URL to Clipboard", command = lambda: job.copytoclip(href)).grid(row=2, column=1)
        HoverButton(list_tab, activebackground='blue', fg="white", bg="black", text="Open URL", command = lambda: job.openurl(href)).grid(row=3, column=1)
        HoverButton(list_tab, activebackground='blue', fg="white", bg="black", text="Back", command = lambda: [job.display(hold), both.closetab(list_tab)]).grid(row=4, column=1)

    def openurl(self, href):
        try:
            import webbrowser
        except:
            cont = True
        webbrowser.open(href)
        
    def displayskills(self, skills, var, job_name, result_tab):
        result_tab.destroy()
        skill_tab = ttk.Frame(tabcontrol)
        tabcontrol.add(skill_tab, text="JOB SKILLS")
        tabcontrol.select(skill_tab)
        tag = job_name + " skills:"
        tk.Label(skill_tab, text=tag).grid(row=1)
        tk.Label(skill_tab, text=" ").grid(row=2)
        for n in range(0, len(skills)-1):
                tk.Label(skill_tab, text=skills[n]).grid(row=n+3)
        HoverButton(skill_tab, activebackground='blue', fg="white", bg="black", text="BACK", command = lambda: [job.display(job_name), both.closetab(skill_tab)]).grid(row=20)
                                                                                        
    def search(self, searchjobentry, tab1):
        #search in database word by word of each job and use LIKE and % to widen critera. If no results, option to add a job to be reviewed.
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
            job.missingjob1(tab1)
        else:
            tab1.destroy()
            job.searchmenu(results)

    def searchmenu(self, results):
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
            job.missingjob1(tab1)
        if a == True:
            job.display(job_name)

    def deletealltabs(self, variables, new):
        for u in range(0, len(new)):
            variables[u].destroy()
        
    def missingjob1(self, tab1):
        tab1.destroy()
        #give options 
        missing = ttk.Frame(tabcontrol)
        tabcontrol.add(missing, text="ADD JOB")
        tabcontrol.select(missing)
        tk.Label(missing, text="THERE WAS NO FOUND JOBS, add a job to be reviewed by an Admin.").grid(row=1, column=1)
        tk.Label(missing, text="JOBNAME:").grid(row=2)
        JOB__name = tk.Entry(missing)
        JOB__name.grid(row=2, column=1)
        tk.Label(missing, text="DESCRIPTION:").grid(row=3)
        JOB__des = tk.Entry(missing)
        JOB__des.grid(row=3, column=1)
        tk.Label(missing, text="FIELD:").grid(row=4)
        JOB__field = tk.Entry(missing)
        JOB__field.grid(row=4, column=1)
        HoverButton(missing, activebackground='blue', fg="white", bg="black", text="Back", command = lambda: [both.closetab(missing), job.mainmenu()]).grid(row=5)
        HoverButton(missing, activebackground='blue', fg="white", bg="black", text="Confirm", command = lambda: job.missingjob2(JOB__name, missing, JOB__des, JOB_field)).grid(row=5, column=1)
        
    def missingjob2(self, JOB__name, missing, JOB__des,  JOB_field):
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
        job.mainmenu()
        
    def popular(self, tab1):
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
        tk.Label(new_tab, text= "POPULAR JOBS:").grid(row=1)
        VAR = StringVar()
        VAR.set(names[random.randint(0, len(names)-1)])
        tk.OptionMenu(new_tab, VAR, *names).grid(row=1, column=1)
        HoverButton(new_tab, activebackground='blue', fg="white", bg="black", text="Confirm", command = lambda: [job.popular2(VAR), both.closetab(new_tab)]).grid(row=2)
        HoverButton(new_tab, activebackground='blue', fg="white", bg="black", text="Back", command = lambda: [both.closetab(new_tab), job.mainmenu()]).grid(row=3)
        
    def popular2(self, VAR):
        job_name = VAR.get()
        job.display(job_name)
        
    def fieldstart(self, tab1):
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
        tk.Label(fieldsearch, text= "Choose a Field").grid(row=1)
        variance = StringVar()
        variance.set(fields[random.randint(0, len(fields)-1)])
        tk.OptionMenu(fieldsearch, variance, *fields).grid(row=2)
        HoverButton(fieldsearch, activebackground='blue', fg="white", bg="black", text="Confirm", command = lambda: job.field_data(variance, fieldsearch)).grid(row=3)
        HoverButton(fieldsearch, activebackground='blue', fg="white", bg="black", text="Back", command = lambda: [both.closetab(fieldsearch), job.mainmenu()]).grid(row=4)

    def field_data(self, variance, fieldsearch):
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
        tk.OptionMenu(results_field, var_job, *new).grid(row=1)
        HoverButton(results_field, activebackground='blue', fg="white", bg="black", text="Confirm", command = lambda: job.getresultoffield_search(var_job, results_field)).grid(row=2)
        tab1 = ttk.Frame(tabcontrol)
        HoverButton(results_field, activebackground='blue', fg="white", bg="black", text="Back", command= lambda: [job.fieldstart(tab1), job.delete_fieldresults(tab1, results_field)]).grid(row=3)

    def delete_fieldresults(self, tab1, results_field):
        tab1.destroy()
        results_field.destroy()
        
    def getresultoffield_search(self, var_job, results_field):
        var_job = var_job.get()
        results_field.destroy()
        job_name = var_job
        if job_name[0] == " ":
            job_name = job_name[1:]
        job.display(job_name)

    def rating(self, tab1):
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
        if len(sort_averages) > 8:
            number = 8
        elif len(sort_averages) > 3:
            number = 3
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
        HoverButton(results_field, activebackground='blue', fg="white", bg="black", text="Continue", command= lambda: [both.closetab(results_field), job.popular2(var)]).grid(row=3, column=1)
        HoverButton(results_field, activebackground='blue', fg="white", bg="black", text="Back", command= lambda: [both.closetab(results_field), job.mainmenu()]).grid(row=3)

#
#
#
#

class complex: # replacing all possible in-built functions with calculations

    class ording:
        def __init__(self, value):
            self.__value = value
        
        def findord(self):
            return ord(self.__value)

    class append:
        def __init__(self, array, value):
            self.__array = array # private access modifiers
            self.__value = value

        def concat(self):
            self.__array = self.__array + [self.__value]
            return self.__array

        def insert(self, pos):
            self.__postition = pos
            self.__array = self.__array[:pos] + [self.__value] + self.__array[pos:]
            return self.__array

    class randomint:
        def __init__(self, min, max):
            self.__min = min
            self.__max = max
            self.__allvalues = []

        def calculate(self):
            for x in range(self.__min, self.__max):
                self.__allvalues = complex.append(self.__allvalues, x).concat()
            return self.__allvalues[random.randint(self.__min, self.__max)]

    class sort:
        def __init__(self, array):
            self.__array = array
            self.__sort1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            self.__sort2 = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
            self.__static = []
            self.__stat = [" "]*len(array)
            self.__test = False

        def nums(self):
            while self.__test == False:
                self.__repeat = 0
                for y in range(0, len(self.__array)):
                    for x in range(0, len(self.__array)):
                        try:
                            self.__num = self.__array[x]
                            self.__num = int(self.__num)
                            self.__num2 = self.__array[x+1]
                            self.__num2 = int(self.__num2)
                            if self.__num >= self.__num2:
                                self.__array[x] = self.__num2
                                self.__array[x+1] = self.__num
                                self.__test = False
                            else:
                                self.__repeat = self.__repeat+1
                        except:
                            self.__test = False
                self.__len = len(self.__array)/2
                self.__len = int(self.__len)+1
                if self.__repeat >= self.__len:
                    self.__test = True
            return self.__array

        def alpha(self):
            for i in range(0, len(self.__array)):
                self.__allnum = 0
                for letter in self.__array[i]:
                    self.__num = complex.ording(letter).findord()
                    self.__allnum = self.__allnum + self.__num
                self.__static = complex.append(self.__static, self.__allnum).concat()
            print(self.__static)
            self.__static = complex.sort(self.__static).nums()
            print(self.__static)
            for i in range(0, len(self.__array)):
                self.__allnum = 0
                for letter in self.__array[i]:
                    self.__num = complex.ording(letter).findord()
                    self.__allnum = self.__allnum + self.__num
                for h in range(0, len(self.__static)):
                    if self.__static[h] == self.__allnum:
                        self.__stat = complex.append(self.__stat, self.__array[i]).insert(h)
            return self.__stat

    class up_down:
        def __init__(self, char):
            self.__char = char
            self.__alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
            self.__z = True

        def down(self):
            for v in range(0, len(self.__alpha)):
                if self.__alpha[v] == self.__char:
                    if v > 26:
                        self.__z = False
                        return self.__alpha[v-26]
            if self.__z == True:
                return self.__char

        def up(self):
            for v in range(0, len(self.__alpha)):
                if self.__alpha[v] == self.__char:
                    if v < 27:
                        self.__z = False
                        return self.__alpha[v+26]
            if self.__z == True:
                return self.__char

    class delete:
        def __init__(self, array, pos):
            self.__pos = pos
            self.__array = array
        
        def _del(self):
            self.__array = self.__array[:self.__pos] + self.__array[self.__pos+1:]
            return self.__array

    class reverse:
        def __init__(self, array):
            self.__array = array
            self.__newarray = []
            self.__len = len(array)
            self.__iter = 1

        def swap(self):
            for item in self.__array:
                self.__newarray = complex.append(self.__newarray, self.__array[self.__len - self.__iter]).concat()
                self.__iter = self.__iter + 1
            return self.__newarray

    class pop:
        def __init__(self, array):
            self.__pos = len(array)-1
            self.__array = array
            self.__temp = array
        
        def last(self):
            self.__array = complex.delete(self.__array, self.__pos)._del()
            return self.__array, self.__temp[self.__pos]

    class strip:
        def __init__(self, string):
            self.__string = str(string)
            self.__set = True

        def trailorfront(self):
            return self.__string

    class lencalc:
        def __init__(self, string):
            self.__string = string
            self.__iter = 0

        def calc(self):
            try:
                for char in self.__string:
                    self.__iter = self.__iter + 1
            except:
                self.__string = str(self.__string)
                self.__iter = complex.lencalc(self.__string).calc()
            return self.__iter

    class replace:
        def __init__(self, char, string):
            self.__string = string
            self.__char = char
            self.__newstring = ""
        
        def chars(self):
            skip = False
            for letter in self.__string:
                if letter == self.__char:
                    skip = True
                if skip == False:
                    self.__newstring = self.__newstring + letter
                skip = False
            return self.__newstring

print(complex.strip("teseet").trailorfront())
print(complex.sort(["Testing", "Test", "Best", "lest", "hi"]).alpha())

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
            handle = sql.connect("RecommendDATA.db")
            cursor = handle.cursor()
            cursor.execute("INSERT INTO JOBS VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (jobid, name, url, ".", ".", ".", ".", ".", fieldname, ".", ".", "0"))
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
    handle = sql.connect("RecommendDATA.db")
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
        handle = sql.connect("RecommendDATA.db")
        cursor = handle.cursor()
        cursor.execute("UPDATE JOBS SET SKILLS = ?, QUALLEVEL = ?, DESCRIPTION = ?, SALARY = ?, WORKEXP = ?, EMPLOYEES = ? WHERE JOBID = ?;", (str(keyskills), str(store), des, salary, stringoutput, employ, count))
        handle.commit()
        count=count+1
        iterate = iterate+1

try:   
    handle = sql.connect("RecommendDATA.db")
    cursor = handle.cursor()
    cursor.execute("CREATE TABLE RANKINGS(UNI_ID INT, UNINAME TEXT, RANK TEXT)")
    cursor.execute("CREATE TABLE UNIENTRY(UNI_ID INT, UNINAME TEXT, UCAS INT)")
    cursor.execute("CREATE TABLE JOBS(JOBID INT, JOBNAME TEXT, URL TEXT, SKILLS TEXT, QUALLEVEL TEXT, WORKEXP TEXT, SALARY INT, DESCRIPTION TEXT, FIELD TEXT, COUNT INT, EMPLOYEES INT, IDLE INT)")
    cursor.execute("CREATE TABLE USERS(USERID TEXT, NAME TEXT, PASSWORD TEXT, QUALLEVEL TEXT, SKILL1 TEXT, SKILL2 TEXT, SKILL3 TEXT, FIELDS TEXT, CURRENTJOB TEXT)")
    cursor.execute("CREATE TABLE RATINGS(JOBID INT, RATING INT, COMMENT TEXT)")
    cursor.execute("CREATE TABLE WEBLIST(WEBID INT, WEBURL TEXT)")
    cursor.execute("CREATE TABLE RECOMMEND(JOBID, USERID)")
    cursor.execute("CREATE TABLE USER_RECOMMENDATIONS(JOBNAME TEXT, DESCRIPTION TEXT, FIELD TEXT)")
    handle.commit()
    handle.close()
    uni.getucaspoints()
    fieldlist = loaddata()
    getskillslist()
except:
    cont = True

#create main menu upon staring program
window=tk.Tk()
window.title("JOB FINDER")
tabcontrol = ttk.Notebook(window)
both = both()
uni = uni()
job = job()
both.home()

tabcontrol.pack(expand=1, fill="both")
window.mainloop()
