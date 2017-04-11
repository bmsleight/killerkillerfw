import sqlite3
db = sqlite3.connect('./kkfw/kkfw.db', detect_types=sqlite3.PARSE_DECLTYPES)

players = '''
    create table if not exists players (
    id integer primary key, 
    screen_name varchar unique,
    holiday BOOLEAN,
    still_in BOOLEAN,
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

cursor = db.cursor()
cursor.execute(players)
cursor.execute(teams)
cursor.execute(series)
cursor.execute(winners)
cursor.execute(payments)
cursor.execute(rounds)
cursor.execute(player_entries)

# Fixtures - Missing django yet ??
team_list = [
  ['AFC Bournemouth', 'Bournemouth'], 
  ['Arsenal', 'Gunners'], 
  ['Burnley', 'Burnley'], 
  ['Chelsea', 'Chelsea'], 
  ['Crystal Palace', 'Palace'],
  ['Everton', 'Everton'],
  ['Hull City', 'Hull'],
  ['Leicester City', 'Leicester'],
  ['Liverpool', 'Liverpool'],
  ['Manchester City', 'Man City'],
  ['Manchester United', 'Man U'], 
  ['Middlesbrough', 'Brough'], 
  ['Southampton', 'Saints'],
  ['Stoke City', 'Stoke'], 
  ['Sunderland', 'Sunderland'],
  ['Swansea City', 'Swansea'], 
  ['Tottenham Hotspur', 'Spurs'], 
  ['Watford', 'Watford'], 
  ['West Bromwich Albion', 'West Brom'], 
  ['West Ham United', 'West Ham']
  ]

for team in team_list:
    cursor.execute('''
        insert into teams (team_name, aka, inactive) 
        values (?,?,?)''', (team[0], team[1], False, ))        

cursor.execute('''
    insert into players (screen_name, holiday, still_in, admin) 
    values (?,?,?,?)''', ('bmsleight', False, False, True,))

db.commit()
