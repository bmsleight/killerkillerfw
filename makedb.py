import sqlite3
conn = sqlite3.connect('./kkfw/kkfw.db', detect_types=sqlite3.PARSE_DECLTYPES)

players = '''
    create table if not exists players (
    id integer primary key, 
    screen_name varchar unique,
    holiday BOOLEAN,
    admin BOOLEAN
    )
    '''

teams = '''
    create table if not exists teams (
    id integer primary key, 
    team_name varchar unique,
    aka varchar unique,
    inactive BOOLEAN
    )
    '''

series = '''
    create table if not exists series (
    id integer primary key, 
    silly_name varchar unique,
    finished BOOLEAN
    )
'''

# http://tinyurl.com/ldmck7g
rounds = '''
    create table if not exists rounds (
    id integer primary key, 
    series_id integer,
    entry_by DATE,
    gamed_played_by DATE,
    FOREIGN KEY(series_id) REFERENCES series(id)
    )
'''

winners = '''
    create table if not exists winners (
    id integer primary key, 
    series_id integer,
    players_id integer,    
    FOREIGN KEY(players_id) REFERENCES players(id),
    FOREIGN KEY(series_id) REFERENCES series(id)
    )    
'''

payments = '''
    create table if not exists payment (
    id integer primary key, 
    series_id integer,
    players_id integer,    
    FOREIGN KEY(players_id) REFERENCES players(id),
    FOREIGN KEY(series_id) REFERENCES series(id)
    )    
'''

player_entries = '''
    create table if not exists player_entries (
    id integer primary key, 
    players_id integer,
    teams_id integer,
    rounds_id integer,    
    FOREIGN KEY(players_id) REFERENCES players(id),
    FOREIGN KEY(teams_id) REFERENCES teams(id),
    FOREIGN KEY(rounds_id) REFERENCES round(id)
    )
'''

c = conn.cursor()
conn.execute(players)
conn.execute(teams)
conn.execute(series)
conn.execute(winners)
conn.execute(payments)
conn.execute(rounds)
conn.execute(player_entries)
