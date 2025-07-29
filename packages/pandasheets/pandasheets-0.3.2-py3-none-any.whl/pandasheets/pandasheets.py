import pandas
import gspread
from gspread.exceptions import SpreadsheetNotFound, WorksheetNotFound, APIError
from pathlib import Path


class pandasheets:
    def __init__(
        self,
        credential: str | Path,
    ):
        """
        Initialize the Pandasheets client and validate the service-account credential.

        Args:
            credential: Path to your service-account JSON credentials file.

        Raises:
            FileNotFoundError: If the credential file is not found.
            ValueError: If authentication fails due to invalid credentials.
        """
        self._credential = Path(credential)
        if not self._credential.exists():
            raise FileNotFoundError(f"Credential file not found: {self._credential}")

        # Attempt to authenticate with Google Sheets
        try:
            self._client = gspread.service_account(filename=str(self._credential))
        except Exception as e:
            raise ValueError(f"Failed to authenticate with provided credential: {e}")

    def open_spreadsheet(self, spreadsheet: str) -> gspread.Spreadsheet:
        """
        Opens and returns a Google Spreadsheet.

        Args:
            spreadsheet (str): The name of the Google Spreadsheet to open.

        Returns:
            gspread.Spreadsheet: The opened Spreadsheet object, allowing further operations.

        Raises:
            gspread.exceptions.SpreadsheetNotFound: If the spreadsheet name is incorrect or inaccessible.
            FileNotFoundError: If the credential file is missing.
            ValueError: If authentication fails due to invalid credentials.
        """

        try:
            # Open and return the spreadsheet object
            return self._client.open(spreadsheet)

        except SpreadsheetNotFound:
            raise SpreadsheetNotFound(
                f"Spreadsheet '{spreadsheet}' not found or inaccessible."
            )

        except APIError as e:
            raise ValueError(
                f"Google API error when opening spreadsheet '{spreadsheet}': {e}"
            )

        except Exception as e:
            raise ValueError(f"An error occurred while opening the spreadsheet: {e}")

    def sheet_exists(self, sheet: str, spreadsheet: gspread.Spreadsheet) -> bool:
        """
        Checks if a worksheet exists in a given Google Spreadsheet.

        Args:
            spreadsheet (gspread.Spreadsheet): The Google Spreadsheet object.
            sheet (str): The name of the worksheet to check.

        Returns:
            bool: True if the worksheet exists, False otherwise.
        """
        try:
            spreadsheet.worksheet(sheet)
            return True
        except WorksheetNotFound:
            return False

    def get_sheet_to_dataframe(self, sheet: str, spreadsheet: str) -> pandas.DataFrame:
        """
        Retrieves data from a specific worksheet in a Google Spreadsheet and returns it as a pandas DataFrame.

        Args:
            sheet (str): The name of the worksheet to retrieve.
            spreadsheet (str): The name of the Google Spreadsheet to open.

        Returns:
            pandas.DataFrame: A DataFrame containing the worksheet data.

        Raises:
            gspread.exceptions.SpreadsheetNotFound: If the spreadsheet is incorrect or inaccessible.
            gspread.exceptions.WorksheetNotFound: If the worksheet name is incorrect.
            ValueError: If data retrieval fails.
        """

        # Open the spreadsheet
        spreadsheet_obj = self.open_spreadsheet(spreadsheet=spreadsheet)

        try:
            # Open the worksheet
            worksheet = spreadsheet_obj.worksheet(sheet)
        except WorksheetNotFound:
            raise WorksheetNotFound(
                f"Worksheet '{sheet}' not found in '{spreadsheet}'."
            )

        # Get all data from the worksheet
        data = worksheet.get_all_records()

        return pandas.DataFrame(data, index=None)

    def get_spreadsheet(
        self,
        spreadsheet: str,
    ) -> dict[str, pandas.DataFrame]:

        # Open the spreadsheet
        spreadsheet_obj = self.open_spreadsheet(spreadsheet=spreadsheet)

        spreadsheet_dict = {}
        for worksheet in spreadsheet_obj.worksheets():
            # Get all data from the sheet
            data = worksheet.get_all_records()

            # Convert to pandas.DataFrame
            df = pandas.DataFrame(data, index=None)

            spreadsheet_dict[worksheet.title] = df

        return spreadsheet_dict

    def upload_dataframe_to_spreadsheet(
        self,
        df: pandas.DataFrame,
        sheet: str,
        spreadsheet: str,
        formatting: bool = True,
        overwrite: bool = False,
    ) -> None:
        """
        Uploads a pandas DataFrame to a newly created formatted worksheet in a Google Spreadsheet.

        This function creates a new worksheet in the specified Google Spreadsheet and uploads the data
        from the provided DataFrame. If the DataFrame is empty, or if a worksheet with the specified name
        already exists, the function raises a ValueError. Optional formatting can be applied to the worksheet
        after data upload:
        - Bold formatting is applied to the header row.
        - All cells in columns A to Z are set to clip text wrapping.
        - The first row is frozen to keep the headers visible during scrolling.

        Args:
            df (pandas.DataFrame): The DataFrame to upload.
            sheet (str): The name of the worksheet to create and upload data to.
            spreadsheet (str): The name of the Google Spreadsheet to open.
            formatting (bool, optional): Whether to apply formatting to the worksheet after upload. Defaults to True.
            overwrite (bool, optional): Whether overwrite existing sheet. Defaults to False.

        Raises:
            ValueError: If the worksheet already exists or the DataFrame is empty.
            Exception: If an unexpected error occurs.

        Returns:
            None
        """
        # Ensure DataFrame is not empty
        if df.empty:
            raise ValueError(
                "Error: The DataFrame is empty. Cannot upload an empty worksheet."
            )

        # Open the spreadsheet
        spreadsheet_obj = self.open_spreadsheet(spreadsheet=spreadsheet)

        # Replace NaN values with an empty string
        df = df.fillna("")

        # Check if the worksheet already exists
        if self.sheet_exists(spreadsheet=spreadsheet_obj, sheet=sheet):

            if overwrite:
                # get the old worksheet
                old_worksheet = spreadsheet_obj.worksheet(sheet)
                # delet it
                spreadsheet_obj.del_worksheet(old_worksheet)
                # create a new one
                worksheet = spreadsheet_obj.add_worksheet(
                    title=sheet, rows=str(df.shape[0] + 1), cols=str(df.shape[1])
                )

            else:
                raise ValueError(
                    f"Error: Worksheet '{sheet}' already exists in '{spreadsheet}'."
                )

        else:
            # Create a new worksheet
            worksheet = spreadsheet_obj.add_worksheet(
                title=sheet, rows=str(df.shape[0] + 1), cols=str(df.shape[1])
            )

        # Convert DataFrame to list format
        data_to_write = [df.columns.values.tolist()] + df.values.tolist()

        # Write data to Google Sheets (starting from cell A1)
        worksheet.update(data_to_write, raw=False)

        if formatting:
            # Get the sheet ID for formatting
            sheet_id = worksheet._properties["sheetId"]

            worksheet.format(
                "A1:Z1",
                {
                    "textFormat": {"bold": True},
                },
            )

            worksheet.format("A:Z", {"wrapStrategy": "CLIP"})

            # Request to freeze the first row
            freeze_request = {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": sheet_id,
                        "gridProperties": {"frozenRowCount": 1},
                    },
                    "fields": "gridProperties.frozenRowCount",
                }
            }

            # Send batch update request with separate operations
            spreadsheet_obj.batch_update({"requests": [freeze_request]})

        print(
            f"Successfully uploaded pandas.DataFrame to new worksheet '{sheet}' in '{spreadsheet}'."
        )

    def append_dataframe_to_sheet(
        self,
        df: pandas.DataFrame,
        sheet: str,
        spreadsheet: str,
        duplicates: bool = False,
    ) -> None:
        """
        Appends new rows from a pandas DataFrame to an existing worksheet in a Google Spreadsheet.

        Args:
            df (pandas.DataFrame): The DataFrame containing the new rows to append.
            sheet (str): The name of the worksheet to append data to.
            spreadsheet (str): The name of the Google Spreadsheet.
            duplicates (bool, optional): Skip rows that already exist exactly. Defaults to False.

        Raises:
            ValueError: If the worksheet does not exist or the DataFrame is empty.

        Returns:
            None
        """

        if df.empty:
            raise ValueError(
                "Error: The pandas.DataFrame is empty. Cannot append empty data. Verify the pandas.DataFrame."
            )

        # Open the spreadsheet
        spreadsheet_obj = self.open_spreadsheet(spreadsheet=spreadsheet)

        # Check if the worksheet exists
        if not self.sheet_exists(sheet=sheet, spreadsheet=spreadsheet_obj):
            raise ValueError(
                f"Error: Worksheet '{sheet}' does not exist in '{spreadsheet}'."
            )

        # Replace NaN values with an empty string
        df = df.fillna("")

        # Open the existing worksheet
        worksheet = spreadsheet_obj.worksheet(sheet)

        # Get actual sheet data
        all_sheet_data = worksheet.get_all_values()
        if not all_sheet_data:
            raise ValueError(
                f"Error: The sheet {sheet} appears to be empty and has no header row."
            )

        # Get sheet headers and rows
        existing_headers = all_sheet_data[0]
        existing_rows = {tuple(row) for row in all_sheet_data[1:]}

        data_to_append = []
        for row in df.to_dict(orient="records"):
            # Convert each field to string for accurate comparison
            new_row = [str(row.get(header, "")) for header in existing_headers]
            if duplicates or tuple(new_row) not in existing_rows:
                data_to_append.append(new_row)

        # Append only if there's new data
        if data_to_append:
            worksheet.append_rows(data_to_append)

        print(
            f"Successfully appended `df` pd.DataFrame to '{sheet}' in '{spreadsheet}' spreadshet."
        )
