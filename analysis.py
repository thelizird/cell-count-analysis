import sqlite3
import pandas as pd



def part2_frequency(conn):
    df = pd.read_sql("SELECT * FROM samples", conn)

    df['total_count'] = df['b_cell'] + df['cd8_t_cell'] + df['cd4_t_cell'] + df['nk_cell'] + df['monocyte']

    melted = df.melt(id_vars=['sample_id','total_count'], value_vars=['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte'], var_name='population', value_name='count')

    melted['percentage'] = melted['count'] / melted['total_count'] * 100

    print(melted.head())

if __name__ == "__main__":
    conn = sqlite3.connect('cell_data.db')
    freq_df = part2_frequency(conn)
    conn.close()