import psycopg2
import pandas as pd

Running = True

def getAttributes(filename):

        df = pd.read_excel (filename , sheet_name='Ark1', header=[0])

        navn = df['Navn'].tolist()
        Region = df['Region'].tolist()
        telefon = df['Tlf'].tolist()
        email = df['Email'].tolist()

        return navn, Region, telefon, email
def checkerForHarProgramFalse():
#Removes entity if the attribute of a store is set to false
    try:
        con = psycopg2.connect(database='program', user='postgres',
                                                password='postgres')

        cur = con.cursor()

        cur.execute('''
            SELECT bID 
            FROM butik 
            WHERE har_program = False;
            ''')

        recordb = cur.fetchall()

        getBid = 0

        for row in recordb:

            getBid = row[0]

            cur.execute('''
            SELECT * 
            FROM harProgram 
            WHERE pID = {};
            '''.format(getBid))

            recordp = cur.fetchall()

            if recordp:

                cur.execute('''
                    DELETE FROM
                        harProgram
                    WHERE pID = {0};
                    '''.format(getBid))

                con.commit()

            else: 
                continue

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if con:
            con.close()

def checkerForHarProgramTrue():

#Adds entity if the attribute of a store is set to true

    try:
        con = psycopg2.connect(database='program', user='postgres',
                                                password='postgres')

        cur = con.cursor()

        cur.execute('''
            SELECT bID 
            FROM butik 
            WHERE har_program = True;
            ''')

        recordb = cur.fetchall()

        getBid = 0

        for row in recordb:

            getBid = row[0]

            cur.execute('''
            SELECT * 
            FROM harProgram 
            WHERE pID = {};
            '''.format(getBid))

            recordp = cur.fetchall()

            if not recordp:

                cur.execute('''
                    INSERT INTO 
                        public.harProgram (pID) 
                    VALUES ({0});
                    '''.format(getBid))

                con.commit()

            else: 
                continue

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if con:
            con.close()

def updateHarProgramToTrue():
#SQL update attribute of a store is to true
    try:
        con = psycopg2.connect(database='program', user='postgres',
                                    password='postgres')

        cur = con.cursor()
        UpdateShop = input("Which storeID should be updated? ")
        cur.execute('''
                UPDATE butik 
                SET har_program = True 
                WHERE bID = {};
                '''.format(UpdateShop))
        con.commit()

        checkerForHarProgramTrue()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if con:
            con.close()

def updateHarProgramToFalse():

#SQL update attribute of a store is to false

    try:
        con = psycopg2.connect(database='program', user='postgres',
                                    password='postgres')

        cur = con.cursor()
        UpdateShop = input("Which storeID should be updated? ")
        cur.execute('''
                UPDATE butik 
                SET har_program = False 
                WHERE bID = {};
                '''.format(UpdateShop))
        con.commit()

        checkerForHarProgramFalse()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if con:
            con.close()

while (Running):
    

    # Ask users for input
    print("Enter what you wish to find of the following:")
    print(" (6) To update programs to stores")
    print(" (7) Insert stores to DB")
    print(" To exit, type 'exit'")
    ActionOption = input(": ")

    if ActionOption == "6":

        checkerForHarProgramTrue()
        checkerForHarProgramFalse()

    elif ActionOption == "7":

        try:

            # Connect to the server - Use the databasename, user, and password you like
            con = psycopg2.connect(database='program', user='postgres',
                                                password='postgres')

            cur = con.cursor()

            navn, region, telefon, email = getAttributes('Butikker/Butikker.xlsx')

            n = len(navn)

            for i in range(n):   
            
                cur.execute('''
                SELECT navn
                FROM butik
                WHERE bID = {};
                '''.format((i+1)))

                exists = cur.fetchone()

                if not exists:

                    cur.execute('''
                    INSERT INTO public.butik(bID, navn, region, telefon, email) 
                    VALUES ({0}, '{1}', '{2}', '{3}', '{4}');
                    '''.format((i+1), navn[i], region[i], telefon[i], email[i]))
            
                    con.commit()
                else: 
                    continue

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            if con:
                con.close()    

            
    elif ActionOption == "exit":

        Running = False

    else:

        print("Error, wrong input, input the number in front of the option you want to choose")

        Running = False