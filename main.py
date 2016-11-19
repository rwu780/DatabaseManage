import sqlite3
import getpass
from mainMenu import *
import hashlib
import os

# Connect to database
def connectToDB():
    CONN = sqlite3.connect('hospital.db')
    init(CONN)


# initial menu, allow the user to log in with existing
# account, register for a new account or exit the program
def init(CONN):
    print("==========WELCOME==========")
    print("Please enter the option number to continue")
    print("1. Log in")
    print("2. register")
    print("3. Exit")

    # get input
    option = input("Please enter a option number: ")
    if option == "1":
        print("Login")
        os.system('clear')
        return login(CONN)
    elif option == "2":
        os.system('clear')
        return register(CONN)
    elif option == "3":
        return close(CONN)
    else:
        print("Incorrect option, please try again")
        return init(CONN)

# Login screen
def login(CONN):
    c = CONN.cursor()
    login = input("Please enter your login ID: ")

    #Check username
    c.execute("SELECT staff_id, role, password FROM staff WHERE login = ?;",(login,))
    
    # row[0] = staff_id
    # row[1] = role
    # row[2] = password
    rows = c.fetchone()

    #If username not exist, return to init()
    if rows == None:
        print("Username not exist")
        return init(CONN)

    #Get password
    temppwd = getpass.getpass().encode('utf-8')
    pwd = hashlib.sha512(temppwd).hexdigest()
    
    #check validity of account 
    if rows[2] == pwd:
        print("Success")
    else:
        print("Incorrect password")
        return init(CONN)
    if rows[1] == 'D':
        return doctorMenu(CONN, rows[0])
    elif rows[1] == 'N':
        return nurseMenu(CONN, rows[0])
    elif rows[1] == 'A':
        return adminMenu(CONN, rows[0])
    else:
        print("Invalid entry")
        return init(CONN)

def register(CONN):
    #conn = sqlite3.connect('hospital.db')
    c = CONN.cursor()
    print("Please enter your role ")
    print("1. Doctor")
    print("2. Nurse")
    print("3. Admin staff")
    option = input("Please enter your role: ")
    if option == '1':
        role = 'D'
    elif option == '2':
        role = 'N'
    elif option == '3':
        role = 'A'
    else:
        print("Invalid entry, please try again")
        return register()
    
    #enter staff ID
    staff_id = input("Please enter your staff_id: ")
    while len(staff_id) == 0:
        print("Invalid entry, please enter your staff_id again")
        staff_id = input("Please enter your staff_id")
    
    #enter name
    name = input("Please enter your name: ")
    while len(name) == 0:
        print("Invalid entry, please enter your name again")
        staff_id = input("Please enter your name: ")
    
    #enter login
    newlogin = input("Pease enter a login id: ")
    while len(newlogin) == 0:
        print("Invalid entry, please try again")
        newlogin = input("Please enter a login id: ")
    
    #enter pwd
    temppwd = getpass.getpass().encode('utf-8')
    #Encrypted
    pwd = hashlib.sha512(temppwd).hexdigest()

    #Insert into table
    try:
        c.execute('''INSERT into staff VALUES 
                    (?,?,?,?,?);''',(staff_id, role, name, newlogin, pwd))
        CONN.commit()
    except:
        print("Error, please try again")

    #Go to menu
    if role == 'D':
        return doctorMenu(CONN, staff_id)
    elif role == 'N':
        return nurseMenu(CONN, staff_id)
    else:
        return adminMenu(CONN, staff_id)
def close(CONN):
    CONN.close()
    print("Good Bye")
    return
if __name__ == '__main__':

    connectToDB()