from . import bandsintown_parsing
from .models import SearchRequest


def get_most_favourite_artists_place_to_perform(artist_name):
    SearchRequest.objects.create(artist_name=artist_name)
    place = bandsintown_parsing.get_most_favourite_artists_place_to_perform(artist_name)
    return place


def get_last_10_search_requests():
    last_10_requests = SearchRequest.objects.order_by('-id')[:10]
    return [request.artist_name for request in last_10_requests]
