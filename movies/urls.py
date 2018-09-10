from django.conf.urls import include,url
from .views import Movies

urlpatterns = [
    url(r'', Movies.as_view(), name='movies'),
]