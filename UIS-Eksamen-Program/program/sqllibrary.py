from psycopg2 import sql
import pandas as pd
from program import con, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    cur = con.cursor()

    schema = 'volunteer'
    id = 'id'
    if str(user_id).startswith('60'):
        schema = 'coordinator'
        id = 'id'

    user_sql = sql.SQL("""
    SELECT * FROM {}
    WHERE {} = %s
    """).format(sql.Identifier(schema), sql.Identifier(id))

    cur.execute(user_sql, (int(user_id),))
    if cur.rowcount > 0:
        return Coordinator(cur.fetchone()) if schema == 'coordinator' else Volunteer(cur.fetchone())
    else:
        return None


class Coordinator(tuple, UserMixin):
    def __init__(self, coordinator_data):
        self.ID = coordinator_data[0]
        self.name = coordinator_data[1]
        self.password = coordinator_data[2]

    def get_id(self):
       return (self.ID)

class Volunteer(tuple, UserMixin):
    def __init__(self, user_data):
        self.ID = user_data[0]
        self.name = user_data[1]
        self.password = user_data[2]

    def get_id(self):
       return (self.ID)

def select_Volunteer(ID):
    cur = con.cursor()
    sql = """
    SELECT * FROM Volunteer
    WHERE ID = %s
    """
    cur.execute(sql, (ID,))
    user = Volunteer(cur.fetchone()) if cur.rowcount > 0 else None;
    cur.close()
    return user

def select_Coordinator(ID):
    cur = con.cursor()
    sql = """
    SELECT * FROM Coordinator
    WHERE ID = %s
    """
    cur.execute(sql, (ID,))
    user = Coordinator(cur.fetchone()) if cur.rowcount > 0 else None;
    cur.close()
    return user

def findStores(region):
    cur = con.cursor()
    sql = '''
    SELECT bID, navn
    FROM butik
    WHERE region = %s
    ORDER BY bID           
    '''
    cur.execute(sql, (region,))   
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset

def findStoresV(ID):
    cur = con.cursor()
    sql = '''
    SELECT bID, navn
    FROM Butik 
    WHERE bid = %s         
    '''
    cur.execute(sql, (ID,))   
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset
 
def getRegions():
    cur = con.cursor()
    sql = '''
    SELECT DISTINCT region
    FROM butik         
    '''
    cur.execute(sql)   
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset

def getScala(region):
    cur = con.cursor()
    sql = '''
    SELECT p.Scala, b.navn, p.ugedag
    FROM harProgram AS p
        INNER JOIN BUTIK AS b
            ON b.har_program = true AND p.pID = b.bID
    WHERE region = %s
    ORDER BY p.scala DESC           
    '''
    cur.execute(sql, (region,))   
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset

def getScalaV(ID):
    cur = con.cursor()
    sql = '''
    SELECT scala
    FROM harProgram
    WHERE pID = %s          
    '''
    cur.execute(sql, (ID,))   
    tuple_resultset = cur.fetchone()
    cur.close()
    return tuple_resultset

def getWeekdayV(ID):
    cur = con.cursor()
    sql = '''
    SELECT Ugedag
    FROM harProgram
    WHERE pID = %s          
    '''
    cur.execute(sql, (ID,))   
    tuple_resultset = cur.fetchone()
    cur.close()
    return tuple_resultset

def getFirstShiftV(ID):
    cur = con.cursor()
    sql = '''
    SELECT first_shift
    FROM harProgram
    WHERE pID = %s          
    '''
    cur.execute(sql, (ID,))   
    tuple_resultset = cur.fetchone()
    cur.close()
    return tuple_resultset

def getInfo(id):
    cur = con.cursor()
    sql = '''
    SELECT navn, email, telefon
    FROM butik
    WHERE bID = %s           
    '''
    cur.execute(sql, (id,))   
    tuple_resultset = cur.fetchone()
    cur.close()
    return tuple_resultset

def updateScale(update, bID):
    cur = con.cursor()
    sql = '''
    UPDATE harProgram
    SET scala = %s
    WHERE pID = %s           
    '''
    cur.execute(sql, (update, bID,)) 
    con.commit()  
    cur.close()

def getName(bID):
    cur = con.cursor()
    sql = '''
    SELECT navn
    FROM butik
    WHERE bID = %s           
    '''
    cur.execute(sql, (bID,))   
    tuple_resultset = cur.fetchone()
    cur.close()
    return tuple_resultset

def updateFirstshift(update, bID):
    cur = con.cursor()
    sql = '''
    UPDATE harProgram
    SET first_shift = first_shift + %s
    WHERE pID = %s           
    '''
    cur.execute(sql, (update, bID,)) 
    con.commit()  
    cur.close()

def updateWeekday(update, bID):
    cur = con.cursor()
    sql = '''
    UPDATE harProgram
    SET ugedag = %s
    WHERE pID = %s           
    '''
    cur.execute(sql, (update, bID,)) 
    con.commit()  
    cur.close()

def checkerForHarProgram(UpdateShop):

#Adds entity if the attribute of a store is set to true

    cur = con.cursor()

    sql = '''
    INSERT INTO 
        public.harProgram (pID) 
    VALUES (%s);
    '''
    cur.execute(sql, (UpdateShop,))

    con.commit()

def createUser(UpdateShop, StoreName):
    cur = con.cursor()

    sql = '''
    INSERT INTO 
        public.Volunteer (id, name) 
    VALUES (%s,%s);
    '''
    cur.execute(sql, (UpdateShop,StoreName))

    con.commit()

def deleteEntityHarProgram(UpdateShop):

#Adds entity if the attribute of a store is set to true

    cur = con.cursor()

    sql = '''
    DELETE FROM 
        public.harProgram
    WHERE pid = %s;
    '''
    cur.execute(sql, (UpdateShop,))
    con.commit()

def deleteUser(UpdateShop):

    cur = con.cursor()

    sql = '''
    DELETE FROM 
        public.volunteer
    WHERE id = %s;
    '''
    cur.execute(sql, (UpdateShop,))
    con.commit()

def updateHarProgramToTrue(boolVal, UpdateShop):
#SQL update attribute of a store is to true
    cur = con.cursor()
    sql = '''
    UPDATE butik 
    SET har_program = %s 
    WHERE bID = %s
    '''
    cur.execute(sql, (boolVal, UpdateShop,))  
    con.commit()

    checkerForHarProgram(UpdateShop)

def checkForProgram(UpdateShop):
    cur = con.cursor()
    sql = '''
    SELECT * 
    FROM harProgram
    WHERE pID = %s
    '''
    cur.execute(sql, (UpdateShop,))  
    tuple_resultset = cur.fetchone()
    cur.close()
    return tuple_resultset


def checkPasswordC(ID, oldPassword):
    cur = con.cursor()
    sql = '''
    SELECT name
    FROM Coordinator
    WHERE password = %s
    AND ID = %s
    '''
    cur.execute(sql, (oldPassword, ID))  
    tuple_resultset = cur.fetchone()
    cur.close()
    return tuple_resultset

def changePasswordC(ID, newPassword):
    cur = con.cursor()
    sql = '''
    UPDATE Coordinator
    Set password = %s
    WHERE ID = %s
    '''
    cur.execute(sql, (newPassword, ID))  
    con.commit()
    cur.close()

def checkPassword(ID, oldPassword):
    cur = con.cursor()
    sql = '''
    SELECT name
    FROM Volunteer
    WHERE password = %s
    AND ID = %s
    '''
    cur.execute(sql, (oldPassword, ID))  
    tuple_resultset = cur.fetchone()
    cur.close()
    return tuple_resultset

def changePassword(ID, newPassword):
    cur = con.cursor()
    sql = '''
    UPDATE Volunteer
    Set password = %s
    WHERE ID = %s
    '''
    cur.execute(sql, (newPassword, ID))  
    con.commit()
    cur.close()