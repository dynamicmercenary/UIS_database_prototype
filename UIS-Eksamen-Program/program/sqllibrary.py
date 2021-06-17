from psycopg2 import sql
import pandas as pd
from program import con, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    cur = con.cursor()

    schema = 'volunteer'
    id = 'vid'
    if str(user_id).startswith('60'):
        schema = 'coordinator'
        id = 'cid'

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
    WHERE vID = %s
    """
    cur.execute(sql, (ID,))
    user = Volunteer(cur.fetchone()) if cur.rowcount > 0 else None;
    cur.close()
    return user

def select_Coordinator(ID):
    cur = con.cursor()
    sql = """
    SELECT * FROM Coordinator
    WHERE cID = %s
    """
    cur.execute(sql, (ID,))
    user = Coordinator(cur.fetchone()) if cur.rowcount > 0 else None;
    cur.close()
    return user

def findStores(region):
    cur = con.cursor()
    sql = '''
    SELECT sID, name
    FROM Store
    WHERE region = %s
    ORDER BY sID           
    '''
    cur.execute(sql, (region,))   
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset

def findStoreV(ID):
    cur = con.cursor()
    sql = '''
    SELECT sID, name
    FROM Store 
    WHERE sID = %s         
    '''
    cur.execute(sql, (ID,))   
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset
 
def getRegions():
    cur = con.cursor()
    sql = '''
    SELECT DISTINCT region
    FROM Store         
    '''
    cur.execute(sql)   
    tuple_resultset = cur.fetchall()
    cur.close()
    return tuple_resultset

def findScala(region):
    cur = con.cursor()
    sql = '''
    SELECT p.Scala, s.name, p.weekDay
    FROM hasProgram AS p
        INNER JOIN Store AS s
            ON s.hasProgram = true AND p.pID = s.sID
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
    FROM hasProgram
    WHERE pID = %s          
    '''
    cur.execute(sql, (ID,))   
    tuple_resultset = cur.fetchone()
    cur.close()
    return tuple_resultset

def getWeekdayV(ID):
    cur = con.cursor()
    sql = '''
    SELECT weekDay
    FROM hasProgram
    WHERE pID = %s          
    '''
    cur.execute(sql, (ID,))   
    tuple_resultset = cur.fetchone()
    cur.close()
    return tuple_resultset

def getFirstShiftV(ID):
    cur = con.cursor()
    sql = '''
    SELECT firstShift
    FROM hasProgram
    WHERE pID = %s          
    '''
    cur.execute(sql, (ID,))   
    tuple_resultset = cur.fetchone()
    cur.close()
    return tuple_resultset

def getInfo(id):
    cur = con.cursor()
    sql = '''
    SELECT name, email, telephone
    FROM Store
    WHERE sID = %s           
    '''
    cur.execute(sql, (id,))   
    tuple_resultset = cur.fetchone()
    cur.close()
    return tuple_resultset

def updateScale(update, sID):
    cur = con.cursor()
    sql = '''
    UPDATE hasProgram
    SET scala = %s
    WHERE pID = %s           
    '''
    cur.execute(sql, (update, sID,)) 
    con.commit()  
    cur.close()

def getName(sID):
    cur = con.cursor()
    sql = '''
    SELECT name
    FROM Store
    WHERE sID = %s           
    '''
    cur.execute(sql, (sID,))   
    tuple_resultset = cur.fetchone()
    cur.close()
    return tuple_resultset

def updateFirstshift(update, sID):
    cur = con.cursor()
    sql = '''
    UPDATE hasProgram
    SET firstShift = firstShift + %s
    WHERE pID = %s           
    '''
    cur.execute(sql, (update, sID,)) 
    con.commit()  
    cur.close()

def updateWeekday(update, sID):
    cur = con.cursor()
    sql = '''
    UPDATE hasProgram
    SET weekDay = %s
    WHERE pID = %s           
    '''
    cur.execute(sql, (update, sID,)) 
    con.commit()  
    cur.close()

def checkerForhasProgram(UpdateShop):

#Adds entity if the attribute of a store is set to true

    cur = con.cursor()

    sql = '''
    INSERT INTO 
        public.hasProgram (pID) 
    VALUES (%s);
    '''
    cur.execute(sql, (UpdateShop,))

    con.commit()

def createUser(UpdateShop, StoreName):
    cur = con.cursor()

    sql = '''
    INSERT INTO 
        public.Volunteer (vID, name) 
    VALUES (%s,%s);
    '''
    cur.execute(sql, (UpdateShop,StoreName))

    con.commit()

def deleteEntityHasProgram(UpdateShop):

#Adds entity if the attribute of a store is set to true

    cur = con.cursor()

    sql = '''
    DELETE FROM 
        public.hasProgram
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

def updateHasProgramToTrue(boolVal, UpdateShop):
#SQL update attribute of a store is to true
    cur = con.cursor()
    sql = '''
    UPDATE Store 
    SET hasProgram = %s 
    WHERE sID = %s
    '''
    cur.execute(sql, (boolVal, UpdateShop,))  
    con.commit()

    checkerForhasProgram(UpdateShop)

def checkForProgram(UpdateShop):
    cur = con.cursor()
    sql = '''
    SELECT * 
    FROM hasProgram
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