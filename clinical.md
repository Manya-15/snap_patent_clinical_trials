# Patent and Clinical Trial Matching & Clinical Trial search

Tools to link patents from Lens.org with relevant clinical trials from the AACT (Aggregate Analysis of ClinicalTrials.gov) database. It uses patent metadata to find potential sponsors and then matches them against clinical trial data, ranking the results based on semantic similarity.

## Core Components

The project is divided into two main functionalities:

1.  **`clinical_matching.ipynb`**: Matches a specific patent (identified by a Lens.org ID) to clinical trials.
2.  **`clinical_trials_search.ipynb`**: Provides a general-purpose search engine for the AACT clinical trials database.

### Dataset

-   **Source**: AACT (Aggregate Analysis of ClinicalTrials.gov)
-   **Database File**: `aact.duckdb`
-   **Creation**: The DuckDB database is created using the script `aact_dataset_create.py`.
-   **Schema**: The structure and description of the tables in the database are detailed in `aact_tables.xlsx`.

---

## 1. `clinical_matching.ipynb` - Patent to Clinical Trial Matching

This notebook takes a patent's Lens.org ID, fetches its metadata, identifies the patent's owners/applicants, and then searches the AACT database for clinical trials sponsored by those entities. The results are ranked by semantic similarity between the patent's text (title, abstract, claims) and the clinical trial's text.

### How it Works

1.  **Fetch Patent Data**:
    -   It first fetches basic patent metadata (title, abstract, owners) from **Lens.org** using the provided Lens ID.
    -   It then uses the patent's publication number to fetch more detailed information, including the full claims, from the **European Patent Office (EPO) OPS API**.

2.  **Find Sponsor Matches**:
    -   The patent's owner and applicant names are normalized (e.g., "Company Inc." becomes "company").
    -   A SQL query is run against the `aact.duckdb` database to find all clinical trials where the sponsor's name matches the patent's owners.

3.  **Rank by Semantic Similarity**:
    -   For each potential match, the notebook aggregates the full text of the patent (title, abstract, claims) and the full text of the clinical trial (titles, summaries, conditions, interventions).
    -   It uses the `all-MiniLM-L6-v2` sentence-transformer model to convert these texts into vector embeddings.
    -   The **cosine similarity** between the patent's embedding and each trial's embedding is calculated.
    -   The trials are then ranked from highest to lowest similarity score.

### How to Run

1.  **Prerequisites**:
    -   Ensure the `aact.duckdb` database file is in the same directory. If not, create it by running `aact_dataset_create.py`.
    -   Make sure you have valid EPO OPS API credentials (Consumer Key and Secret) in the script.

2.  **Modify Parameters**:
    -   Open `clinical_matching.ipynb`.
    -   In the final cell, change the `lens_id` variable to the Lens.org ID of the patent you want to analyze.
        ```python
        if __name__ == "__main__":
            lens_id = "023-587-103-542-962"  # <-- CHANGE THIS ID
            patent_info = get_patent_metadata(lens_id)
            # ...
        ```

3.  **Execute the Notebook**:
    -   Run all cells in the notebook.

### Output

-   The notebook will print the fetched patent metadata, a preview of the claims, and a list of matching clinical trials ranked by their semantic similarity score.
-   The final output file is a **CSV file** containing the ranked list of clinical trials, including their NCT ID and similarity score. The filename is generated dynamically based on the Lens ID.

---

## 2. `clinical_trials_search.ipynb` - Clinical Trials Search Engine

This notebook provides a powerful interface to search the AACT clinical trials database with various filters. It's a useful tool for exploring the dataset independently of patent matching.

### How it Works

1.  **Connect to Database**:
    -   It connects to the `aact.duckdb` database.

2.  **Comprehensive Search**:
    -   The `search_comprehensive` function builds a dynamic SQL query based on a search query and optional filters.
    -   It searches across multiple fields, including titles, interventions, conditions, and summaries.
    -   It allows filtering by study phase, status, study type, intervention type, start date, and enrollment size.

3.  **Analysis and Export**:
    -   The notebook can display a summary of the search results, including distributions of study phases and statuses.
    -   It can also export the full, detailed results for the found trials into a comprehensive CSV file.

### How to Run

1.  **Prerequisites**:
    -   Ensure the `aact.duckdb` database file is in the correct path as specified in the notebook.

2.  **Modify Parameters**:
    -   Open `clinical_trials_search.ipynb`.
    -   In the **fifth cell**, modify the `SEARCH_QUERY` variable and add any desired filters to the `search_clinical_trials` function call.
        ```python
        # Example Search - Modify this cell for your searches
        SEARCH_QUERY = "Alpha-2-macroglobulin"  # <-- CHANGE THIS

        results = search_clinical_trials(
            query=SEARCH_QUERY,
            phases=['PHASE 2', 'PHASE 3'],  # Optional filter
            statuses=['RECRUITING']         # Optional filter
        )
        ```

3.  **Execute the Notebook**:
    -   Run all cells to perform the search, view the summary, and save the results.

### Output

-   The notebook prints a summary of the search results and an analysis of the found trials.
-   The primary output is a **CSV file** containing the search results. The filename is generated dynamically based on the search query and timestamp (e.g., `comprehensive_Alpha_2_macroglobulin_trials_20250913_192702.csv`).
- Find the same in the `result_files` folder.
