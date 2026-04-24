# SportRadar Tennis Data Pipeline & SQL Analytics

This project is an end-to-end data engineering and analytics pipeline designed to extract, clean, structure, and analyze live tennis data from the Sportradar API.

The project is divided into three main phases. **Phase 1 (Data Engineering)** is currently complete. **Phase 2 (SQL Analytics)** and **Phase 3 (Streamlit Dashboard)** are the next steps.

---

## 📂 Phase 1: Data Engineering (Completed)
The python-based extraction and cleaning pipeline is fully operational. 

### What has been done:
1. **API Fetching:** The script connects to the SportRadar Tennis API v3 using a valid API key, respecting rate limits, to fetch live data from three endpoints (`competitions`, `complexes`, `double_competitors_rankings`).
2. **Raw Storage:** The highly nested JSON responses are backed up into the `data/raw_data/` directory.
3. **Data Flattening:** The pipeline parses the nested JSON (dictionaries within arrays) and flattens them into clean, relational Pandas DataFrames.
4. **Data Type Enforcement:** Numeric ranking metrics (points, rank, movement) are strictly cast to `int64` integers. Missing values are safely handled to ensure SQL compatibility.
5. **CSV Export:** The cleaned DataFrames are exported as 6 relational `.csv` files directly into the `data/processed_data/` folder.

### Project Structure
- `Tennis_Data_Pipeline.ipynb`: The main Jupyter Notebook containing the extraction, cleaning, and export logic.
- `Implementation_Plan.pdf`: A detailed architectural breakdown of how the pipeline works.
- `data/raw_data/`: Contains the backup JSON API responses (`live_competitions.json`, etc.).
- `data/processed_data/`: **(IMPORTANT)** Contains the 6 perfectly cleaned CSV files ready for SQL ingestion:
  - `categories.csv`
  - `competitions.csv`
  - `complexes.csv`
  - `venues.csv`
  - `competitors.csv`
  - `rankings.csv`

---

## 🛠️ Phase 2: SQL Analytics (Next Steps)

If you are taking over to build the SQL Connection & Analysis part, **you do not need to run the Python API script.** The data is already cleaned and waiting for you in `data/processed_data/`.

### How you should proceed:

1. **Database Setup:**
   - Create a new database in your preferred RDBMS (e.g., PostgreSQL, MySQL, SQL Server).
   
2. **Table Creation & Schema Design:**
   - Review the 6 `.csv` files in `data/processed_data/`.
   - Write `CREATE TABLE` scripts for each file. 
   - **Key Tip:** Use the string-based IDs (like `sr:competition:123`) as your Primary Keys (VARCHAR). Ensure foreign key relationships are established (e.g., linking `category_id` in the `competitions` table to the `categories` table).

3. **Data Ingestion:**
   - Bulk insert the CSV files into your newly created SQL tables. You can use the `COPY` command in Postgres, SQL Server Management Studio's Import Flat File wizard, or a Python script using `SQLAlchemy`.
   - *Note: There are zero duplicate rows in the CSVs, and missing strings are designed to safely become `NULL`.*

4. **Analytics & Querying:**
   - Once the tables are populated and relationships are defined, you can begin writing analytical queries (e.g., finding the complexes with the most venues, or ranking the competitors by total points).

### Running the Pipeline Manually (Optional)
If you ever need to refresh the live data:
1. Ensure `pandas` and `requests` are installed.
2. Open `Tennis_Data_Pipeline.ipynb`.
3. Add your active SportRadar API key in the configuration block.
4. Click **"Run All Cells"**. The new CSVs will automatically overwrite the old ones in `data/processed_data/`.

---

## 📊 Phase 3: Streamlit Dashboard (Future Step)

After the SQL Analytics phase is complete and the queries are generating meaningful insights, the final phase will involve building an interactive web dashboard.
- We will use **Streamlit** (Python) to connect directly to the SQL database.
- The dashboard will visualize the live rankings, tournament metrics, and venue data interactively for end users.
