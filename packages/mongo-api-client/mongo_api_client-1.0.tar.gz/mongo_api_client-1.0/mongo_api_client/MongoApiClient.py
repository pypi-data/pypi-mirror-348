import json
import requests
from typing import Any, Dict, List, Optional, Union, Callable, Type, Tuple, Iterator
import time
import requests
from functools import wraps

from .MongoApiResponse import MongoApiResponse


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

    def count(self) -> MongoApiResponse:
        raw = self._request("GET", "/count", params=self._assemble_params())
        return self._wrap_response(raw, single=True, utils=True)

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