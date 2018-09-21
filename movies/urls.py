from django.conf.urls import url
from .views import CommentViewSet, MovieViewSet

from rest_framework.routers import SimpleRouter


urlpatterns = [
    # url(r'movies/$', Movies.as_view(), name='movies'),
    # url(r'movies/(?P<movie_id>\d+)/$', Movies.as_view()),
    # url(r'comments/$', Comments.as_view(), name='comments'),
    # url(r'comments/(?P<movie_id>\d+)/$', Comments.as_view()),
]

router = SimpleRouter()

router.register("movies", MovieViewSet)
router.register("comments", CommentViewSet)

urlpatterns += router.urls
