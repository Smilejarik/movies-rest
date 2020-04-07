from django.shortcuts import render
from .models import MovieItem, CommentItem
from django.http import HttpResponseRedirect, HttpResponse
import requests
from django.db.models import Count
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
	for elt in dictionary:
		return elt.get(key)

# omdapi.com API key
api_key = 'apikey=8a9a1640'


def handle_movies(request):
	all_movies = MovieItem.objects.all()

	# request from external api on POST
	if request.method == 'POST':
		try:
			sorting_way = request.POST['sorting_way']
			if sorting_way == 'top_comments':
				all_movies = all_movies.annotate(comments_count=Count('commentitem')).order_by('comments_count').reverse()
			else:
				all_movies = all_movies.order_by(sorting_way)

			return render(request, "movies.html", {'all_movies': all_movies})
		except Exception:
			pass

		title_to_add = request.POST['movie_title']

		response = requests.get(f'http://www.omdbapi.com/?t={title_to_add}&{api_key}')
		if response.status_code != 200:
			return HttpResponse(request, f"<h2>Can't request API, code: {response.status_code}</h2>")

		json_data = response.json()

		# validate if have Title in response
		try:
			if json_data['Response'] == "True":
				new_movie = MovieItem(
						title=json_data['Title'],
						year=json_data['Year'],
						director=json_data['Director'],
						poster=json_data['Poster'],
						full_data=json_data,
					)
				new_movie.save()
		except Exception:
			return HttpResponse("<h2>No such movie in DB</h2>")
		
		return render(request, "added.html", {'new_movie': json_data})

	return render(request, "movies.html", {'all_movies': all_movies})


def handle_comments(request):
	all_comments = CommentItem.objects.all()

	# request from external api on POST
	if request.method == 'POST':
		try:
			movie_id = request.POST['movie_id']
			comment_body = request.POST['comment_body']
			movie = MovieItem.objects.get(pk=movie_id)

			new_comment = CommentItem(
						movie_id=movie,
						body=comment_body,
					)
			new_comment.save()

			#return render(request, "comments.html", {'all_comments': all_comments})
		except Exception:
			return HttpResponse("<h3>Wrong kwargs in your request</h3>")
	elif request.method == "GET":
		if len(all_comments) == 0:
			return HttpResponse("<h3>No Comments</h3>")

	return render(request, "comments.html", {'all_comments': all_comments})


def filter_by_movie(request, movie_id):
	try:
		movie = MovieItem.objects.get(pk=movie_id)
		movie_comments = CommentItem.objects.filter(movie_id=movie)

		return render(request, "comments.html", {'movie_comments': movie_comments})
	except Exception:
		return HttpResponse("<h3>Error: No such movie</h3>")


def top_movies(request):
	if request.method == "POST":
		try:
			start_range = 0000
			end_range = 9999
			start_range = int(request.POST['start_range'])
			end_range = int(request.POST['end_range'])
			all_movies = MovieItem.objects.filter(year__range=[start_range, end_range])
		except Exception:
			return HttpResponse("<h3>Error: incorrect range</h3>")
	else:
		all_movies = MovieItem.objects.all()

	if len(all_movies) == 0:
		return HttpResponse("<h3>Error: no movies in this range</h3>")

	all_movies = all_movies.annotate(comments_count=Count('commentitem')).order_by('comments_count').reverse()

	curr_comments = all_movies[0].commentitem_set.count()  # define max nr of comments for first place
	top_array = []
	rank = 1
	for movie in all_movies:
		nr_comments = movie.commentitem_set.count()
		if nr_comments < curr_comments:
			curr_comments = nr_comments
			rank += 1

		movie_rank = {
			"movie_id": movie.id,
			"total_comments": nr_comments,
			"rank": rank
		}

		top_array.append(movie_rank)

	return render(request, "top.html", {'top_array': top_array})
