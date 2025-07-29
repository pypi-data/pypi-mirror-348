"""
Module for inserting data into ResultTable
"""
import time
import socket
import pyodbc
from msb_rpa.web import close_website_panes


def sql_insert_result(rpa_id: str,
                      executionid: str,
                      resulttype: str,
                      resultinjson: str,
                      conn_str: str,
                      resulttable: str):
    """
    Inserts a row into the given result table using the provided connection.

    Args:
        rpa_id (str): GUID for the RPA process.
        executionid (str): GUID for the execution.
        resulttype (str): Indicates the type of result.
        resultinjson (str): Result in JSON format.
        conn_str (str): Connection string for the database.
        resulttable (str): Table name in the format [schema].[table].

    Note:
        - `rpa_id` and `executionid` should be GUIDs in string format (e.g., str(uuid.uuid4())).
        - If `resulttype` is '1', `resultinjson` is converted to: {"Maskine":"<hostname>"}.
    """

    # Convert result to default format if resulttype is '1'
    if resulttype == '1':
        resultinjson = f'{{"Maskine":"{socket.gethostname()}"}}'

    # Construct the SQL statement
    sql_statement = f'''
    INSERT INTO {resulttable} (RPA_ID, ExecutionID, ResultType, ResultInJson)
    VALUES (?, ?, ?, ?)
    '''

    # Debugging output
    print("SQL Statement:", sql_statement)
    print("Values:", (rpa_id, executionid, resulttype, resultinjson))

    # Execute the insert operation
    with pyodbc.connect(conn_str) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql_statement, (rpa_id, executionid, resulttype, resultinjson))
            connection.commit()


def use_retry_logic(func, *args, max_retries: int = 3, sleep_time: int = 2, target=None, **kwargs):
    """
    Applies retry logic to a function.

    Args:
        func (callable): The function to retry.
        *args: Positional arguments to pass to the function.
        max_retries (int): Maximum number of retries (0-5). Default is 3.
        sleep_time (int): Time to sleep between retries in seconds. Default is 2.
        target (str, optional): The target to match against window title or URL for closing specific windows.
                                If None, all windows will be closed.
        **kwargs: Keyword arguments to pass to the function.
    """

    class BusinessError(Exception):
        """An empty exception used to identify errors caused by breaking business rules"""

    if not (0 <= max_retries <= 5):
        raise ValueError("max_retries must be between 0 and 5")

    last_exception = None
    for attempt in range(max_retries + 1):

        try:
            return func(*args, **kwargs)
        except BusinessError as e:
            print(f"Business error occurred: {e}")
            # Do not retry for business errors
            raise BusinessError(e) from e
        except Exception as e:
            print(f"Process failed on attempt {attempt + 1}: {e}")
            last_exception = e

        if attempt < max_retries:
            print("Retrying...")
            close_website_panes(target=target)
            time.sleep(sleep_time)
        else:
            print("All retries failed.")
            close_website_panes(target=target)
            raise Exception(f"Failed after {max_retries} retries: {last_exception}")
