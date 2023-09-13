from typing import List
import requests



class RESTPaginatedIterator:
    """Iterates trough paginated response via requests library."""

    def __init__(self, url: str, results_key: str, next_key: str) -> None:
        self.url = url
        self.results_key = results_key
        # path for the next key
        if "." in next_key:
            self.next_key = next_key.split(".")

    def __get_next(self, response: dict) -> str | None:
        if isinstance(self.next_key, list):
            for key in self.next_key:
                response = response.get(key, {})
            return response
        return response.get(self.next_key)

    def __iter__(self) -> "RESTPaginatedIterator":
        return self

    def __next__(self) -> List[dict]:
        # the pagination is finished and we should stop iteration
        if not self.url:
            raise StopIteration

        req = requests.get(self.url)
        req.raise_for_status()
        response_body = req.json()
        results = response_body.get(self.results_key)
        self.url = self.__get_next(response_body)
        return results
