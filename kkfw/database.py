import sqlite3

def database():
    db = sqlite3.connect('./kkfw/kkfw.db')
    return db

def existsPlayerNotOnHoliday(screen_name):
    db = database()
    cursor = db.cursor()
    cursor.execute('''
        select holiday from players 
        where screen_name = ?''', (screen_name,))
    holiday=cursor.fetchone()
    if holiday is None:
        return None
    else:
        return holiday[0]



def insertPlayer(screen_name):
    db = database()
    cursor = db.cursor()
    cursor.execute('''
        insert into players (screen_name, holiday) 
        values (?,?)''', (screen_name, False,))
    db.commit()

