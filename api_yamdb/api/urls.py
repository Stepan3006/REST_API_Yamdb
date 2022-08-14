from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    email,
    token,
    CommentViewSet,
    ReviewViewSet,
    GenresViewSet,
    CategoriesViewSet,
    TitlesViewSet
)

router_v1 = DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)
router_v1.register(
    'genres',
    GenresViewSet,
    basename='genres'
)
router_v1.register(
    'categories',
    CategoriesViewSet,
    basename='categories'
)
router_v1.register(
    'titles',
    TitlesViewSet,
    basename='titles'
)

router_v1_auth = DefaultRouter()
router_v1_auth.register(
    'users',
    UserViewSet,
    basename='users'
)

auth_patterns = [
    path('signup/', email),
    path('token/', token),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include(router_v1_auth.urls)),
    path('v1/auth/', include(auth_patterns)),
]
