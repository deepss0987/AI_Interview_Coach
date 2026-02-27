import sqlite3
import json
from datetime import datetime

DB_PATH = "database/interview_coach.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interview_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            feedback TEXT NOT NULL,
            FOREIGN KEY (interview_id) REFERENCES interviews (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def save_interview(results):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO interviews (date) VALUES (?)', (date_str,))
    interview_id = cursor.lastrowid
    
    for item in results:
        cursor.execute('''
            INSERT INTO responses (interview_id, question, answer, feedback)
            VALUES (?, ?, ?, ?)
        ''', (
            interview_id,
            item['question'],
            item['answer'],
            json.dumps(item['feedback'])
        ))
        
    conn.commit()
    conn.close()
    return interview_id

def get_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    interviews = cursor.execute('SELECT * FROM interviews ORDER BY id DESC').fetchall()
    
    history = []
    for interview in interviews:
        responses = cursor.execute('''
            SELECT * FROM responses WHERE interview_id = ?
        ''', (interview['id'],)).fetchall()
        
        history.append({
            "id": interview['id'],
            "date": interview['date'],
            "results": [
                {
                    "question": r['question'],
                    "answer": r['answer'],
                    "feedback": json.loads(r['feedback'])
                } for r in responses
            ]
        })
        
    conn.close()
    return history
