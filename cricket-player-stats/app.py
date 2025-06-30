from flask import Flask, render_template, request, redirect, url_for
from db import connect
from flask_cors import CORS
from datetime import date, datetime

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    conn = connect()
    cur = conn.cursor(dictionary=True)

    player = None
    searched = False

    if request.method == 'POST':
        name = request.form.get('search_name')
        searched = True
        cur.execute("SELECT * FROM players WHERE full_name LIKE %s", ('%' + name + '%',))
        player = cur.fetchone()
        players = []
    else:
        cur.execute("SELECT player_id, full_name FROM players")
        players = cur.fetchall()

    conn.close()
    return render_template('index.html', players=players, player=player, searched=searched)

@app.route('/player/<player_id>')
def player_profile(player_id):
    conn = connect()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM players WHERE player_id = %s", (player_id,))
    player = cur.fetchone()
    conn.close()
    return render_template('player_profile.html', player=player)

@app.route('/batting/<player_id>')
def batting_stats(player_id):
    conn = connect()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM batting_stats WHERE player_id = %s", (player_id,))
    stats = cur.fetchone()
    cur.execute("SELECT full_name FROM players WHERE player_id = %s", (player_id,))
    player = cur.fetchone()
    conn.close()
    return render_template('batting_stats.html', stats=stats, player_name=player['full_name'])

@app.route('/bowling/<player_id>')
def bowling_stats(player_id):
    conn = connect()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM bowling_stats WHERE player_id = %s", (player_id,))
    stats = cur.fetchone()
    cur.execute("SELECT full_name FROM players WHERE player_id = %s", (player_id,))
    player = cur.fetchone()
    conn.close()
    return render_template('bowling_stats.html', stats=stats, player_name=player['full_name'])

@app.route('/fielding/<player_id>')
def fielding_stats(player_id):
    conn = connect()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM fielding_stats WHERE player_id = %s", (player_id,))
    stats = cur.fetchone()
    cur.execute("SELECT full_name FROM players WHERE player_id = %s", (player_id,))
    player = cur.fetchone()
    conn.close()
    return render_template('fielding_stats.html', stats=stats, player_name=player['full_name'])

@app.route('/wicketkeeping/<player_id>')
def wicketkeeping_stats(player_id):
    conn = connect()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM wicketkeeping_stats WHERE player_id = %s", (player_id,))
    stats = cur.fetchone()

    cur.execute("SELECT full_name FROM players WHERE player_id = %s", (player_id,))
    player = cur.fetchone()

    conn.close()
    return render_template('wicketkeeping_stats.html', stats=stats, player_name=player['full_name'])


@app.route('/captaincy/<player_id>')
def captaincy_stats(player_id):
    conn = connect()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM captaincy_stats WHERE player_id = %s", (player_id,))
    captaincy = cur.fetchone()
    cur.execute("SELECT full_name FROM players WHERE player_id = %s", (player_id,))
    player = cur.fetchone()
    conn.close()
    return render_template('captaincy_stats.html', captaincy=captaincy, player_name=player['full_name'])

@app.route('/add', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        data = request.form.to_dict()
        conn = connect()
        cur = conn.cursor()

        try:
            cur.execute('''INSERT INTO players VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', (
                data['player_id'], data['full_name'], data['birthdate'], data.get('deathdate') or None,
                data['current_age'], data['bats'], data['bowls'], data['matches'], data['teams']
            ))

            cur.execute('''INSERT INTO batting_stats VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (
                data['player_id'], data['innings'], data['not_outs'], data['aggregate_runs'],
                data['highest_score'], data['batting_average'], data['fifties'], data['hundreds'],
                data['double_hundreds'], data['triple_hundreds'], data['ducks'], data['pairs'],
                data['fours'], data['sixes'], data['balls_faced'], data['scoring_rate'],
                data['opened_batting'], data['top_scored_in_innings'], data['percent_team_runs']
            ))

            cur.execute('''INSERT INTO bowling_stats VALUES (%s, %s, %s, %s, %s, %s, %s)''', (
                data['player_id'], data['balls_bowled'], data['maidens'], data['runs_conceded'],
                data['wickets'], data['economy_rate'], data['best_innings']
            ))

            cur.execute('''INSERT INTO fielding_stats VALUES (%s, %s, %s, %s)''', (
                data['player_id'], data['catches'], data['most_catches_innings'], data['most_catches_in_match']
            ))

            cur.execute('''INSERT INTO captaincy_stats VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (
                data['player_id'], data['captaincy_matches'], data['captaincy_won'], data['captaincy_lost'],
                data['tosses_won'], data['chose_to_field'], data['field_won'], data['field_lost'],
                data['runs_as_captain'], data['batting_avg_as_captain']
            ))

            conn.commit()
        except Exception as e:
            conn.rollback()
            return f"Error while adding player: {e}"
        finally:
            conn.close()

        return redirect(url_for('home'))

    return render_template('add_player.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    conn = connect()
    cur = conn.cursor(dictionary=True)

    player = None
    searched = False

    if request.method == 'POST':
        name = request.form.get('search_name')
        searched = True
        cur.execute("SELECT * FROM players WHERE full_name LIKE %s", ('%' + name + '%',))
        player = cur.fetchone()

    conn.close()
    return render_template('search_player.html', player=player, searched=searched)

# -------------------------
# ✅ Route to Auto-Update Player Ages
# -------------------------
@app.route('/update_ages')
def update_ages():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT player_id, birthdate, deathdate FROM players")
    players = cur.fetchall()

    def calculate_age(birthdate, end_date):
        age_days = (end_date - birthdate).days
        years = age_days // 365
        days = age_days % 365
        return f"{years} years {days} days"

    for player_id, birthdate, deathdate in players:
        birthdate = birthdate if isinstance(birthdate, date) else datetime.strptime(str(birthdate), "%Y-%m-%d").date()
        end_date = date.today() if not deathdate else datetime.strptime(str(deathdate), "%Y-%m-%d").date()
        current_age = calculate_age(birthdate, end_date)

        cur.execute("UPDATE players SET current_age = %s WHERE player_id = %s", (current_age, player_id))

    conn.commit()
    conn.close()
    return "✅ All player ages have been updated!"

if __name__ == '__main__':
    app.run(debug=True)
