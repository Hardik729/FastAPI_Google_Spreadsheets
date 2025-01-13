from fastapi import Query, APIRouter
from typing import Optional, Dict, Any, List, Union
import gspread
from google_authentication import authenticate_user

router = APIRouter(prefix="/gsheets", tags=["Google Sheets"])

# Authenticate the user
gc: gspread.Client = authenticate_user()


@router.get("/fetch-data/", response_model=Union[Dict[str, Any], Dict[str, List[Dict[str, Any]]]])
async def fetch_data(
    sheet_name: str = Query(..., description="Name of the sheet to fetch data from"),
    location: Optional[str] = Query(None, description="Filter by location"),
    department: Optional[str] = Query(None, description="Filter by department"),
    employee_name: Optional[str] = Query(None, description="Filter by employee name"),
) -> Union[Dict[str, Any], Dict[str, List[Dict[str, Any]]]]:
    """Fetch details from a Google Spreadsheet.

    This endpoint fetches all rows from the specified sheet in the Google Spreadsheet.
    Users can optionally filter the results by providing `location`, `department`,
    and/or `employee_name` as query parameters.

    Args:
        sheet_name (str): Name of the sheet to fetch data from.
        location (Optional[str]): Optional filter for the location column.
        department (Optional[str]): Optional filter for the department column.
        employee_name (Optional[str]): Optional filter for the employee name column.

    Returns:
        Union[Dict[str, Any], Dict[str, List[Dict[str, Any]]]]: A dictionary containing
        either an error message or a list of filtered records.
    """
    # Open the spreadsheet
    try:
        spreadsheet = gc.open("Employee_Database")
    except gspread.exceptions.SpreadsheetNotFound:
        return {"error": "Spreadsheet not found. Please check the name and try again."}

    # Select the specified sheet
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        return {"error": f"Sheet '{sheet_name}' not found in the spreadsheet."}

    # Fetch all records using the built-in `get_all_records` method
    records: List[Dict[str, Any]] = worksheet.get_all_records()

    # Filter dynamically based on input
    filters: Dict[str, Optional[str]] = {
        "Location": location,
        "Department": department,
        "Employee Details": employee_name,
    }

    filtered_records: List[Dict[str, Any]] = [
        record
        for record in records
        if all(
            value is None or str(value).strip().lower() in str(record.get(key, "")).strip().lower()
            for key, value in filters.items()
        )
    ]


    return {"records": filtered_records}
