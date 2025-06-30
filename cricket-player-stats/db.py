import mysql.connector
from datetime import datetime, date

# Function to connect to the database
def connect():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='206',
        database='test_wicket'
    )

# Function to calculate age (from birthdate to deathdate or today)
def calculate_age(birthdate, deathdate=None):
    birthdate = datetime.strptime(str(birthdate), "%Y-%m-%d").date()
    if deathdate:
        end_date = datetime.strptime(str(deathdate), "%Y-%m-%d").date()
    else:
        end_date = date.today()

    age_days = (end_date - birthdate).days
    years = age_days // 365
    days = age_days % 365
    return f"{years} years {days} days"

# Function to update all player ages
def update_player_ages():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT player_id, birthdate, deathdate FROM players")
    players = cur.fetchall()

    for player_id, birthdate, deathdate in players:
        age_str = calculate_age(birthdate, deathdate)
        cur.execute("UPDATE players SET current_age = %s WHERE player_id = %s", (age_str, player_id))

    conn.commit()
    conn.close()
