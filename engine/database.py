import sqlite3
import os
from typing import List, Tuple, Optional

# path to db
DB_PATH = os.path.join('database', 'data.db')

def init_db() -> sqlite3.Connection:
    # create db folder if it doesn't exist
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # create connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # create scores table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    return conn

def add_score(player_name: str, score: int) -> None:
    # add new score to db
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO scores (player_name, score) VALUES (?, ?)',
        (player_name, score)
    )
    
    conn.commit()
    conn.close()

def get_all_scores() -> List[Tuple]:
    # get all scores
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM scores ORDER BY score DESC')
    scores = cursor.fetchall()
    
    conn.close()
    return scores

def get_leaderboard() -> List[Tuple]:
    # get cumulative scores for all 4 players
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            player_name,
            COALESCE(SUM(score), 0) as total_score,
            COUNT(*) as games_played
        FROM scores 
        WHERE player_name IN ('1', '2', '3', '4')
        GROUP BY player_name
        ORDER BY total_score DESC
    ''')
    scores = cursor.fetchall()
    
    # Ensure all 4 players are in the result, even if they have no scores
    player_scores = {str(i): (0, 0) for i in range(1, 5)}  # (total_score, games_played)
    for player_name, total_score, games_played in scores:
        player_scores[player_name] = (total_score, games_played)
    
    # Convert to list of tuples with player_id, total_score, games_played
    result = [(int(player_id), total_score, games_played) 
              for player_id, (total_score, games_played) in player_scores.items()]
    
    conn.close()
    return result

def get_player_scores(player_name: str) -> List[Tuple]:
    # get player scores
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute(
        'SELECT * FROM scores WHERE player_name = ? ORDER BY score DESC',
        (player_name,)
    )
    scores = cursor.fetchall()
    
    conn.close()
    return scores

def update_score(score_id: int, new_score: int) -> bool:
    # update score
    conn = init_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            'UPDATE scores SET score = ? WHERE id = ?',
            (new_score, score_id)
        )
        conn.commit()
        success = cursor.rowcount > 0
    except sqlite3.Error:
        success = False
    
    conn.close()
    return success

def delete_score(score_id: int) -> bool:
    # delete score
    conn = init_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM scores WHERE id = ?', (score_id,))
        conn.commit()
        success = cursor.rowcount > 0
    except sqlite3.Error:
        success = False
    
    conn.close()
    return success

def get_player_best_score(player_name: str) -> Optional[int]:
    # get player best score
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute(
        'SELECT MAX(score) FROM scores WHERE player_name = ?',
        (player_name,)
    )
    result = cursor.fetchone()
    
    conn.close()
    return result[0] if result and result[0] is not None else None

def delete_all_scores() -> bool:
    # delete all scores
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM scores')
    conn.commit()
