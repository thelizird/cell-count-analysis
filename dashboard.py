import streamlit as st
import sqlite3
import pandas as pd

st.title('Cell Count Analysis Dashboard')

conn = sqlite3.connect('cell_data.db')

tab1, tab2, tab3 = st.tabs(['Cell Frequencies', 'Statistical Analysis', 'Subset Analysis'])

with tab1:
    st.header('Cell Frequencies')
    freq_df = pd.read_sql('SELECT * FROM cell_frequencies', conn)
    st.dataframe(freq_df)

with tab2:
    st.header('Responders vs Non-Responders')
    st.image('responders_vs_non_responders.png')
    stats_df = pd.read_sql('SELECT * FROM statistical_results', conn)
    st.dataframe(stats_df)
    st.write("Among melonoma patients treated with miraclib, CD4 T cells show a significant difference between responders and non-responders (p=0.013) This suggests that CD4 T cell levels may help predict treament response")

with tab3:
    st.header('Baseline Subset Analysis')
    subset_df = pd.read_sql('SELECT * FROM part4_baseline', conn)

    st.subheader('Samples per Project')
    st.dataframe(subset_df.groupby('project_id')['sample_id'].count().reset_index(name='count'))

    st.subheader('Responders vs Non-Responders')
    st.dataframe(subset_df.groupby('response')['subject_id'].nunique().reset_index(name='count'))

    st.subheader('Males vs Females')
    st.dataframe(subset_df.groupby('sex')['subject_id'].nunique().reset_index(name='count'))
    

conn.close()