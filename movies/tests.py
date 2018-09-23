from django.test import TestCase
from .models import Movie, Comment
from .utils import OMDBClient
from .helps import OMDB_MOVIE_DATA, PREPROCESSED_MOVIE_DATA
from unittest import mock
import json


class OMDBTestCase(TestCase):

    @mock.patch('requests.get')
    def test_get_data_by_title_correct(self, mock_get):
        mock_response = mock.Mock()
        expected_data = OMDB_MOVIE_DATA

        mock_response.json.return_value = expected_data
        mock_response.status_code = 200

        mock_get.return_value = mock_response

        response_data = OMDBClient().get_data_by_title(
            title='Titanic'
        )

        self.assertEqual(
            response_data,
            PREPROCESSED_MOVIE_DATA
        )


class MovieTestCase(TestCase):

    def post_movie(self, titles):
        for title in titles:
            data = json.dumps({"title": title})
            response = self.client.post(
                        '/movies/',
                        data,
                        content_type="application/json",
            )
        return response

    @mock.patch('movies.utils')
    def test_movie_post_omdb_api(self, mock_utils):
        mock_client = mock_utils.OMDBClient()
        mock_client.get_data_by_title.return_value = PREPROCESSED_MOVIE_DATA

        movie_data = mock_client.get_data_by_title('Titanic')

        mock_client.get_data_by_title.assert_called_once_with('Titanic')

    def test_movie_post_correct(self):
        response = self.post_movie(["Titanic"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Movie.objects.filter(data__title="Titanic").count(),
            1
        )

    def test_movie_post_incorrect(self):
        response = self.post_movie(["Titanic film"])
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            Movie.objects.all().count(),
            0
        )

    def test_movie_post_exist(self):
        title = "Titanic"
        self.post_movie([title for i in range(3)])
        self.assertEqual(
            Movie.objects.filter(data__title=title).count(),
            1
        )

    def test_movie_get(self):
        self.post_movie(["Titanic"])
        response = self.client.get('/movies/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Movie.objects.all().count(),
            len(response.data)
        )

    def test_movie_get_id(self):
        title = "Titanic"
        self.post_movie([title])

        movie_id = Movie.objects.get(data__title=title).movie_id
        url = '/movies/{}/'.format(movie_id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            movie_id,
            response.data['movie_id']
        )

    def test_movie_get_year(self):
        titles = ["Titanic", "Fight Club"]
        self.post_movie(titles)

        year = "1997"
        url = '/movies/?year={}'.format(year)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Movie.objects.filter(data__year=year).count(),
            len(response.data)
        )

    def test_movie_get_order_by(self):
        titles = ["Titanic", "Fight Club", "Atlas"]
        self.post_movie(titles)

        order_by = "data__title"
        url = '/movies/?ordering={}'.format(order_by)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Movie.objects.get(data__title=titles[2]).movie_id,
            response.data[0]['movie_id']
        )

    def test_movie_get_order_by_and_year(self):
        titles = ["Deadpool 2", "Black Panther", "Titanic"]
        self.post_movie(titles)

        order_by = "data__title"
        year = "2018"
        url = '/movies/?ordering={}&year={}'.format(order_by, year)
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

    def test_comment_get_query_not_exist(self):
        titles = ["Deadpool 2", "Black Panther", "Titanic"]
        self.post_movie(titles)

        query = 'some_value'
        url = '/movies/?query_not_exist={}'.format(query)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 400)


class CommentTestCase(TestCase):

    def post_movie(self, titles):
        for title in titles:
            data = json.dumps({"title": title})
            response = self.client.post(
                        '/movies/',
                        data,
                        content_type="application/json",
            )

    def post_comment(self, movie_id, text):
        data = json.dumps({
            "movie_id": movie_id,
            "text": text
        })
        response = self.client.post(
            '/comments/',
            data,
            content_type="application/json",
        )
        return response

    def test_comment_post_correct(self):
        title = "Titanic"
        self.post_movie([title])

        movie_id = Movie.objects.get(data__title=title).movie_id
        text = "The best movie ever!"
        response = self.post_comment(movie_id, text)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            Comment.objects.filter(text=text).count(),
            1
        )

    def test_comment_post_incorrect(self):
        movie_id = 0
        text = "The best movie ever!"
        response = self.post_comment(movie_id, text)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            Comment.objects.all().count(),
            0
        )

    def test_comment_get(self):
        titles = ["Deadpool 2", "Black Panther"]
        self.post_movie(titles)

        for title in titles:
            movie_id = Movie.objects.get(data__title=title).movie_id
            texts = ["Funny!", "This is awesome :)", "Waiting for next part"]
            for text in texts:
                self.post_comment(movie_id, text)

        response = self.client.get('/comments/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Comment.objects.all().count(),
            len(response.data)
        )

    def test_comment_get_id(self):
        titles = ["Deadpool 2", "Black Panther"]
        self.post_movie(titles)
        for title in titles:
            movie_id = Movie.objects.get(data__title=title).movie_id
            texts = ["Funny!", "This is awesome :)", "Waiting for next part"]
            for text in texts:
                self.post_comment(movie_id, text)

        movie_id = Movie.objects.get(data__title=titles[0]).movie_id
        url = '/comments/?movie_id={}'.format(movie_id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Comment.objects.filter(movie_id=movie_id).count(),
            len(response.data)
        )
