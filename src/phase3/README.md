## Additional Run
We have used Pseudo Relevance Feedback for query enrichment along with stopping to update the existing queries.
We then used BM25 to performed the additional run.

#### `inverted_indexer.py`
1. Please ensure that that the results generated in Phase1-Task1 for Lucene run are generated in the folder 
`src/phase1/task1/lucene_results`.
2. Make sure all the imports are installed that are used in the file.
 

#### `queryexpansion_stopping.py`
1. Please create an empty text file named `expanded_queries.txt` to store the expanded queries.
2. Please create an intermediate folder named `inverted_indexes` to store the top files for each query further used for
 Pseudo Relevance Feedback. 
3. Make sure all the imports are installed that are used in the file.
4. The text file will be populated with the 64 queries in t he format `<query_id <expnaded_query>`.
5. This file uses `inverted_indexer.py` . So, please follow the instructions given above.
 
 
#### `AdditionalRun.py`
1. Please create a folder named `Additional_results` to store the results.
2. Make sure all the imports are installed that are used in the file.
3. The folder will be populated with top 100 results for the 64 queries.
