from django.test import TestCase
from .bandsintown_parsing import get_most_favourite_artists_place_to_perform, ArtistDoesntExist
import mock
from . import services
from .models import SearchRequest


class FakeResponse():
    def __init__(self, status_code=200):
        self.status_code = status_code

    def json(self):
        return [
            {
                "venue": {
                    "country": "Russia",
                    "city": "Moscow",
                    "latitude": "55.7522222",
                    "name": "Крокус Сити Холл",
                    "region": "",
                    "longitude": "37.6155556"
                },
            },
            {
                "venue": {
                    "country": "Russia",
                    "city": "Moscow",
                    "latitude": "55.7703285",
                    "name": "Сад Эрмитаж",
                    "region": "",
                    "longitude": "37.6090393"
                },
            },
            {
                "venue": {
                    "country": "United Kingdom",
                    "city": "London",
                    "latitude": "55.7703285",
                    "name": "Сад Эрмитаж",
                    "region": "",
                    "longitude": "37.6090393"
                },
            },
            {
                "venue": {
                    "country": "France",
                    "city": "Paris",
                    "latitude": "55.7703285",
                    "name": "Сад Эрмитаж",
                    "region": "",
                    "longitude": "37.6090393"
                },
            },
            {
                "venue": {
                    "country": "United States",
                    "city": "Los Angeles",
                    "latitude": "55.7703285",
                    "name": "Сад Эрмитаж",
                    "region": "",
                    "longitude": "37.6090393"
                },
            }
        ]

    def raise_for_status(self):
        pass


class ApiTest(TestCase):

    @mock.patch('requests.get', return_value=FakeResponse())
    def test_get_most_favourite_artists_place_to_perform(self, mocked_get):
        place = get_most_favourite_artists_place_to_perform('Uma2rman')
        self.assertEqual(place, 'Moscow, Russia')
        self.assertTrue(mocked_get.called)

    @mock.patch('requests.get', return_value=FakeResponse(404))
    def test_get_most_favourite_artists_place_to_perform_404(self, mocked_get):
        with self.assertRaises(ArtistDoesntExist):
            place = get_most_favourite_artists_place_to_perform('Uma2rman')
        self.assertTrue(mocked_get.called)

    @mock.patch('requests.get', return_value=FakeResponse(200))
    def test_services_get_most_favourite_artists_place_to_perform(self, mocked_get):
        artist_name = 'Uma2rman'
        empty_query = SearchRequest.objects.filter(artist_name=artist_name)
        self.assertFalse(empty_query)
        place = services.get_most_favourite_artists_place_to_perform(artist_name)
        self.assertEqual(place, 'Moscow, Russia')
        not_empty_query = SearchRequest.objects.filter(artist_name=artist_name)
        self.assertTrue(not_empty_query)
        self.assertEqual(not_empty_query.count(), 1)
        self.assertTrue(mocked_get.called)

    def test_services_history_for_3(self):
        artist_names = ['Uma2rman', 'Eminem', 'Metallica']
        self._check_history(artist_names)

    def test_services_history_for_13(self):
        artist_names = ['Uma2rman', 'Eminem', 'Metallica', 'spam', 'foo', 'Lady Gaga', 'Red Hot Chili Peppers', 'Queen',
                        'Gorillaz', 'Nirvana', 'Nickelback', '50 Cent', 'Muse']
        self._check_history(artist_names)

    def _check_history(self, artist_names):
        for artist_name in artist_names:
            SearchRequest.objects.create(artist_name=artist_name)
        last_10_search_requests = services.get_last_10_search_requests()
        self.assertListEqual(last_10_search_requests, artist_names[:-11:-1])
