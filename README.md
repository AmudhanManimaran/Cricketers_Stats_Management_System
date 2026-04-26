# Cricketers Stats Management System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-black?style=flat-square&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?style=flat-square&logo=mysql)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

> A Flask + MySQL web application for managing and exploring cricket player statistics across 5 normalized tables — batting, bowling, fielding, wicketkeeping, and captaincy — with automated age computation, player search, and full CRUD operations.

---

## 🎯 Features

- **5 normalized stat tables** — batting, bowling, fielding, wicketkeeping, captaincy (per player)
- **Player search** — LIKE-based name search across all players
- **Player profile view** — full player info including DOB, teams, batting/bowling style
- **Stat drill-down** — dedicated pages for each stat category per player
- **Add player** — single form inserts into all 5 tables atomically with rollback on failure
- **Update player** — edit existing player records
- **Auto age computation** — calculates current age (or age at death) from birthdate in years + days
- **Bulk age update** — `/update_ages` route recalculates all player ages in one call
- **CSV data loader** — `init_data.py` bulk-inserts players from a CSV file

---

## 🏗️ System Architecture

```
Browser
   │
   ▼
Flask App (app.py)
   │
   ├── / (Home + Search)
   ├── /player/<id>      → Player Profile
   ├── /batting/<id>     → Batting Stats
   ├── /bowling/<id>     → Bowling Stats
   ├── /fielding/<id>    → Fielding Stats
   ├── /wicketkeeping/<id> → Wicketkeeping Stats
   ├── /captaincy/<id>   → Captaincy Stats
   ├── /add              → Add Player (5-table atomic insert)
   ├── /search           → Search Player
   └── /update_ages      → Bulk Age Recalculation
         │
         ▼
     db.py (MySQL Connector)
         │
         ▼
MySQL: test_wicket
   ├── players
   ├── batting_stats
   ├── bowling_stats
   ├── fielding_stats
   ├── wicketkeeping_stats
   └── captaincy_stats
```

---

## 🗃️ Database Schema

### players
| Column | Type | Description |
|--------|------|-------------|
| player_id | VARCHAR | Primary key |
| full_name | VARCHAR | Player full name |
| birthdate | DATE | Date of birth |
| deathdate | DATE | Date of death (NULL if alive) |
| current_age | VARCHAR | Auto-computed: "X years Y days" |
| bats | VARCHAR | Batting style |
| bowls | VARCHAR | Bowling style |
| matches | INT | Total matches played |
| teams | VARCHAR | Teams represented |

### batting_stats
19 columns including: innings, not_outs, aggregate_runs, highest_score, batting_average, fifties, hundreds, double_hundreds, triple_hundreds, ducks, pairs, fours, sixes, balls_faced, scoring_rate, opened_batting, top_scored_in_innings, percent_team_runs

### bowling_stats
7 columns: balls_bowled, maidens, runs_conceded, wickets, economy_rate, best_innings

### fielding_stats
4 columns: catches, most_catches_innings, most_catches_in_match

### wicketkeeping_stats
Per wicketkeeper stats

### captaincy_stats
10 columns: captaincy_matches, captaincy_won, captaincy_lost, tosses_won, chose_to_field, field_won, field_lost, runs_as_captain, batting_avg_as_captain

---

## 📁 Project Structure

```
Cricketers-Stats-Management-System/
│
├── cricket-player-stats/
│   ├── app.py                      # Flask routes + age computation
│   ├── db.py                       # MySQL connection + age utility
│   ├── init_data.py                # CSV bulk data loader
│   │
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/
│   │       ├── script.js
│   │       └── profile.js
│   │
│   └── templates/
│       ├── base.html
│       ├── index.html              # Home + search
│       ├── player_profile.html     # Player overview
│       ├── batting_stats.html
│       ├── bowling_stats.html
│       ├── fielding_stats.html
│       ├── wicketkeeping_stats.html
│       ├── captaincy_stats.html
│       ├── add_player.html
│       ├── search_player.html
│       ├── update_player.html
│       └── all_players.html
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/AmudhanManimaran/Cricketers-Stats-Management-System.git
cd Cricketers-Stats-Management-System/cricket-player-stats
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up MySQL Database
Create the database and tables in MySQL:
```sql
CREATE DATABASE test_wicket;
USE test_wicket;
-- Run the table creation statements from db.py
```

### 5. Configure Database Credentials
Open `db.py` and update your MySQL credentials:
```python
return mysql.connector.connect(
    host='localhost',
    user='root',
    password='YOUR_PASSWORD',
    database='test_wicket'
)
```

### 6. Run the Application
```bash
python app.py
```
Visit `http://localhost:5000` in your browser.

---

## 🚀 Usage

- **Home** — lists all players, search by name
- **Player Profile** — click any player to view full profile
- **Stat Pages** — navigate to batting / bowling / fielding / wicketkeeping / captaincy stats
- **Add Player** — `/add` — fill the form to insert a new player across all 5 tables atomically
- **Update Ages** — visit `/update_ages` to recalculate all player ages from birthdate

---

## 📦 Requirements

```
flask>=2.0.0
flask-cors>=3.0.0
mysql-connector-python>=8.0.0
```

---

## ⚠️ Known Limitations

- Database credentials are hardcoded in `db.py` — update before deployment
- `init_data.py` uses SQLite-style `?` placeholders — incompatible with the MySQL connector used in `app.py` (uses `%s`). Use `app.py` routes to add players instead.

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Amudhan Manimaran**
- 🌐 Portfolio: [amudhanmanimaran.github.io/Portfolio](https://amudhanmanimaran.github.io/Portfolio/)
- 💼 LinkedIn: [linkedin.com/in/amudhan-manimaran-3621bb32a](https://www.linkedin.com/in/amudhan-manimaran-3621bb32a)
- 🐙 GitHub: [github.com/AmudhanManimaran](https://github.com/AmudhanManimaran)
