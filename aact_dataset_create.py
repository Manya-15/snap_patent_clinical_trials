import duckdb
import os
import glob
import time

# --- Configuration ---
# Set the path to the folder containing your AACT .txt files
AACT_FOLDER = "E:/ML SELF CODES/snaplife/patent_clinical_trial/AACT_clinical_patent" 
# Set the name for your database file
DB_FILE = "aact.duckdb"

# --- Main Script ---
def create_aact_database():
    """
    Scans a directory for pipe-delimited .txt files and loads each one
    as a table into a new DuckDB database.
    """
    # Find all .txt files in the specified directory
    txt_files = glob.glob(os.path.join(AACT_FOLDER, '*.txt'))
    
    if not txt_files:
        print(f"❌ Error: No .txt files found in the directory '{AACT_FOLDER}'.")
        print("Please make sure you have unzipped the AACT dataset into that folder.")
        return

    # Remove the old database file if it exists to start fresh
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Removed existing database file: {DB_FILE}")

    # Connect to the DuckDB database file (it will be created)
    con = duckdb.connect(database=DB_FILE, read_only=False)
    print(f"🚀 Started creating DuckDB database at '{DB_FILE}'...")
    start_time = time.time()

    # Loop through each file and create a table from it
    for i, file_path in enumerate(txt_files):
        # Extract the table name from the filename (e.g., "sponsors.txt" -> "sponsors")
        table_name = os.path.basename(file_path).replace('.txt', '')
        
        print(f"  ({i+1}/{len(txt_files)}) Loading table '{table_name}'...")

        # DuckDB's read_csv_auto is powerful. It will automatically detect
        # columns, types, delimiter, and header from the file.
        # We then create a table in the database from this file.
        query = f"""
    CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto(
        '{file_path}', 
        delim='|', 
        header=True, 
        all_varchar=True,
        ignore_errors=True  -- This is the line you add
    );
"""
        con.execute(query)

    end_time = time.time()
    print("\n✅ Success! All tables have been loaded into the database.")
    print(f"Total time taken: {end_time - start_time:.2f} seconds.")
    
    # Close the database connection
    con.close()

if __name__ == "__main__":
    create_aact_database()