from django.db import models
from django.utils import timezone


class MovieItem(models.Model):
	title = models.TextField(max_length=50, blank=False)
	year = models.TextField(max_length=4, default='null')
	director = models.TextField(max_length=50, default='Unknown')
	poster = models.TextField(default='Not available')
	full_data = models.TextField(default='No data')

	def __str__(self):
		return self.title


class CommentItem(models.Model):
	movie_id = models.ForeignKey(MovieItem, on_delete=models.CASCADE)
	date = models.DateTimeField(default=timezone.now)
	body = models.TextField(default='No data')
