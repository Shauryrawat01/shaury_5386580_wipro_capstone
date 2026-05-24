import os
from openpyxl import load_workbook
from utilities.logger import setup_logger

logger = setup_logger("ExcelReader")

def get_test_data():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(
        current_dir,
        "..",
        "test_data",
        "search_data.xlsx"
    )

    logger.info(f"Loading test data from: {file_path}")
    try:
        workbook = load_workbook(file_path)
        sheet = workbook.active

        data = {
            "mobile_number": sheet["A2"].value,
            "location": sheet["B2"].value
        }
        logger.info(f"Successfully loaded test data: {data}")
        return data
    except Exception as e:
        logger.error(f"Failed to load test data: {str(e)}")
        raise e
