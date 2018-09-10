from django.conf.urls import include,url
from .views import Movies, Comments

urlpatterns = [
    url(r'movies/', Movies.as_view(), name='movies'),
    url(r'comments/', Comments.as_view(), name='comments'),
]