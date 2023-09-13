import os
import json

from client import RickAndMortyClient

# the download functionality
RickAndMortyClient.download()
print("Rick And Morty REST Api download is finished.")


# list of names of the episodes aired between 2017 and 2021 and contains more than three characters
episodes = []
data_dir = "rick_and_morty/episode"
for file in os.listdir(data_dir):
    file_name = os.fsdecode(file)
    with open(f"{data_dir}/{file_name}") as f:
        full_data = json.loads(f.read())
        raw_data = full_data.get("RawData")
        air_date = raw_data.get("air_date")
        # format: May 24, 2015
        year = air_date[-4:]
        if year < "2017" or year > "2021":
            continue
        characters = raw_data.get("characters", [])
        if len(characters) < 3:
            continue
        name = full_data.get("Metadata")
        episodes.append(name)

print(f"List of names of the episodes aired between 2017 and 2021 and contains more than three characters: {episodes}")


# locations which appear only on odd episode numbers
locations = []
data_dir = "rick_and_morty/character"
for file in os.listdir(data_dir):
    file_name = os.fsdecode(file)
    with open(f"{data_dir}/{file_name}") as f:
        full_data = json.loads(f.read())
        raw_data = full_data.get("RawData")
        # the only way to find a relation for location and episode is trough characters.
        location = raw_data.get("location")
        location_name = location.get("name")
        episodes = raw_data.get("episode")

        def check_if_episode_is_odd(episode: str) -> bool:
            episode_last_digit = episode[-1]
            return not int(episode_last_digit) % 2 == 0

        for ep in episodes:
            # format: https://rickandmortyapi.com/api/episode/45
            ep_id = ep.split("/")[-1]
            with open(f"rick_and_morty/episode/{ep_id}.json") as f:
                episode_data = json.loads(f.read())
                episode_raw_data = episode_data.get("RawData")
                episode_number = episode_raw_data.get("episode")
                if check_if_episode_is_odd(episode_number):
                    locations.append(location_name)
                    break


print(f"Locations which appear only on odd episode numbers: {locations}")