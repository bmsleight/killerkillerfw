import sqlite3, datetime

def database():
    db = sqlite3.connect('./kkfw/kkfw.db')
    return db

def prizePool():
    FEE = 5.00
    db = database()
    cursor = db.cursor()
    cursor.execute('''
        select screen_name from players 
        where holiday = 0''')        
    return len(cursor.fetchall()) * FEE

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
        insert into players (screen_name, holiday, still_in, admin) 
        values (?,?,?,?)''', (screen_name, False, False, False,))
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
    # All player not on holiday back in the game
    cursor.execute('''
        update players
        set still_in = 0
        where holiday  = 0''')
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
        print("Series", series[0])
        cursor.execute('''
        select * from rounds 
        where series_id = ?''', (series[0],))        
        round_num = len(cursor.fetchall())
        print('round_num', round_num, type(round_num))
        r = {
            'silly_name': series[1],
            'round_num': round_num, 
            'entry_by': friday,
            'gamed_played_by': sunday
        }
        return r


def playerRowtoDict(row):
    r = {
        'id': row[0],
        'screen_name': row[1], 
        'holiday': row[2],
        'still_in': row[3],
        'admin': row[4]
        }
    return r

def playersInCurrentSeries():
    db = database()
    cursor = db.cursor()
    cursor.execute('''
        select * from players 
        where still_in = 0''')        
    rows = cursor.fetchall()
    players = []
    for row in rows:
        players.append(playerRowtoDict(row))
    return players
