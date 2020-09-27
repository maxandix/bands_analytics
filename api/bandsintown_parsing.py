import requests
import collections


class ArtistDoesntExist(Exception):
    pass


def places_of_events(events):
    for event in events:
        # because of COVID
        if event['venue']['name'] == 'Live Stream':
            continue

        city = event['venue']['city']
        country = event['venue']['country']
        yield f'{city}, {country}'


def get_most_favourite_artists_place_to_perform(artist_name):
    response = requests.get(f'https://rest.bandsintown.com/artists/{artist_name}/events?app_id=11&date=all')

    if response.status_code == 404:
        raise ArtistDoesntExist
    response.raise_for_status()

    events = response.json()
    counter = collections.Counter()
    for place in places_of_events(events):
        counter[place] += 1

    return counter.most_common(1)[0][0]


if __name__ == '__main__':
    result = get_most_favourite_artists_place_to_perform('eminem')
    print(result)
