
## Running the application

Three terminals, in order.

**1. Bring Azure AI Search up** (it is torn down between sessions to control cost):

    . .\env.ps1
    .\infra\search-up.ps1

Wait for `"Status": "running"`, then build the index:

    python -m backend.search.index_schema
    python -m backend.search.indexer

Expect `Index now contains 104 documents.`

**2. Start the API:**

    .\.venv\Scripts\Activate.ps1
    uvicorn api.main:app --reload --port 8000

Interactive API documentation at http://localhost:8000/docs

**3. Open the web interface:**

    Start-Process .\web\index.html

The frontend calls the API at `http://localhost:8000`. If the API is not running,
each screen falls back to mock data and logs `[API Notice]` to the browser console.

**Alternative interface.** A Streamlit version of the same nine screens is at
`frontend/app.py`. It calls the backend modules directly rather than through the API:

    streamlit run frontend/app.py

**Tear down when finished.** Azure AI Search is the only hourly-billed resource:

    .\infra\search-down.ps1
