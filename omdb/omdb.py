import requests
import json
from rest_framework import exceptions
from django.conf import settings


class OMDBClient(object):

    def __init__(self):
        self.api_key = settings.OMDB_API_KEY

    def get_data_by_title(self, title):
        url = 'http://www.omdbapi.com/?t={}&apikey={}'.format(
            title,
            self.api_key
        )
        response = requests.get(url)
        data = self.get_preprocess_data(response.text)
        return data

    def check_response(self, data):
        if data.get('Response') == 'False':
            raise exceptions.NotFound

    def get_preprocess_data(self, json_data):
        data = json.loads(json_data)
        self.check_response(data)
        ratings = data.get('Ratings')
        data['Ratings'] = [
            self.get_lowercase_dict(rating) for rating in ratings
        ]
        return self.get_lowercase_dict(data)

    def get_lowercase_dict(self, dict_data):
        return {key.lower(): value for key, value in dict_data.items()}
