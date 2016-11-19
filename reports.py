import sqlite3
import os

# Report outlinining the amount and name
# of each drug a doctor has prescribed
# within a time period.
def doctorReport(CONN, admin):
    c = CONN.cursor()
    os.system('clear')
    print("Enter the date in the following format: YYYY-mm-dd ")
    start_period = input("Enter start of period: ")
    end_period = input("Enter end of period: ")
    c.execute('''SELECT name, drug_name, SUM(amount)
            FROM staff, medications
            WHERE mdate BETWEEN ? AND ?
            AND staff.staff_id = medications.staff_id
            GROUP BY name, drug_name''', (start_period,end_period))
    rows = c.fetchall()
    for x in rows:
        print(x)
    return

# Report outlining the total amount
# prescribed for a drug in a given
# category within a time period.
def rxTotal(CONN, admin):
    c = CONN.cursor()
    os.system('clear')
    print("Enter the date in the following format: YYYY-mm-dd ")
    start_period = input("Enter start of period: ")
    end_period = input("Enter end of period: ")
    c.execute('''SELECT drugs.category, drugs.drug_name, SUM(amount)
            FROM drugs, medications
            WHERE medications.mdate BETWEEN ? AND ?
            AND drugs.drug_name = medications.drug_name
            GROUP BY drugs.category, drugs.drug_name''', (start_period,end_period))
    rows = c.fetchall()
    print("Total amount of each drug prescribed within a category: ")
    for x in rows:
        print(x)
    c.execute('''SELECT drugs.category, SUM(amount)
            FROM drugs, medications
            WHERE medications.mdate BETWEEN ? AND ?
            AND drugs.drug_name = medications.drug_name
            GROUP BY drugs.category''', (start_period,end_period))
    rows = c.fetchall()
    print("Grand total prescribed for a category: ")
    for x in rows:
        print(x)
    return

# Report outlining all possible
# medications that have been
# prescribed over time after a
# given diagnosis.
def allRX(CONN, admin):
    c = CONN.cursor()
    os.system('clear')
    select = input("Enter a diagnosis (case sensitive): ")
    c.execute('''SELECT ddate
            FROM diagnoses
            WHERE diagnosis = ?
            ORDER BY ddate''', (select,))
    first_ddate = c.fetchone()
    c.execute('''SELECT medications.drug_name, COUNT(medications.drug_name)
            FROM medications, diagnoses
            WHERE diagnoses.diagnosis = ?
            AND diagnoses.chart_id = medications.chart_id
            AND medications.mdate BETWEEN ? AND DateTime('now','localtime')
            GROUP BY medications.drug_name
            ORDER BY COUNT(medications.drug_name) DESC''', (select,first_ddate[0]))
    rows = c.fetchall()
    print("Frequency of each prescribed medication since diagnosis date " +first_ddate[0]+": ")
    for x in rows:
        print(x)
    return

# Report outlining all diagnoses
# made prior to prescribing a
# specific drug.
def diagBeforeRX(CONN, admin):
    c = CONN.cursor()
    os.system('clear')
    select = input("Enter a drug (case sensitive): ")
    c.execute('''SELECT diagnoses.diagnosis, AVG(medications.amount)
            FROM medications, diagnoses
            WHERE medications.drug_name = ?
            AND diagnoses.chart_id = medications.chart_id
            AND diagnoses.ddate BETWEEN julianday('1900-02-04 11:02:03') AND medications.mdate
            GROUP BY medications.drug_name, diagnoses.diagnosis
            ORDER BY AVG(medications.amount) DESC''', (select,))
    rows = c.fetchall()
    print("Diagnoses prior to prescription: ")
    for x in rows:
        print(x)
    return

