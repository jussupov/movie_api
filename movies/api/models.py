from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Genre(models.Model):
    created = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Movie(models.Model):
    created = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=155)
    description = models.TextField()
    image = models.TextField()
    year = models.CharField(max_length=150)
    genre = models.ForeignKey(Genre, related_name='movies', on_delete=models.CASCADE, default=None)

    def avg_rating(self):
        sum = 0
        ratings = Rating.objects.filter(movie=self)
        for rating in ratings:
            sum += rating.rate
        if len(ratings) > 0:
            return sum / len(ratings)
        else:
            return 0


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    class Meta:
        unique_together = (('user'), ('movie'))
        index_together = (('user'), ('movie'))
