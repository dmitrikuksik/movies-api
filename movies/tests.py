from django.test import TestCase
from .models import Movie
import json


class MovieTestCase(TestCase):

    def test_movie_post_correct(self):
        title = "Titanic"
        data = json.dumps({"title": title})
        response = self.client.post(
            '/movies/',
            data,
            content_type="application/json",
            )

        self.assertEqual(response.status_code,200)
        self.assertEqual(
            Movie.objects.filter(data__title="Titanic").count(),
            1
        )

    def test_movie_post_incorrect(self):
        title = "Titanic film"
        data = json.dumps({"title": title})
        response = self.client.post(
            '/movies/',
            data,
            content_type="application/json",
            )

        self.assertEqual(response.status_code,400)
        self.assertEqual(
            Movie.objects.all().count(),
            0
        )

    def test_movie_post_exist(self):
        title = "Titanic"
        data = json.dumps({"title": title})
        for i in range(2):
            response = self.client.post(
                '/movies/',
                data,
                content_type="application/json",
                )
        self.assertEqual(
            Movie.objects.filter(data__title=title).count(),
            1
        )

    def test_movie_get(self):
        title = "Titanic"
        data = json.dumps({"title": title})
        self.client.post(
            '/movies/',
            data,
            content_type="application/json",
            )
        response = self.client.get('/movies/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Movie.objects.all().count(),
            len(response.data)
        )

    def test_movie_get_id(self):
        title = "Titanic"
        data = json.dumps({"title": title})
        self.client.post(
            '/movies/',
            data,
            content_type="application/json",
            )
        movie_id = Movie.objects.get(data__title=title).movie_id

        url = '/movies/{}/'.format(movie_id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            movie_id,
            response.data['movie_id']
        )

    


        


