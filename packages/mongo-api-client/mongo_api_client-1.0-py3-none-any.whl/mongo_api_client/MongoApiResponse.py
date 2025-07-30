from .MongoApiResponseData import MongoApiResponseData
from .MongoApiResponsePagination import MongoApiResponsePagination
from typing import Union, Optional, Dict, Any

class MongoApiResponse:
    """
    A uniform wrapper for responses from MongoApiClient.

    Attributes:
        status (bool): Whether the operation succeeded.
        code (int): HTTP or application-specific status code.
        database (Optional[str]): Name of the database involved.
        table (Optional[str]): Name of the collection/table involved.
        count (int): Number of records in the result set.
        pagination (Dict[str, Any]): Pagination metadata (pages, per_page, etc.).
        query (Dict[str, Any]): The query parameters actually sent.
        data (Union[Dict[str, Any], List[Any], None]): The returned document(s).
        error (Optional[str]): Error message if status is False.
        _raw (Dict[str, Any]): The original unwrapped response payload.
    """

    def __init__(self, payload: Dict[str, Any]):
        """
        Initialize the ApiResponse from a raw payload dict.

        Args:
            payload: The JSON-decoded response from the API.
        """
        self._raw = payload
        self.status = payload.get("status", False)
        self.code = payload.get("code", 500)
        self.database = payload.get("database")
        self.table = payload.get("table")
        self.count = payload.get("count", 0)
        self.pagination = payload.get("pagination", {})
        self.query = payload.get("query", {})
        self.data = payload.get("data", None)
        self.error = payload.get("error", None)
        self.databases = payload.get("databases", [])
        self.message = payload.get("message", None)
        self.tables = payload.get("tables", [])

    def get_status(self) -> bool:
        """
        Returns:
            bool: True if the operation succeeded, False otherwise.
        """
        return self.status

    def get_status_code(self) -> int:
        """
        Returns:
            int: HTTP or application-specific status code.
        """
        return self.code

    def get_database(self) -> Optional[str]:
        """
        Returns:
            Optional[str]: The database name, if present.
        """
        return self.database

    def get_table(self) -> Optional[str]:
        """
        Returns:
            Optional[str]: The table/collection name, if present.
        """
        return self.table

    def get_total_count(self) -> int:
        """
        Returns:
            int: Number of records in the result set.
        """
        return self.count

    def get_pagination(self) -> MongoApiResponsePagination:
        """
        Returns:
            MongoApiResponsePagination: Pagination metadata (total_pages, current_page, etc.).
        """
        return MongoApiResponsePagination(self.pagination)

    def get_query(self) -> Dict[str, Any]:
        """
        Returns:
            Dict[str, Any]: The actual query parameters sent to the API.
        """
        return self.query

    def is_ok(self) -> bool:
        return self.get_status() == True

    def is_not_ok(self) -> bool:
        return self.get_status() == False

    def get_count(self) -> int:
        return self.get_total_count()

    def get_data(self) -> Union[MongoApiResponseData, None]:
        """
        Returns:
            Union[Dict[str, Any], List[Any], None]: The returned document(s):
                - A single dict if fetching one record.
                - A list of dicts if fetching multiple.
                - None if no data.
        """
        return MongoApiResponseData(self.data)

    def get_databases(self) -> list:
        return self.databases

    def get_tables(self) -> list:
        return self.tables

    def get_message(self) -> Optional[str]:
        return self.message

    def get_error(self) -> Optional[str]:
        """
        Returns:
            Optional[str]: The error message if status is False, else None.
        """
        return self.error

    def get_response(self) -> Dict[str, Any]:
        """
        Returns:
            Dict[str, Any]: The original raw response payload.
        """
        return self._raw

    def __repr__(self):
        """
        Returns:
            str: A concise summary for debugging.
        """
        return (
            f"<ApiResponse status={self.status!r} code={self.code!r} "
            f"database={self.database!r} table={self.table!r} count={self.count!r}>"
        )

