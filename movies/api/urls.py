from django.urls import path, include
from rest_framework import routers
from .views import MovieViewSet, RatingViewSet, GenreViewSet

router = routers.DefaultRouter()

router.register('movie', MovieViewSet, basename='movie')
router.register('rating', RatingViewSet, basename='rating')
router.register('genre', GenreViewSet, basename='genre')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_auth.urls')),
    path('auth/reg', include('rest_auth.registration.urls'))
]
