from django.test import TestCase
from .models import Collection, Movie
from .factories import UserFactory, CollectionFactory, MovieFactory

class CollectionTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.collection = CollectionFactory(user=self.user)

    def test_collection_creation(self):
        self.assertEqual(Collection.objects.count(), 1)
        self.assertEqual(self.collection.user, self.user)
        self.assertIsInstance(self.collection, Collection)

    def test_movie_creation(self):
        movie = MovieFactory(collection=self.collection)
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(movie.collection, self.collection)
        self.assertIsInstance(movie, Movie)
