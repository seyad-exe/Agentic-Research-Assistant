# ingest.py
from agno.knowledge.reader.arxiv_reader import ArxivReader
from config import knowledge_base

def ingest_data():
    print("--- Starting Ingestion ---")

    # OPTION 1: Specific Topics (Prevents broad duplicates)
    # Instead of just "Machine Learning", use specific sub-fields or years.
    topics = [
        "Machine Learning 2024"
    ]

    for topic in topics:
        print(f"Fetching papers for: {topic}")
        knowledge_base.add_content(
            reader=ArxivReader(
                query=topic,
                max_results=5
            )
        )
        print(f"  - Added 5 papers for {topic}")

    # OPTION 2: Fetch by "Submitted Date" (Get the newest papers)
    # This helps ensure you get new content rather than the same "most relevant" ones.
    # Note: You might need to check if 'sort_by' is supported by your specific ArxivReader version,
    # but generally, changing the query string is the safest way to vary results.
    
    print("--- Ingestion Complete ---")
    print("Your Vector DB has been updated.")

if __name__ == "__main__":
    ingest_data()