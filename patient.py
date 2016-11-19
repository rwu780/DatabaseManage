import sqlite3
import os

#Search for a patient name
#Every doctor enter a name, it will find the patinet name that is similar to the patient name
#Once a match is found, the system will output a list of matched patient names.
#Then, the doctor select the patient to continue
def patientSelect(CONN, staff):
    c = CONN.cursor()
    print("Search for Patient")
    select = input("Enter patient name(type 'exit' to leave): ")
    if select == 'exit':
        os.system('clear')
        #return doctorMenu(CONN, staff[0])
        return
    c.execute('''SELECT hcno, name FROM patients WHERE name LIKE ?''', ('%'+select+'%',))
    rows = c.fetchall()
    if len(rows) == 0:      
        print("No patient found, please try again")
        return patientSelect(CONN, staff)

    count = 1
    for x in rows:
        print(str(count)+": patient hcno "+x[0]+"; patient name: "+x[1])
        count = count + 1

    try:
        select = input("Please select your patient: ")
        selectedPatient = int(select)-1
        patientHCNO = rows[selectedPatient][0]
        patientName = rows[selectedPatient][1]
        patient = (patientHCNO, patientName)
    except:
        print("Invalid input, please try again")
        return patientSelect(CONN, staff)
    return patientChart(CONN, staff, patient)


#Output the tables related to the patient
#The doctor can select an open chart to continue
def patientChart(CONN, staff, patient):
    c = CONN.cursor()
    os.system('clear')

    print("Patient HCNO: " + patient[0] + ", Patient Name: " + patient[1])
    c.execute('''SELECT * 
                    FROM charts 
                    WHERE hcno = ?
                    ORDER BY adate
                    ''', (patient[0],))
    rows = c.fetchall()
    count = 1
    checkOpenChart = 0
    for x in rows:
        print(str(count)+": chart id: "+x[0]+"; patient hcno: "+ x[1] + "; admission time: "+x[2], end="")
        if x[3] is None:
            print(" discharge time: " + "Status: open.")
            checkOpenChart = checkOpenChart + 1
        else:
            print(" discharge time: " + x[3] + "Status: close.")
        count = count + 1;
    if checkOpenChart == 0:
        print("No open chart")
        openChart = input("Do you want to create a new chart (y/n):")
        if openChart == 'y':
            print("Open chart")
            return addChart(CONN, staff, patient)
    else:
        print("")
        print("You have an open chart. If you want a new chart, close the open chart first")

    try:
        select = input("Please select a chart to continue(type 'exit' to leave): ")
        if select == 'exit':
            os.system('clear')
            return patientSelect(CONN, staff)
        selectChart = int(select)-1
        chart_id = rows[selectChart][0]     
    except:
        print("Invalid enry")
        return patientChart(CONN, staff, patient)

    if rows[selectChart][3] is None:
        editAble = 1
    else:
        editAble = 0

    return viewChart(CONN, chart_id, staff, patient, editAble)

#View a list of charts that related to the patient
def viewChart(CONN, chart_id, staff, patient, editAble):
    c = CONN.cursor()
    os.system('clear')
    print("Patient HCNO: " + patient[0] + ", Patient Name: " + patient[1])
    print("symptoms table")
    c.execute('''SELECT * 
                    FROM symptoms 
                    WHERE hcno = ? AND chart_id = ?
                    ORDER BY obs_date;''', (patient[0], chart_id))
    rows = c.fetchall()
    for x in rows:
        print(x)
    print("diagnosis table")
    c.execute('''SELECT * 
                    FROM diagnoses 
                    WHERE hcno = ? AND chart_id = ?
                    ORDER BY ddate;''', (patient[0], chart_id))
    rows = c.fetchall()
    for x in rows:
        print(x)
    print("medication table")
    c.execute('''SELECT * 
                    FROM medications 
                    WHERE hcno = ? AND chart_id = ?
                    ORDER BY mdate;''', (patient[0], chart_id))
    rows = c.fetchall()
    for x in rows:
        print(x)

    if editAble == 0:
        input("Press any key to return: ")
        return patientChart(CONN, staff, patient)
    if staff[1] == 'D':
        return doctorChartMenu(CONN, patient, chart_id, staff)
    elif staff[1] == 'N':
        return nurseChartMenu(CONN, patient, chart_id, staff)   

#If the chart is open, able to edit the chart
def doctorChartMenu(CONN, patient, chart_id, staff):
    print("==========Chart Menu==========")
    print("1. Add a symptoms")
    print("2. Add a Diagnosis")
    print("3. Add a medication")
    print("4. Exit")
    select = input("Please select an option to continue: ")
    if select == '1':
        print("Add symptoms")
        os.system('clear')
        return addSymptoms(CONN, patient, chart_id, staff)
    elif select == '2':
        print("Add Diagnosis")
        os.system('clear')
        return addDiagnosis(CONN, patient, chart_id, staff)
    elif select == '3':
        print("Add medication")
        os.system('clear')
        return addMedication(CONN, patient, chart_id, staff)
    elif select == '4':
        return patientChart(CONN, staff, patient)
    else:
        print("Invalid entry, please try again")
        return patientSelect(CONN, staff)

def nurseChartMenu(CONN, patient, chart_id, staff):
    print("Chart Menu")
    print("1. Add a symptoms")
    print("2. close chart")
    print("3. Exit")
    select = input("Please select an option to cintinue: ")

    if select == '1':
        os.system('clear')
        return addSymptoms(CONN, patient, chart_id, staff)
    elif select == '2':
        print("xx")
        return closeChart(CONN, patient, chart_id, staff)
    elif select == '3':
        return patientChart(CONN, staff, patient)
    else:
        print("Invalid, please try again")
        return patientSelect(CONN, staff)
#Insert a symptom
#Ask doctor for symptom name
#Observer date will be current time
# The function will return to viewChart()
def addSymptoms(CONN, patient, chart_id, staff):
    c = CONN.cursor()
    symptoms = input("Please enter a symptom: ")
    while len(symptoms) == 0:
        symptoms = input("Please enter a symptom: ")
            
    c.execute('''INSERT INTO symptoms VALUES
                    (?,?,?,DateTime('now','localtime'),?);''',(patient[0], chart_id, staff[0], symptoms))
    CONN.commit()
    return viewChart(CONN, chart_id, staff, patient, 1)

# Insert a diagnosis
# Will prompt for a diagnose name
# Observe date will be current time
# Return to viewChart() after finish
def addDiagnosis(CONN, patient, chart_id, staff):
    #Insert a diagnosis
    c = CONN.cursor()
    diagnosis = input("Please enter a diagnosis: ")
    while len(diagnosis) == 0:
        diagnosis = input("Please enter a diagnosis: ")
            
    c.execute('''INSERT INTO diagnoses VALUES
                    (?,?,?,DateTime('now', 'localtime'),?);''',(patient[0], chart_id, staff[0], diagnosis))
    CONN.commit()
    return viewChart(CONN, chart_id, staff, patient, 1)

# Insert a medication
# Will prompt for a medication name
# start date will be today
# Return to viewChart() after finish
def addMedication(CONN, patient, chart_id, staff):
    c = CONN.cursor()
    c.execute("SELECT * FROM patients WHERE hcno = ?;",(patient[0],))
    rows = c.fetchone()
    patientAge = rows[2]

    #Get Medication Name, if not exist in database, return to previous page
    medicationName = input("Please enter a medication: ")
    c.execute("SELECT sug_amount FROM dosage WHERE drug_name = ? AND age_group = ?;", (medicationName,patientAge))
    dosageAmount = c.fetchone()
    if dosageAmount == None:
        print("Drug Name not exist")
        input("Press any key to return")
        return viewChart(CONN, chart_id, staff, patient, 1)

    c.execute('''SELECT drug_name FROM reportedallergies WHERE hcno = ?;''', (patient[0],))
    allergies = c.fetchone()
    for x in allergies:
        if x == medicationName:
            print("WARNING, the patinet is allergic to "+ x)
    c.execute('''SELECT canbe_alg FROM inferredallergies WHERE alg = ?;''',(medicationName,))
    
    inferallergies = c.fetchall()
    for x in inferallergies:
        print("Patinet can be allergic to: " + x[0])

    # Get prescripbtion amount, if larger than suggest amount, display warning message
    amount = int(input("Medication amount: "))
    if amount > dosageAmount[0]:
        print("Suggest Amount: "+ str(dosageAmount[0]))
        confirm = input("WARNING: Prescibe Amount is greater than suggest amount.Confirm (y/n)")

        if confirm == 'n':
            return viewChart(CONN, chart_id, staff, patient, 1)
        
    #Get medication period
    day = input("Medication length(in days): ")

    c.execute('''INSERT INTO medications VALUES
                    (?,?,?,DateTime('now', 'localtime'), DateTime('now','localtime'),DateTime('now',?,'localtime'),?,?);''',(patient[0], chart_id, staff[0], '+'+day+' day', amount, medicationName))
    CONN.commit()
    return viewChart(CONN, chart_id, staff, patient, 1)

def closeChart(CONN, patient, chart_id, staff):
    c = CONN.cursor()
    c.execute("SELECT * FROM charts WHERE chart_id = ?;", (chart_id,))
    rows = c.fetchone()

    if rows[3] is None:
        print("Close chart id "+str(chart_id)+"?")
        print("1. Yes.")
        print("2. No.")
        result = input("Please enter your choice: ")
        if result == '1':
            print("Closing chart.")
            c.execute('''UPDATE charts SET edate = DateTime('now','localtime')
                WHERE chart_id = ?;''', (chart_id,))
            CONN.commit()
            return viewChart(CONN, chart_id, staff, patient, 1)
        elif result == '2':
            return viewChart(CONN, chart_id, staff, patient, 1)
        else:
            print("Invalid")
            return closeChart(CONN, patient, chart_id, staff)

def addPatient(CONN, staff):
    c = CONN.cursor()
    print("==========New Patient Record==========")

    name = input("Please enter patient name: ")
    
    hcno = input("Please enter patient HCNO: ")
    try:
        testHcno = int(hcno)
    except:
        print("Invalid HCNO, please try again")
        return addPatient(CONN, staff)
    age_group = input("Please enter age group: ")
    address = input("Please enter address: ")
    phone = input("Please enter phone number: ")
    emg_phone = input("Please enter emergency phone number: ")
    try:
        c.execute('''INSERT INTO patients VALUES
            (?,?,?,?,?,?);''',(hcno, name, age_group, address, phone, emg_phone))
        CONN.commit()
        print("Patient record created.")
    except:
        print("Invalid entry, patient already exists")

def addChart(CONN, staff, patient):
    c = CONN.cursor()
    #phcno = input("Please enter patient health care #: ")
    c.execute("SELECT chart_id FROM charts ORDER BY chart_id DESC LIMIT 1;")
    last_chart = c.fetchone()
    if last_chart[0] is not None:
        new_chart_id = int(last_chart[0])+1
    else:
        new_chart_id = '00001'

    c.execute('''INSERT INTO charts VALUES
                    (?,?, DateTime('now','localtime'), ?);''', (new_chart_id, patient[0], None))
    c.execute("SELECT * FROM charts WHERE hcno = ? ORDER BY adate DESC LIMIT 1;", (patient[0],))
    CONN.commit()

    print("A new chart had been create. Chart ID: "+ str(new_chart_id))
    return patientChart(CONN, staff, patient)
