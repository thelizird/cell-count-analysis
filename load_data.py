import sqlite3
import csv

conn = sqlite3.connect('cell_data.db')
cursor = conn.cursor()
cursor.execute('PRAGMA foreign_keys = ON')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        project_id TEXT PRIMARY KEY
        )
''')
cursor.execute('''

    CREATE TABLE IF NOT EXISTS subjects (
        subject_id TEXT PRIMARY KEY,
        project_id TEXT,
        condition TEXT,
        age INTEGER,
        sex TEXT,
        treatment TEXT,
        response TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS samples (
        sample_id TEXT PRIMARY KEY,
        subject_id TEXT,
        sample_type TEXT,
        time_from_treatment_start INTEGER,
        b_cell INTEGER,
        cd8_t_cell INTEGER,
        cd4_t_cell INTEGER,
        nk_cell INTEGER,
        monocyte INTEGER,
        FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
    )
''')


with open('cell-count.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute('''
            INSERT OR REPLACE INTO projects (project_id) VALUES (?)
        ''', (row['project'],))

        cursor.execute('''
            INSERT OR REPLACE INTO subjects (subject_id, project_id, condition, age, sex, treatment, response) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (row['subject'], row['project'], row['condition'], row['age'], row['sex'], row['treatment'], row['response']))

        cursor.execute('''
            INSERT OR REPLACE INTO samples (sample_id, subject_id, sample_type, time_from_treatment_start, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row['sample'], row['subject'], row['sample_type'], row['time_from_treatment_start'], row['b_cell'], row['cd8_t_cell'], row['cd4_t_cell'], row['nk_cell'], row['monocyte']))

conn.commit()
conn.close()