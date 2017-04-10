import sqlite3, datetime

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

def removePlayer(screen_name):
    db = database()
    cursor = db.cursor()
    cursor.execute('''
        update players
        set holiday = 1
        where screen_name = ?''', (screen_name,))
    db.commit()

def restorePlayer(screen_name):
    db = database()
    cursor = db.cursor()
    cursor.execute('''
        update players
        set holiday = 0
        where screen_name = ?''', (screen_name,))
    db.commit()

def isAdmin(screen_name):
    db = database()
    cursor = db.cursor()
    cursor.execute('''
        select admin from players 
        where screen_name = ?''', (screen_name,))
    admin=cursor.fetchone()
    if admin is None:
        return false
    else:
        return admin[0]

def newSeries(silly_name):
    db = database()
    cursor = db.cursor()
    cursor.execute('''
        insert into series (silly_name, finished) 
        values (?,?)''', (silly_name, False,))
    db.commit()
    return cursor.lastrowid

def newRound():
    db = database()
    cursor = db.cursor()
    cursor.execute('''
        select id, silly_name from series 
        where finished = ?''', (False,))
    series=cursor.fetchone()
    if series is None:
        return None
    else:
        today = datetime.date.today()
        friday = today + datetime.timedelta( (4-today.weekday()) % 7 )
        sunday = today + datetime.timedelta( (6-today.weekday()) % 7 )
        cursor.execute('''
            insert into rounds (series_id, entry_by, gamed_played_by) 
            values (?,?,?)''', (series[0], friday, sunday,))
        db.commit()
        r = {
            'silly_name': series[1], 
            'entry_by': friday,
            'gamed_played_by': sunday
        }
        return r
