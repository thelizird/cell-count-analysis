import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def part2_frequency(conn):
    df = pd.read_sql("SELECT * FROM samples", conn)

    df['total_count'] = df['b_cell'] + df['cd8_t_cell'] + df['cd4_t_cell'] + df['nk_cell'] + df['monocyte']

    melted = df.melt(id_vars=['sample_id','total_count'], value_vars=['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte'], var_name='population', value_name='count')

    melted['percentage'] = melted['count'] / melted['total_count'] * 100

    print(melted.head())
    melted.to_sql('cell_frequencies', conn, if_exists='replace', index=False)
    return melted

def part3_statistics(conn):
    query = '''
        SELECT cf.*, s.sample_type, sub.condition, sub.treatment, sub.response
        FROM cell_frequencies cf
        JOIN samples s ON cf.sample_id = s.sample_id
        JOIN subjects sub ON s.subject_id = sub.subject_id
        WHERE sub.condition = 'melanoma'
        AND sub.treatment = 'miraclib'
        AND s.sample_type = 'PBMC'
    '''
    df = pd.read_sql(query, conn)
    sns.boxplot(x='population', y='percentage', hue='response', data=df)
    plt.title('Responders vs Non-Responders')
    plt.savefig('responders_vs_non_responders.png')
    plt.close()

    from scipy import stats
    populations = df['population'].unique()
    results = []
    for pop in populations:
        pop_data = df[df['population'] == pop]
        responders = pop_data[pop_data['response'] == 'yes']['percentage']
        non_responders = pop_data[pop_data['response'] == 'no']['percentage']
        stat, p_value = stats.mannwhitneyu(responders, non_responders)
        results.append({
            'population': pop,
            'statistic': stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        })
    results_df = pd.DataFrame(results)
    print(results_df)
    results_df.to_sql('statistical_results', conn, if_exists='replace', index=False)

def part4_subset(conn):
    query = '''
        SELECT s.*, sub.project_id, sub.condition, sub.sex, sub.treatment, sub.response
        FROM samples s
        JOIN subjects sub ON s.subject_id = sub.subject_id
        WHERE sub.condition = 'melanoma'
        AND sub.treatment = 'miraclib'
        AND s.sample_type = 'PBMC'
        AND s.time_from_treatment_start = 0
    '''
    df = pd.read_sql(query, conn)
    print(df.groupby('project_id')['sample_id'].count())
    print(df.groupby('response')['subject_id'].nunique())
    print(df.groupby('sex')['subject_id'].nunique())

    df.to_sql('part4_baseline', conn, if_exists='replace', index=False)

if __name__ == "__main__":
    conn = sqlite3.connect('cell_data.db')
    freq_df = part2_frequency(conn)
    part3_statistics(conn)
    part4_subset(conn)
    conn.close()