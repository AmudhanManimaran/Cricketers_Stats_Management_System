import csv
from db import connect, init_db

# Initialize DB (create tables if not exist)
init_db()

def load_players_from_csv(path):
    conn = connect()
    cur = conn.cursor()

    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Insert into players
            cur.execute('''INSERT OR REPLACE INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (
                row['player_id'], row['full_name'], row['birthdate'], row['current_age'],
                row['bats'], row['bowls'], row['matches'], row['teams']
            ))

            # Insert into batting_stats
            cur.execute('''INSERT OR REPLACE INTO batting_stats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                row['player_id'], row['innings'], row['not_outs'], row['aggregate_runs'],
                row['highest_score'], row['batting_average'], row['fifties'], row['hundreds'],
                row['double_hundreds'], row['triple_hundreds'], row['ducks'], row['pairs'],
                row['fours'], row['sixes'], row['balls_faced'], row['scoring_rate'],
                row['opened_batting'], row['top_scored_in_innings'], row['percent_team_runs']
            ))

            # Insert into bowling_stats
            cur.execute('''INSERT OR REPLACE INTO bowling_stats VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (
                row['player_id'], row['balls_bowled'], row['maidens'], row['runs_conceded'],
                row['wickets'], row['economy_rate'], row['best_innings'], row['best_match']
            ))

            # Insert into fielding_stats
            cur.execute('''INSERT OR REPLACE INTO fielding_stats VALUES (?, ?, ?, ?)''', (
                row['player_id'], row['catches'], row['most_catches_in_innings'], row['most_catches_in_match']
            ))

            # Insert into captaincy_stats
            cur.execute('''INSERT OR REPLACE INTO captaincy_stats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                row['player_id'], row['captaincy_matches'], row['captaincy_won'], row['captaincy_lost'],
                row['tosses_won'], row['chose_to_field'], row['field_won'], row['field_lost'],
                row['runs_as_captain'], row['batting_avg_as_captain']
            ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    load_players_from_csv("data/players.csv")
    print("Players loaded into the database successfully.")
