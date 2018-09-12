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
    
    def test_movie_get_year(self):
        titles = [ "Titanic", "Fight Club"]
        for title in titles:
            data = json.dumps({"title": title})
            self.client.post(
                '/movies/',
                data,
                content_type="application/json",
                )
        
        year = "1997"
        url = '/movies/?year={}/'.format(year)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Movie.objects.filter(data__year=year).count(),
            len(response.data)
        )

    def test_movie_get_order_by(self):
        titles = [ "Titanic", "Fight Club","Atlas"]
        for title in titles:
            data = json.dumps({"title": title})
            self.client.post(
                '/movies/',
                data,
                content_type="application/json",
                )
        
        order_by = "data__title"
        url = '/movies/?order_by={}'.format(order_by)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Movie.objects.get(data__title=titles[2]).movie_id,
            response.data[0]['movie_id']
        )

    def test_movie_get_order_by_and_year(self):
        titles = [ "Deadpool 2", "Black Panther", "Titanic"]
        for title in titles:
            data = json.dumps({"title": title})
            self.client.post(
                '/movies/',
                data,
                content_type="application/json",
                )
        
        order_by = "data__title"
        year = "2018"
        url = '/movies/?order_by={}&year={}'.format(order_by,year)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Movie.objects.filter(data__year=year).count(),
            len(response.data)
        )
        self.assertEqual(
            Movie.objects.get(data__title=titles[1]).movie_id,
            response.data[0]['movie_id']
        )

class CommentTestCase(TestCase):

    def test_comment_post_correct(self):
        pass

        





        


