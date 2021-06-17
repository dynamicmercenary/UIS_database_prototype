import psycopg2
import pandas as pd

Running = True

def getAttributes(filename):

        df = pd.read_excel (filename , sheet_name='Ark1', header=[0])

        name = df['Navn'].tolist()
        Region = df['Region'].tolist()
        telephone = df['Tlf'].tolist()
        email = df['Email'].tolist()

        return name, Region, telephone, email
def checkerForHasProgramFalse():
#Removes entity if the attribute of a store is set to false
    try:
        con = psycopg2.connect(database='program', user='postgres',
                                                password='postgres')

        cur = con.cursor()

        cur.execute('''
            SELECT sID 
            FROM Store 
            WHERE hasProgram = False;
            ''')

        recordb = cur.fetchall()

        getsID = 0

        for row in recordb:

            getsID = row[0]

            cur.execute('''
            SELECT * 
            FROM hasProgram 
            WHERE pID = {};
            '''.format(getsID))

            recordp = cur.fetchall()

            if recordp:

                cur.execute('''
                    DELETE FROM
                        hasProgram
                    WHERE pID = {0};
                    '''.format(getsID))

                con.commit()

            else: 
                continue

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if con:
            con.close()

def checkerForHasProgramTrue():

#Adds entity if the attribute of a store is set to true

    try:
        con = psycopg2.connect(database='program', user='postgres',
                                                password='postgres')

        cur = con.cursor()

        cur.execute('''
            SELECT sID 
            FROM Store 
            WHERE hasProgram = True;
            ''')

        recordb = cur.fetchall()

        getsID = 0

        for row in recordb:

            getsID = row[0]

            cur.execute('''
            SELECT * 
            FROM hasProgram 
            WHERE pID = {};
            '''.format(getsID))

            recordp = cur.fetchall()

            if not recordp:

                cur.execute('''
                    INSERT INTO 
                        public.hasProgram (pID) 
                    VALUES ({0});
                    '''.format(getsID))

                con.commit()

            else: 
                continue

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if con:
            con.close()

def updateHasProgramToTrue():
#SQL update attribute of a store is to true
    try:
        con = psycopg2.connect(database='program', user='postgres',
                                    password='postgres')

        cur = con.cursor()
        UpdateShop = input("Which storeID should be updated? ")
        cur.execute('''
                UPDATE Store 
                SET hasProgram = True 
                WHERE sID = {};
                '''.format(UpdateShop))
        con.commit()

        checkerForHasProgramTrue()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if con:
            con.close()

def updateHasProgramToFalse():

#SQL update attribute of a store is to false

    try:
        con = psycopg2.connect(database='program', user='postgres',
                                    password='postgres')

        cur = con.cursor()
        UpdateShop = input("Which storeID should be updated? ")
        cur.execute('''
                UPDATE Store 
                SET hasProgram = False 
                WHERE sID = {};
                '''.format(UpdateShop))
        con.commit()

        checkerForHasProgramFalse()

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

        checkerForHasProgramTrue()
        checkerForHasProgramFalse()

    elif ActionOption == "7":

        try:

            # Connect to the server - Use the databasename, user, and password you like
            con = psycopg2.connect(database='program', user='postgres',
                                                password='postgres')

            cur = con.cursor()

            name, region, telephone, email = getAttributes('Butikker/Butikker.xlsx')

            n = len(name)

            for i in range(n):   
            
                cur.execute('''
                SELECT name
                FROM Store
                WHERE sID = {};
                '''.format((i+1)))

                exists = cur.fetchone()

                if not exists:

                    cur.execute('''
                    INSERT INTO public.Store(sID, name, region, telephone, email) 
                    VALUES ({0}, '{1}', '{2}', '{3}', '{4}');
                    '''.format((i+1), name[i], region[i], telephone[i], email[i]))
            
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