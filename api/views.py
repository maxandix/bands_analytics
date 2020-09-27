from django.views.decorators.http import require_safe
from bands_analytics.base_view import base_view
from .bandsintown_parsing import ArtistDoesntExist
from . import services
from django.http import HttpResponseNotFound


@base_view
@require_safe
def get_place(request, artist_name):
    try:
        return services.get_most_favourite_artists_place_to_perform(artist_name)
    except ArtistDoesntExist:
        return HttpResponseNotFound(f'Artist "{artist_name}" not found.')


@base_view
@require_safe
def get_history(request):
    return services.get_last_10_search_requests()
