from .serializers import MovieSerializer, RatingSerializer, GenreSerializer
from .models import Movie, Rating, Genre
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework import status
from django_filters import rest_framework as filters


class MovieFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Movie
        fields = ('title', )


class GenreViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        queryset = Genre.objects.values('id', 'name').order_by('name')
        serializer = GenreSerializer(queryset, many=True)

        return Response(serializer.data)

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by('-created')
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    filterset_class = MovieFilter

    @action(detail=True, methods=['POST'])
    def rate_movie(self, requests, pk=None):
        if 'rate' in requests.data:
            movie = Movie.objects.get(id=pk)
            rate = requests.data['rate']
            user = requests.user

            try:
                rating = Rating.objects.get(user=user, movie=movie)
                rating.rate = rate
                rating.save()
                serializer = RatingSerializer(rating)
                response = {'message': 'Rating updated', 'rating': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating(user=user, movie=movie, rate=rate)
                rating.save()
                serializer = RatingSerializer(rating)
                response = {'message': 'Rating created', 'rating': serializer.data}
                return Response(response, serializer.data)
        else:
            response = {'message': 'You need provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
