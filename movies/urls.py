from .views import CommentViewSet, MovieViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register("movies", MovieViewSet)
router.register("comments", CommentViewSet)

urlpatterns = router.urls
