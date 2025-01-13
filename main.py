"""Application for fetching details from a given Google Spreadsheet.

This FastAPI application allows users to fetch details from a Google Spreadsheet 
based on optional filters such as location, department, and employee name.
"""

from fastapi import FastAPI
from sheet_router import router

# Initialize FastAPI app
app = FastAPI(title="Evaluators")

app.include_router(router)

# Run the application using uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
