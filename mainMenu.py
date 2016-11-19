import sqlite3
import os
from patient import *
from reports import *
# The menu for doctor onlys.
# The menu ask the doctor for
# 1. Search a patient
# 2. Log out of the system
def doctorMenu(CONN, staff_id):
    os.system('clear')
    print("==========Doctor Main Menu==========")
    print("1. Search for a patient")
    print("2. logout")
    result = input("Please enter your choice: ")
    if result == '1':
        print("Select a patient")
        doctor = (staff_id, 'D')
        patientSelect(CONN, doctor)
    elif result == '2':
        print("Good Bye")
        CONN.close()
        return
    else:
        print("Invalid")
        return doctorMenu(CONN, staff_id)
    return doctorMenu(CONN, staff_id)

# The menu for nurses only.
# The menu ask the nurse for
# 1. Search a patient
# 2. Log out of the system
def nurseMenu(CONN, staff_id):
    print("==========Nurse Main Menu==========")
    print("1. Search for a patient")
    print("2. Add a new patient")
    print("3. logout")
    result = input("Please enter your choice: ")
    nurse = (staff_id, 'N')
    if result == '1':
        print("Select a patient")
        patientSelect(CONN, nurse)
    elif result == '2':
        print("Add Patient")
        addPatient(CONN, nurse)
    elif result == '3':
        print("Good Bye")
        CONN.close()
        return
    else:
        print("Invalid")
        return nurseMenu(CONN, staff_id)
    return nurseMenu(CONN, staff_id)

# The menu for admins only.
# The menu asks the admin for
# 1. Doctor prescription total amount within time period
# 2. Prescription amount-total by category
# 3. All prescriptions after diagnosis
# 4. All diagnoses prior to prescription
def adminMenu(CONN, staff_id):
    os.system('clear')
    print("==========Administration Main Menu==========")
    print("Select a report to create: ")
    print("1. Doctor prescription total amount within time period")
    print("2. Prescription amount-total by category")
    print("3. All prescriptions after diagnosis")
    print("4. All diagnoses prior to prescription")
    print("5. logout")
    result = input("Please enter your choice: ")
    admin = (staff_id, 'A')
    if result == '1':
        doctorReport(CONN, admin)
    elif result == '2':
        rxTotal(CONN, admin)
    elif result == '3':
        allRX(CONN, admin)
    elif result == '4':
        diagBeforeRX(CONN, admin)
    elif result == '5':
        print("Good Bye")
        CONN.close()
        return
    else:
        print("Invalid")
        return adminMenu(CONN, staff_id)
    return adminMenu(CONN, staff_id)
