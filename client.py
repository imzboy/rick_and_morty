import os
import json
import uuid
from typing import List

from helpers import RESTPaginatedIterator



class RESTClient:
    """Download all the data from any provided REST api."""
    # base url of the api.
    base_url: str = None
    # the list of REST resourses that need to be downloaded.
    resourses: List[str] = []
    # relative directory path where to save resourses.
    save_path: str = None
    # dictionary key that stores the results in responce.
    results_key: str = "results"
    # the key or path (ex: key.key.key) to the key for the next url in paginated response.
    next_key: str = "next"
    # dictionary_key for some kind of name from the resourse result that will be used for the file name.
    id_key: str = "id"
    meta_data_key: str = None

    @classmethod
    def make_file_path(cls: "RESTClient", resourse: str, file_name: str) -> str:
        """Create and return the file path of the new file."""
        path = f"./{cls.save_path}/{resourse}"
        file_path = f"{path}/{file_name}.json"
        os.makedirs(path, exist_ok=True)
        return file_path

    @classmethod
    def download(cls: "RESTClient") -> None:
        for resourse in cls.resourses:
            url = f"{cls.base_url}{resourse}/"
            for results in RESTPaginatedIterator(url, cls.results_key, cls.next_key):
                for result in results:
                    file_name = result[cls.id_key]
                    meta_data = result[cls.meta_data_key]
                    file_path = cls.make_file_path(resourse, file_name)
                    with open(file_path, "w") as f:
                        to_insert = {
                            "Id": str(uuid.uuid4()),
                            "Metadata": meta_data,
                            "RawData": result
                        }
                        json_decoded = json.dumps(to_insert)
                        f.write(json_decoded)


class RickAndMortyClient(RESTClient):

    base_url = "https://rickandmortyapi.com/api/"
    resourses = ["character", "location", "episode"]
    save_path = "rick_and_morty"
    next_key = "info.next"
    meta_data_key = "name"
