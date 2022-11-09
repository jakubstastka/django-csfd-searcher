from django.test import TestCase
from django.utils.text import slugify

from searcher.models import Actor, Movie


class TestSlugCreation(TestCase):
    def test_if_actors_and_movies_get_slug_generated(self):
        actor_names = ["Tom Hanks", "Jiří Kodet", "Emília Vášáryová"]

        for actor_name in actor_names:
            actor = Actor.objects.create(name=actor_name)

            self.assertEqual(actor.slug, slugify(actor))

        movie_names = ["Pelíšky", "Terminátor 2: Den zúčtování", "Vykoupení z věznice Shawshank"]
        for movie_name in movie_names:
            movie = Movie.objects.create(name=movie_name)

            self.assertEqual(movie.slug, slugify(movie))
