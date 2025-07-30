from typing import Any, Dict, List, Optional, Union, Callable, Type, Tuple, Iterator
from .MongoApiResponsePagination import MongoApiResponsePagination

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

    def get_results(self):
        return MongoApiResponseData(self._payload)

    def get_result(self) -> dict:
        if isinstance(self._payload, list) and len(self._payload) == 1:
            return self._payload[0]
        return self._payload

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

    def get_record_id(self) -> any:
        """
        Retrieve the record id / criteria on which it was grouped on

        Returns:
            any: Can return any type
        """
        if not self.has_grouped():
            return None
        if isinstance(self._payload, dict):
            return self._payload.get("_id")
        return [
            item.get("_id") if isinstance(item, dict) and self._is_grouped(item) else None
            for item in self._payload
        ]

    def get_total_records(self) -> List[int]:
        """
        Retrieve total_records count(s), or sum of them.

        Returns:
            - [int] for a single-doc payload if it's grouped and has a numeric total_records,
            - [sum] for a list payload with grouped items that have numeric total_records,
            - [] if not grouped or no valid numeric total_records fields.
        """
        if not self.has_grouped():
            return []

        if isinstance(self._payload, dict):
            val = self._payload.get("total_records")
            return [int(val)] if isinstance(val, (int, float, str)) and str(val).isdigit() else []

        total = 0
        found = False
        for doc in self._payload:
            if isinstance(doc, dict) and self._is_grouped(doc):
                val = doc.get("total_records")
                if isinstance(val, (int, float, str)) and str(val).isdigit():
                    total += int(val)
                    found = True

        return [total] if found else []

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
