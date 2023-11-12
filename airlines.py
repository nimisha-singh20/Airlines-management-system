import mysql.connector

import time
import random

# Global variables
depart = 0
arrive = 0
ddate = ""
adate = ""
nchoice = 0
serchoice = 0
typech = 0
cost = 0
tcost = 0
adult = {}
child = {}
seat1 = []
seat2 = []
dlist = {}
alist = {}

# Connect to the database
db = mysql.connector.connect(host='localhost', database='airlines', user='root', passwd='***********')

# Function to select departure and arrival places
def place():
    global depart
    global arrive
    global city
    city = {1: 'KOLKATA', 2: 'MUMBAI', 3: 'DELHI', 4: 'CHENNAI'}
    print('Select your place of departure:')
    for key in city:
        print(key, city[key])
    depart = int(input('Enter your choice: '))
    print('Select your place of arrival:')
    for key in city:
        print(key, city[key])
    arrive = int(input('Enter your choice: '))
    if depart == arrive:
        return 1

# Function to select departure and return dates
def date():
    global ddate
    global adate
    global nature
    global nchoice
    nature = {1: 'One way', 2: 'Returning'}
    print('Do you want to book a one-way flight or a returning flight?')
    for key in nature:
        print(key, nature[key])
    nchoice = int(input('Enter your choice: '))
    if nchoice == 1:
        ddate = input('\nEnter departure date in dd/mm/yyyy format: ')
    elif nchoice == 2:
        ddate = input('\nEnter departure date in dd/mm/yyyy format: ')
        adate = input('\nEnter return date in dd/mm/yyyy format: ')
    else:
        print('\nInvalid option, try again')
        return nchoice

# Function to input passenger details
def passenger():
    global adult
    global child
    print('NOTE: Children aged below 2 years do not require plane fees and extra seats')
    n1 = int(input('Enter no. of adults (age: 2 years and above): '))
    n2 = int(input('Enter no. of children (age: below 2 years): '))
    for i in range(n1):
        print('\nFor adult', i+1)
        name = input('Enter full name: ')
        age = int(input('Enter age (in years): '))
        phone = int(input('Enter phone no.: '))
        email = input('Enter email address: ')
        prefer = input('Does passenger have preference for window seat?(y/n): ')
        adult[i+1] = (name, age, phone, email, prefer)
    for i in range(n2):
        print('\nFor child', i+1)
        name = input('Enter full name: ')
        age = int(input('Enter age (in months): '))
        child[i+1] = (name, age)

# Function to select service class
def serviceclass():
    global serchoice
    global service
    service = {1: 'Economy class', 2: 'Business class', 3: 'First class'}
    print('Please select the type of service class you want to travel in')
    for key in service:
        print(key, service[key])
    serchoice = int(input('Enter your choice: '))

# Function to select type of flight (direct/connecting)
def typefly():
    global typech
    global typef
    typef = {1: 'Direct', 2: 'Connecting'}
    print('Select the type of flight you want:')
    for key in typef:
        print(key, typef[key])
    typech = int(input('Enter your choice: '))

# Function to list available flights
def flightlist():
    print("Finding flights", end="")
    for i in range(5):
        print(".", end="")
        time.sleep(1)
    print('\n\nLIST OF FLIGHTS\n')
    print('Based on your preferences, the following are the flights available (in the order of Flight No., Origin, Destination, Via, Company, Departure time, and Arrival time):')
    departlist()
    if adate is not None:
        returnlist()

# Function to list departure flights
def departlist():
    global dlist
    global dchoice
    dlist = {}
    mc = db.cursor()
    sd = ''
    c = 1
    if typech == 1:
        sd = 'select * from flight where origin = "'+city[depart]+'" and destination = "'+city[arrive]+'" and via is NULL'
        mc.execute(sd)
        for i in mc:
            print(i[0],"\t",i[1],"\t",i[2],"\t",i[3],"\t",i[4],"\t",i[5],"\t",i[6])
            dlist[c] = i
            c = c + 1
        dchoice = int(input('\nEnter your choice of flight: '))
    else:
        sd = 'select * from flight where origin = "'+city[depart]+'" and destination = "'+city[arrive]+'" and via is not NULL'
        mc.execute(sd)
        for i in mc:
            print(i)
            dlist[c] = i
            c = c + 1
        dchoice = int(input('\nEnter your choice of flight: '))

# Function to list return flights
def returnlist():
    global alist
    global achoice
    alist = {}
    mc = db.cursor()
    sa = ''
    c = 1
    if typech == 1:
        sa = 'select * from flight where origin = "'+city[arrive]+'" and destination = "'+city[depart]+'" and via is NULL'
        mc.execute(sa)
        for i in mc:
            print(i[0],"\t",i[1],"\t",i[2],"\t",i[3],"\t",i[4],"\t",i[5],"\t",i[6])
            alist[c] = i
            c = c + 1
        achoice = int(input('\nEnter your choice of flight: '))
    else:
        sa = 'select * from flight where origin = "'+city[arrive]+'" and destination = "'+city[depart]+'" and via is not NULL'
        mc.execute(sa)
        for i in mc:
            print(i)
            alist[c] = i
            c = c + 1
        achoice = int(input('\nEnter your choice of flight: '))

# Function to calculate flight cost
def price():
    global cost
    global tcost
    if adate is None:
        if (depart == 1 and arrive == 2) or (depart == 2 and arrive == 1):
            cost = 4500
        elif (depart == 1 and arrive == 3) or (depart == 3 and arrive == 1):
            cost = 4000
        elif (depart == 1 and arrive == 4) or (depart == 4 and arrive == 1):
            cost = 3500
        elif (depart == 2 and arrive == 3) or (depart == 3 and arrive == 2):
            cost = 3500
        elif (depart == 2 and arrive == 4) or (depart == 4 and arrive == 2):
            cost = 4000
        else:
            cost = 5000
    else:
        if (depart == 1 and arrive == 2) or (depart == 2 and arrive == 1):
            cost = 9000
        elif (depart == 1 and arrive == 3) or (depart == 3 and arrive == 1):
            cost = 8000
        elif (depart == 1 and arrive == 4) or (depart == 4 and arrive == 1):
            cost = 7000
        elif (depart == 2 and arrive == 3) or (depart == 3 and arrive == 2):
            cost = 7000
        elif (depart == 2 and arrive == 4) or (depart == 4 and arrive == 2):
            cost = 8000
        else:
            cost = 10000
    if serchoice == 1:
        tcost = cost * 105 // 100
    else:
        tcost = cost * 112 // 100
    print("\nCost of flight calculated\n\n")

# Function to select seats
def seats():
    global seat1
    global seat2
    avail1 = []
    avail2 = []
    while len(avail1) <= 20:
        a = random.randint(1, 222)
        if a in avail1:
            continue
        avail1.append(a)
        print("Available seats during departure are:\n", avail1)
        time.sleep(4)
        print("\nEnter your choices:\n")
        c = 1
        while c <= len(adult):
            s = "For adult "+str(c)+": "
            b = int(input(s))
            if b not in avail1:
                print("Given seat is not available, try again")
                continue
            seat1.append(b)
            c = c + 1
    if adate is not None:
        while len(avail2) <= 20:
            a = random.randint(1, 222)
            if a in avail2:
                continue
            avail2.append(a)
            print("\n\nAvailable seats during return are:\n", avail2)
            time.sleep(4)
            print("\nEnter your choices:\n")
            c = 1
            while c <= len(adult):
                s = "For adult "+str(c)+": "
                b = int(input(s))
                if b not in avail2:
                    print("Given seat is not available, try again")
                    continue
                seat2.append(b)
                c = c + 1

# Function to print departure ticket
def depticket():
    pnr = ""
    for i in range(2):
        a = random.randint(65, 90)
        pnr = pnr + chr(a)
        pnr = pnr + str(random.randint(1000, 9999))
    print("-------------------------------------------------------------------------------------------------------------------------------------")
    print("\n\t\t\t\t\t\t\tAIR TICKET\n")
    print("-------------------------------------------------------------------------------------------------------------------------------------")
    print("\n\nPASSENGER NAME:", adult[1][0], "\tFROM:", dlist[dchoice][1], "\t\t\tTO:", dlist[dchoice][2])
    print("\nDEPARTURE TIME:", dlist[dchoice][5], ddate, "\tBOARDING TIME:", (dlist[dchoice][5]-1))
    print("\nCOMPANY:", dlist[dchoice][4], "\t\t\tFLIGHTNO.:", dlist[dchoice][0], "\t\tFLIGHT PNR:", pnr)
    print("\nNO. OF ADULTS:", len(adult), "\t\t\tNO. OF CHILDREN:", len(child))
    if serchoice == 1:
        group = random.randint(5, 9)
        print("\nGROUP NO.:", group, "\t\t\t\tSEATS:", seat1)
    else:
        group = random.randint(1, 4)
        print("\nGROUP NO.:", group, "\t\t\t\tSEATS:", seat1)
    print("\n\nBASE FAIR:", cost * len(adult), "\t\t\tTOTAL FAIR WITH GST:", tcost * len(adult))
    print("\n\nNOTICE: ALL PASSENGERS ARE REQUIRED TO FOLLOW THE PROPER PROTOCOLS OF COVID SAFETY. PASSENGERS WHO ARE FOUND TO VIOLATE THE SAFETY")
    print("PROTOCOLS MAYBE STOPPED FROM BOARDING THE FLIGHT UNTIL THEY FOLLOW THE NECESSITIES")
    print("-------------------------------------------------------------------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------------------------------------------------------------------\n\n")

# Function to print return ticket
def retticket():
    pnr = ""
    for i in range(2):
        a = random.randint(65, 90)
        pnr = pnr + chr(a)
        pnr = pnr + str(random.randint(1000, 9999))
    print("-------------------------------------------------------------------------------------------------------------------------------------")
    print("\n\t\t\t\t\t\t\tAIR TICKET\n")
    print("-------------------------------------------------------------------------------------------------------------------------------------")
    print("\n\nPASSENGER NAME:", adult[1][0], "\tFROM:", alist[achoice][1], "\t\t\tTO:", alist[achoice][2])
    print("\nDEPARTURE TIME:", alist[achoice][5], adate, "\tBOARDING TIME:", (alist[achoice][5]-1))
    print("\nCOMPANY:", alist[achoice][4], "\t\t\tFLIGHT NO.:", alist[achoice][0], "\t\tFLIGHT PNR:", pnr)
    print("\nNO. OF ADULTS:", len(adult), "\t\t\tNO. OF CHILDREN:", len(child))
    if serchoice == 1:
        group = random.randint(5, 9)
        print("\nGROUP NO.:", group, "\t\t\t\tSEATS:", seat2)
    else:
        group = random.randint(1, 4)
        print("\nGROUP NO.:", group, "\t\t\t\tSEATS:", seat2)
    print("\n\nBASE FAIR:", cost * len(adult), "\t\t\tTOTAL FAIR WITH GST:", tcost * len(adult))
    print("\n\nNOTICE: ALL PASSENGERS ARE REQUIRED TO FOLLOW THE PROPER PROTOCOLS OF COVID SAFETY. PASSENGERS WHO ARE FOUND TO VIOLATE THE SAFETY")
    print("PROTOCOLS MAYBE STOPPED FROM BOARDING THE FLIGHT UNTIL THEY FOLLOW THE NECESSITIES")
    print("-------------------------------------------------------------------------------------------------------------------------------------")
    print("-------------------------------------------------------------------------------------------------------------------------------------\n\n")

# Main program
while True:
    print("Loading", end="")
    for i in range(8):
        print(".", end="")
        time.sleep(1)
    print("\n")
    print("-----------------------------------------------------")
    print("\tWELCOME TO ONLINE FLIGHT BOOKING")
    print("-----------------------------------------------------")
    time.sleep(4)
    print('\n')
    check = place()
    if check == 1:
        print("\nDeparture and arrival cannot be the same, please try again")
        time.sleep(4)
        continue
    else:
        print('\nPlace of departure and arrival recorded\n\n')
        time.sleep(3)
    check = date()
    if check != 1 and check != 2:
        time.sleep(3)
        continue
    else:
        print('\nNature of flight and date(s) recorded\n\n')
        time.sleep(3)
    passenger()
    print('\nPassenger data recorded\n\n')
    time.sleep(3)
    check = serviceclass()
    if 1 <= check <= 3:
        print('\nPreferred service class recorded\n\n')
        time.sleep(3)
    else:
        print('Invalid choice, try again')
        time.sleep(3)
        continue
    check = typefly()
    if check == 1 or check == 2:
        print('\nPreferred type of flight stored\n\n')
        time.sleep(3)
    else:
        print('Invalid choice, try again')
        time.sleep(3)
        continue
    flightlist()
    print("\nChoice of flight recorded\n\n")
    time.sleep(3)
    print("Please choose preferred seats\n")
    seats()
    print("\nPreferred seats recorded\n\n")
    time.sleep(3)
    print("Calculating cost of flight", end="")
    for i in range(5):
        print(".", end="")
        time.sleep(1)
    price()
    time.sleep(3)
    print("\n\nGenerating ticket(s)", end="")
    for i in range(8):
        print(".", end="")
        time.sleep(1)
    print('\n\n\n\n\nDEPARTURE TICKET\n\n')
    depticket()
    if adate is not None:
        print('\n\n\nRETURN TICKET\n\n')
        retticket()
        ch = ""
        while len(ch) == 0:
            ch = input("\n\nPress any key followed by enter to continue: ")
            print("\n\nThank you for using our services to book a flight")
            time.sleep(3)
            s = ""
            while True:
                s = input("\n\nWould you like to book another flight? (y/n):")
                if s.lower() == 'y':
                    print("\nLoading the start page in a second\n\n\n")
                    time.sleep(3)
                    break
                elif s.lower() == 'n':
                    print("\n\nThank you again for using our services. Have a safe journey and remember to follow the COVID-safety protocols")
                    time.sleep(5)
                    break
                else:
                    print("Invalid input, please try again")
                    time.sleep(2)
            if s.lower() == 'y':
                continue
            elif s.lower() == 'n':
                break
