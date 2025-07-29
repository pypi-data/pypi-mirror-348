import json
import requests
from typing import Any, Dict, List, Optional, Union, Callable, Type, Tuple, Iterator
import time
import requests
from functools import wraps


def retry(
    exceptions: Union[Type[BaseException], Tuple[Type[BaseException], ...]] = (
        requests.RequestException,
    ),
    retries: int = 3,
    backoff: float = 0.5,
    backoff_factor: float = 2.0,
) -> Callable:
    """
    Decorator to retry a function on specified exceptions.

    Args:
        exceptions: Exception class or tuple of classes to catch and retry on.
        retries: Number of total attempts (initial call + retries = retries).
        backoff: Initial wait time between retries, in seconds.
        backoff_factor: Multiplier applied to the backoff after each retry.

    Usage:
        @retry(retries=5, backoff=1.0)
        def flaky_operation(...):
            ...
    """

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            attempts, delay = retries, backoff
            last_exc = None
            while attempts > 0:
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    attempts -= 1
                    if attempts == 0:
                        break
                    time.sleep(delay)
                    delay *= backoff_factor
            # re-raise the last exception if we exhausted retries
            raise last_exc

        return wrapper

    return decorator


def _convert_col_value_for_arrays(data: Any, auto_convert_type: bool) -> str:
    """
    Format a value (or 2-item array) for serialized output,
    appending '/a' (auto-convert) or '/n' (no-convert) as needed.

    Args:
        data (Any): The data to convert (could be a value or 2-element list).
        auto_convert_type (bool): Whether to tag the value(s) for auto-conversion.

    Returns:
        str: The formatted representation.
    """
    def tag(val: Any) -> str:
        suffix = "/a" if auto_convert_type else "/n"
        return f"{val}{suffix}"

    if isinstance(data, list) and len(data) == 2:
        return f"[{tag(data[0])}: {tag(data[1])}]"

    return tag(data)


def _merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for d in dicts:
        result.update(d)
    return result

class MongoApiResponsePagination:
    """
    Wraps the 'pagination' section of a Mongo API response,
    providing convenient accessors for pagination metadata.
    """

    def __init__(self, payload: Dict[Any, Any]):
        """
        Initialize the pagination helper.

        Args:
            payload: The raw pagination dict, e.g.
              {
                  "total_pages": 1,
                  "current_page": 1,
                  "next_page": 1,
                  "prev_page": 1,
                  "last_page": 1,
                  "per_page": 10
              }
        """
        self.payload: Dict[Any, Any] = payload

    def get_total_pages(self) -> int:
        """
        Get the total number of pages available.

        Returns:
            The 'total_pages' value, or 1 if it's missing.
        """
        return int(self.payload.get("total_pages", 1))

    def get_current_page(self) -> int:
        """
        Get the current page index.

        Returns:
            The 'current_page' value, or 1 if it's missing.
        """
        return int(self.payload.get("current_page", 1))

    def get_next_page(self) -> int:
        """
        Get the next page index.

        Returns:
            The 'next_page' value, or 1 if it's missing.
        """
        return int(self.payload.get("next_page", 1))

    def get_prev_page(self) -> int:
        """
        Get the previous page index.

        Returns:
            The 'prev_page' value, or 1 if it's missing.
        """
        return int(self.payload.get("prev_page", 1))

    def get_last_page(self) -> int:
        """
        Get the last page index.

        Returns:
            The 'last_page' value, or 1 if it's missing.
        """
        return int(self.payload.get("last_page", 1))

    def get_per_page(self) -> int:
        """
        Get the number of items per page.

        Returns:
            The 'per_page' value, or 1 if it's missing.
        """
        return int(self.payload.get("per_page", 1))

    def get_payload(self) -> Dict[Any, Any]:
        """
        Retrieve the raw pagination payload.

        Returns:
            The original pagination dict.
        """
        return self.payload

    def __repr__(self) -> str:
        """
        Return a concise summary of the pagination state for debugging.

        Example:
            <MongoApiResponsePagination page=2/5 per_page=10>
        """
        current = self.get_current_page()
        total = self.get_total_pages()
        per_page = self.get_per_page()
        return (
            f"<MongoApiResponsePagination page={current}/{total} "
            f"per_page={per_page}>"
        )


class MongoApiResponseData:
    """
    Wraps one or more documents from the 'results' array of a Mongo API response,
    providing accessors for grouped-by subfields (inner_pagination, records,
    total_records). If grouped fields aren't present at the top level, fall back
    to get_response(). Supports iteration to yield individual document wrappers.
    """

    def __init__(self, payload: Union[Dict[str, Any], List[Dict[str, Any]]]):
        """
        Initialize with either:
        - A dict representing one document (with grouped fields), or
        - A list of such dicts.

        Args:
            payload: Raw response element(s) from response['results'].
        """
        self._payload = payload

    def __iter__(self) -> Iterator['MongoApiResponseData']:
        """
        Iterate over individual document wrappers.

        Yields:
            MongoApiResponseData for each dict in payload list,
            or self if payload is a single dict.
        """
        if isinstance(self._payload, list):
            for item in self._payload:
                yield MongoApiResponseData(item)
        else:
            yield self

    def __len__(self) -> int:
        """
        Return number of documents wrapped.

        Returns:
            1 for single dict, or len(list) for list payload.
        """
        return len(self._payload) if isinstance(self._payload, list) else 1

    def _is_grouped(self, doc: Dict[str, Any]) -> bool:
        """
        Check if a single document contains grouped pagination fields.
        """
        return all(k in doc for k in ("inner_pagination", "records", "total_records"))

    def has_grouped(self) -> bool:
        """
        Determine if payload(s) include grouped-by data.

        Returns:
            True if single dict has grouped fields, or list contains at least one
            dict with grouped fields.
        """
        if isinstance(self._payload, dict):
            return self._is_grouped(self._payload)
        if isinstance(self._payload, list):
            return any(isinstance(item, dict) and self._is_grouped(item) for item in self._payload)
        return False

    def get_inner_pagination(
            self
    ) -> Optional[Union[MongoApiResponsePagination, List[Optional[MongoApiResponsePagination]]]]:
        """
        Retrieve inner_pagination data wrapped in MongoApiResponsePagination.

        Returns:
            - A MongoApiResponsePagination for single-doc payload,
            - A list of MongoApiResponsePagination or None for each item in list payload,
            - None if no grouped data.
        """
        if not self.has_grouped():
            return None

        if isinstance(self._payload, dict):
            inner = self._payload.get("inner_pagination")
            return MongoApiResponsePagination(inner) if inner is not None else None

        wrapped = []
        for item in self._payload:
            if isinstance(item, dict) and self._is_grouped(item):
                inner = item.get("inner_pagination")
                wrapped.append(MongoApiResponsePagination(inner) if inner is not None else None)
            else:
                wrapped.append(None)
        return wrapped

    def get_records(
        self
    ) -> Optional[Union[List[Dict[str, Any]], List[Optional[List[Dict[str, Any]]]]]]:
        """
        Retrieve records data.

        Returns:
            - List of dicts for single-doc payload,
            - List of record-lists/None for each item in list payload,
            - None if no grouped data.
        """
        if not self.has_grouped():
            return None
        if isinstance(self._payload, dict):
            return self._payload.get("records")
        return [
            item.get("records") if isinstance(item, dict) and self._is_grouped(item) else None
            for item in self._payload
        ]

    def get_total_records(
        self
    ) -> Optional[Union[int, List[Optional[int]]]]:
        """
        Retrieve total_records count.

        Returns:
            - Int for single-doc payload,
            - List of ints/None for each item in list payload,
            - None if no grouped data.
        """
        if not self.has_grouped():
            return None
        if isinstance(self._payload, dict):
            val = self._payload.get("total_records")
            try:
                return int(val)
            except (TypeError, ValueError):
                return None
        results = []
        for item in self._payload:
            if isinstance(item, dict) and self._is_grouped(item):
                try:
                    results.append(int(item.get("total_records")))
                except (TypeError, ValueError):
                    results.append(None)
            else:
                results.append(None)
        return results

    def get_data(self) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Return the raw payload unchanged.
        """
        return self._payload

    def __repr__(self) -> str:
        """
        Provide a summary indicating number of items and grouped status.

        Example:
          <MongoApiResponseData items=3 grouped=True>
        """
        count = len(self._payload) if isinstance(self._payload, list) else 1
        grp = self.has_grouped()
        return f"<MongoApiResponseData items={count} grouped={grp}>"


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


class MongoApiClient:
    """
    RESTful API client for MongoDB API.
    Supports fluent query building and select/insert/update/delete,
    returning a uniform response envelope for all methods.
    """

    _OPERATOR_MAP = {
        "=": "=",
        "!=": "!=",
        "<": "<",
        "<=": "<=",
        ">": ">",
        ">=": ">=",
        "like": "ilike",
        "not_like": "not_like",
        "between": "between",
    }
    _SORT_ORDERS = {"asc", "desc"}

    def __init__(
        self,
        server_url: str,
        server_port: int,
        api_key: Optional[str] = None,
        scheme: str = "http",
        auto_convert_values : bool = True,
        timeout: float = 5.0,
    ) -> None:
        self._base_url = f"{scheme}://{server_url}:{server_port}/db"
        self._headers = {
            "Accept": "application/json",
            **({"api_key": api_key} if api_key else {}),
        }
        self._timeout = timeout
        self._session = requests.Session()

        # Query-builder state
        self._db_name: Optional[str] = None
        self._table_name: Optional[str] = None
        self._where: List[str] = []
        self._or_where: List[str] = []
        self._sort_by: List[str] = ["_id", "desc"]
        self._group_by: Optional[str] = None
        self._page: Optional[int] = None
        self._per_page: Optional[int] = None
        self._inner_page : Optional[int] = None
        self._inner_per_page : Optional[int] = None
        self._as_pipeline : Optional[bool] = False
        self._auto_convert_values : Optional[bool] = auto_convert_values

    def _reset_query(self) -> None:
        self._where.clear()
        self._or_where.clear()
        self._sort_by.clear()
        self._group_by = None
        self._page = None
        self._per_page = None
        self._inner_page = None
        self._inner_per_page = None

    def _assemble_params(self) -> Dict[str, Any]:
        p: Dict[str, Any] = {}
        if self._where:
            p["query_and"] = "[" + "|".join(self._where) + "]"
        if self._or_where:
            p["query_or"] = "[" + "|".join(self._or_where) + "]"
        if self._sort_by:
            p["sort"] = "[" + "|".join(self._sort_by) + "]"
        if self._group_by:
            p["group_by"] = self._group_by
        if self._page and self._page > 0:
            p["page"] = self._page
        if self._per_page and self._per_page > 0:
            p["per_page"] = self._per_page
        if self._inner_page and self._inner_page > 0:
            p["inner_page"] = self._inner_page
        if self._inner_per_page and self._inner_per_page > 0:
            p["inner_per_page"] = self._inner_per_page
        if self._as_pipeline:
            p["as_pipeline"] = self._as_pipeline
        if self._auto_convert_values:
            p["auto_convert_inputs"] = self._auto_convert_values
        return p

    def _build_path(self, path: Optional[str] = None) -> str:
        """
        Builds a safe API path by joining non-empty components.

        Args:
            path (Optional[str]): Optional additional endpoint path.

        Returns:
            str: A fully constructed URL path for the request.
        """
        parts = [
            self._base_url.rstrip("/"),
            self._db_name or "",
            self._table_name or "",
            path or "",
        ]
        return "/".join(part.strip("/") for part in parts if part)

    @retry(retries=3, backoff=0.5, backoff_factor=2.0)
    def _send_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]],
        data: Optional[Any],
        headers: Dict[str, str],
    ) -> Dict[str, Any]:
        """Internal: perform the HTTP request and raise on any network/HTTP error."""
        resp = self._session.request(
            method,
            url,
            params=params,
            data=data,
            headers=headers,
            timeout=self._timeout,
        )
        resp.raise_for_status()
        return resp.json()

    def _request(
        self,
        method: str,
        path: str = "",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        use_custom_path: bool = False,
        custom_path: str = None,
    ) -> Dict[str, Any]:
        """
        Public: build full URL, merge headers, call _send_request with retry,
        and catch any final errors into a uniform envelope.
        """
        url = self._build_path(path)
        hdrs = _merge_dicts(self._headers, headers or {})

        if use_custom_path:
            url = custom_path

        try:
            return self._send_request(method, url, params, data, hdrs)
        except Exception as e:
            return {
                "status": False,
                "code": 500,
                "error": f"{method} {url} ultimately failed after retries: {e}",
            }

    def _wrap_response(
        self, raw: Dict[str, Any], single: bool = False, utils: bool = False
    ) -> MongoApiResponse:
        """
        Normalize any raw API response into a consistent envelope.
        
        If raw['status'] is False:
            → {status: False, code: <code or 500>, error: <error message>}
        
        If utils is True:
            → Return simplified responses for utilities like databases, tables, or messages.
        
        Otherwise:
            → Return a standard data response with metadata and results.
        """

        # Failure case
        if not raw.get("status", False):
            return MongoApiResponse({
                "status": False,
                "code": raw.get("code", 500),
                "error": raw.get("error", "Unknown error"),
            })

        # Utility endpoints (e.g. list of databases, tables, etc.)
        if utils:
            if "databases" in raw:
                return MongoApiResponse({
                    "status": True,
                    "databases": raw.get("databases", [])
                })
            if "tables" in raw:
                return MongoApiResponse({
                    "status": True,
                    "tables": raw.get("tables", [])
                })
            if "message" in raw:
                return MongoApiResponse({
                    "status": True,
                    "code": raw.get("code", 200),
                    "message": raw.get("message", "unknown message")
                })

        # Default data response
        results = raw.get("results") or []

        return MongoApiResponse({
            "status": True,
            "code": raw.get("code", 200),
            "database": raw.get("database"),
            "table": raw.get("table"),
            "count": raw.get("count", 0),
            "pagination": raw.get("pagination", {}),
            "query": raw.get("query", {}),
            "data": results[0] if single and results else (None if single else results)
        })


    # ——— Fluent interface —————————————————————————————

    def from_db(self, db_name: str) -> "MongoApiClient":
        self._db_name = db_name
        return self

    def into_db(self, db_name: str) -> "MongoApiClient":
        return self.from_db(db_name)

    def from_table(self, table_name: str) -> "MongoApiClient":
        self._table_name = table_name
        return self

    def into_table(self, table_name: str) -> "MongoApiClient":
        return self.from_table(table_name)

    def where(self, column: str, operator: str, value: Any, auto_convert_type : bool = True) -> "MongoApiClient":
        op = self._OPERATOR_MAP.get(operator)
        if op:
            self._where.append(f"{column},{op},{_convert_col_value_for_arrays(value, auto_convert_type)}")
        return self

    def or_where(self, column: str, operator: str, value: Any, auto_convert_type = True) -> "MongoApiClient":
        op = self._OPERATOR_MAP.get(operator)
        if op:
            self._or_where.append(
                f"{column},{op},{_convert_col_value_for_arrays(value, auto_convert_type)}"
            )
        return self

    def sort_by(self, column: str, direction: str) -> "MongoApiClient":
        if direction in self._SORT_ORDERS:
            self._sort_by.append(f"{column}:{direction}")
        return self

    def group_by(self, column: str) -> "MongoApiClient":
        self._group_by = column
        return self

    def page(self, page: int) -> "MongoApiClient":
        if page > 0:
            self._page = page
        return self

    def per_page(self, per_page: int) -> "MongoApiClient":
        if per_page > 0:
            self._per_page = per_page
        return self

    def inner_page(self, inner_page: int) -> "MongoApiClient":
        if inner_page > 0:
            self._inner_page = inner_page
        return self

    def inner_per_page(self, inner_per_page: int) -> "MongoApiClient":
        if inner_per_page > 0:
            self._inner_per_page = inner_per_page
        return self

    # ——— CRUD operations —————————————————————————————
    def execute_custom_query(self, custom_query : any = None, aggregate : bool = False) -> MongoApiResponse:
        """Will execute a custom query for data retrieval

        Args:
            custom_query (str, optional): custom query in the form of a string. Defaults to None.
            ex no aggregate: { "stats.timePlayed": { "$gte":  10000 } }
            ex with aggregate: [
                    { "$match": { "stats.timePlayed": { "$gte": 10000 } } }
                ]


        Returns:
            MongoApiClient: The inst
        """
        self._as_pipeline = aggregate
        params = self._assemble_params()
        body = {"payload": json.dumps(custom_query)}
        raw = self._request(
            "POST",
            "/custom-query",
            params=params,
            data=body,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        return self._wrap_response(raw)
        
    def find(self) -> MongoApiResponse:
        raw = self._request("GET", "/select", params=self._assemble_params())
        self._reset_query()
        return self._wrap_response(raw, single=False)

    def first(self) -> MongoApiResponse:
        self._page = 1
        self._per_page = 1
        raw = self._request("GET", "/select", params=self._assemble_params())
        self._reset_query()
        return self._wrap_response(raw, single=True)

    def find_by_id(self, mongo_id: str) -> MongoApiResponse:
        raw = self._request("GET", f"/get/{mongo_id}")
        return self._wrap_response(raw, single=True)

    def insert(self, payload: Union[Dict[str, Any], List[Any]]) -> MongoApiResponse:
        body = {"payload": json.dumps(payload)}
        raw = self._request(
            "POST",
            "/insert",
            data=body,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        return self._wrap_response(raw, single=False)

    def insert_if(self, payload: Union[Dict[str, Any], List[Any]]) -> MongoApiResponse:
        params = self._assemble_params()
        body = {"payload": json.dumps(payload)}
        raw = self._request(
            "POST",
            "/insert-if",
            params=params,
            data=body,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        return self._wrap_response(raw, single=False)

    def update(self, payload: Union[Dict[str, Any], List[Any]]) -> MongoApiResponse:
        params = self._assemble_params()
        body = {"payload": json.dumps(payload)}
        raw = self._request(
            "PUT",
            "/update-where",
            params=params,
            data=body,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        return self._wrap_response(raw, single=False)

    def update_by_id(
        self, mongo_id: str, payload: Union[Dict[str, Any], List[Any]]
    ) -> MongoApiResponse:
        body = {"payload": json.dumps(payload)}
        raw = self._request(
            "PUT",
            f"/update/{mongo_id}",
            data=body,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        return self._wrap_response(raw, single=False)

    def delete(self) -> MongoApiResponse:
        raw = self._request("DELETE", "/delete-where", params=self._assemble_params())
        return self._wrap_response(raw, single=False)

    def delete_by_id(self, mongo_id: str) -> MongoApiResponse:
        raw = self._request("DELETE", f"/delete/{mongo_id}")
        return self._wrap_response(raw, single=False)

    # ——— Utilities ————————————————————————————————

    def use_db(self, db_name : str = None):
        return self.from_db(db_name)

    def use_table(self, table_name : str = None):
        return self.from_table(table_name)
    
    def use_collection(self, collection_name : str = None):
        return self.use_table(collection_name)
    
    def list_databases(self) -> MongoApiResponse:
        raw = self._request("GET", "/databases")
        return self._wrap_response(raw=raw, utils=True)

    def list_tables_in_db(self, db_name: str) -> MongoApiResponse:
        raw = self._request("GET", f"/{db_name}/tables")
        return self._wrap_response(raw=raw, utils=True)

    def delete_database(self, db_name: str = None) -> MongoApiResponse:
        selected_db: str = db_name if db_name else self._db_name
        self.from_db(selected_db)

        request_url: str = f"{self._base_url}/{selected_db}/delete"
        return self._wrap_response(
            self._request(
                method="DELETE", use_custom_path=True, custom_path=request_url
            ),
            utils=True,
        )

    def delete_table(self, db_name: str = None, table_name: str = None) -> MongoApiResponse:
        selected_db: str = db_name if db_name else self._db_name
        selected_table: str = table_name if table_name else self._table_name

        request_url: str = f"{self._base_url}/{selected_db}/{selected_table}/delete"
        return self._wrap_response(
            self._request(
                method="DELETE", use_custom_path=True, custom_path=request_url
            ),
            utils=True,
        )

    # ——— Aliases for `find()` —————————————————————————————————
    def select(self) -> MongoApiResponse:
        """
        Alias for `find()`: fetch all matching documents.

        Returns:
            MongoApiResponse
        """
        
        return self.find()
    def all(self) -> MongoApiResponse:
        """
        Alias for `find()`: fetch all matching documents.

        Returns:
            MongoApiResponse
        """
        return self.find()

    def get(self) -> MongoApiResponse:
        """
        Alias for `find()`: fetch all matching documents.

        Returns:
            MongoApiResponse
        """
        return self.find()

    def get_all(self) -> MongoApiResponse:
        """
        Alias for `find()`: fetch all matching documents.

        Returns:
            MongoApiResponse
        """
        return self.find()

    # ——— Aliases for first() ———————————————————————————————

    def first_or_none(self) -> MongoApiResponse:
        """
        Alias for `first()`: fetch the first matching document or return None.

        Returns:
            Optional[Dict[str, Any]]: The single-document envelope, or None.
        """
        return self.first()

    def one(self) -> MongoApiResponse:
        """
        Alias for `first()`: fetch the first matching document or return None.

        Returns:
            Optional[Dict[str, Any]]: The single-document envelope, or None.
        """
        return self.first()

    # --- Alias for per_page ---
    def limit(self, per_page: int) -> "MongoApiClient":
        return self.limit(per_page)
    
    # -- aliases for dropping stuff
    def drop_database(self, db_name: str = None) -> MongoApiResponse:
        return self.delete_database(db_name)

    def drop_collection(self, db_name : str = None, collection_name : str = None) -> MongoApiResponse:
        return self.delete_table(db_name, collection_name)