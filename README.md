## How to run

1. `make setup` installs all dependencies
2. `make pipeline` builds the database and runs the full analysis

The dashboard is deployed [here](#dashboard). To run it locally instead, use `make dashboard` to start the Streamlit server on localhost:8501.

## Database Schema
The data is organized into three normalized tables

- Projects (unique project ids)
- Subjects (patient level data (condition, age, sex, treatment, response), linked to a project via foreign key)
- Samples (individual biological samples with cell counts, linked to a subject via foreign key)

I went with this design because each row in the original CSV mixes project, patient, and sample data together. Normalizing into three tables eliminates redundancy. That way, for example, a subject's age and treatment aren't repeated across every one of the samples. 

For the analysis, we could have gone away with two tables: just subjects and samples, but to prepare for scaling with hundreds of projects and thousands of samples, I decided to do the projects table early on, even though there were only three. This schema keeps queries efficient. It can allow us to easily add new data types, like a treatments table, new cell populations, or other metadata. We can easily add tables or columns rather than restructuring existing ones. Indexing the foreign keys would keep JOINS fast as data grows.

## Code Structure

This project is split into three files. 

- `load_data.py`
This creates the SQLite database schema and loads cell-count.csv into the normalized tables. This is the only file that touches the raw CSV. 

- `analysis.py` 
Since the nature of the problem required different analysis, I split each part of the code into functions. We read from the database and then go into the different functions part 2 which computes the cell population frequencies, part 3, which runs the statistical comparisons between responders and non-responders, part 4, which queries the baseline subset data.
All of these results are written back to the database to easily be retrieved by the Streamlit dashboard

- `dashboard.py`
This is the Streamlit app that reads the computed results from the database and displays them across three tabs. 

### Why this structure
The database acts as the interface between stages. load_data.py writes raw data in, analysis.py reads it and writes results back, and the dashboard only reads. This means each step can run independently, and the dashboard doesn't need to recompute anything. It just displays what's already in the database. 

## Dashboard
https://cell-count-analysis-4tsrew7nmiahfggejgsro7.streamlit.app/
