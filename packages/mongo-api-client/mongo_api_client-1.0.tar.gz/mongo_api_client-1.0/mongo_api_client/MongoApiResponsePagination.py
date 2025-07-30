from typing import Dict, Any

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