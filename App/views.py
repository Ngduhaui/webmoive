from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm, CommentForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Movie, Comment, Genre, CustomUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.core.serializers import serialize
from itertools import cycle
from datetime import date, timedelta
import os
# Create your views here.


def genre_data():
    genres = Genre.objects.all()
    drops = [
        {'name': genre.name, 'genreID': genre.genreID}
        for genre in genres
    ]
    return drops

def card_data(movies):
    cards_data = [
        {
            'title': movie.title,
            'movieID': movie.movieID,
            'imageURl': movie.imageURl,
            'releaseDate': movie.releaseDate,
        }
        for movie in movies
    ]
    return cards_data

def findmovie(request):
    genre_id = request.GET.get('genreID')
    movies= Movie.objects.filter(genreID=genre_id)
    genre_name = get_object_or_404(Genre, genreID=genre_id)
    content = {
        'drops': genre_data(),
        'data_movie': card_data(movies),
        'username': request.user.username,
        'name': genre_name, 
    }
    return render(request, 'find_movie.html', content)


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
        
    content = {
        'drops': genre_data(),
        'form': form,
    }
    return render(request, 'signup.html', content)
# login page
def user_login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    content = {
        'drops': genre_data(),
    }
    return render(request, 'login.html', content)

        
# logout page
def user_logout(request):
    logout(request)
    return redirect('login')

def profile(request):
    link = [
        'https://lh3.googleusercontent.com/pZwZJ5HIL5iKbA91UGMUIPR0VJWa3K0vOGzDZmY6wU3EJBUdfsby3VEyxU162XxTyOyP3D154tjkr-4Jgcx8lygYUR8eB-jVmld4dsHi1c-mE_A8jKccseAG7bdEwVrcuuk6ciNtSw=s170-no',
        'https://lh3.googleusercontent.com/oUUiPB9sq3ACq4bUaRmo8pgvC4FUpRRrQKcGIBSOsafawZfRpF1vruFeYt6uCfL6wGDQyvOi6Ez9Bpf1Fb7APKjIyVsft7FLGR6QqdRFTiceNQBm1In9aZyrXp33cZi9pUNqjHASdA=s170-no',
        'https://lh3.googleusercontent.com/pZwZJ5HIL5iKbA91UGMUIPR0VJWa3K0vOGzDZmY6wU3EJBUdfsby3VEyxU162XxTyOyP3D154tjkr-4Jgcx8lygYUR8eB-jVmld4dsHi1c-mE_A8jKccseAG7bdEwVrcuuk6ciNtSw=s170-no'
            ]
    cards_data = [
        {'link': link[0], 'name_alt': 'name alt', 'card_image': 'card image', 'card_name': 'card name'},
        {'link': link[1], 'name_alt': 'name alt', 'card_image': 'card image', 'card_name': 'card name'},
        {'link': link[2], 'name_alt': 'name alt', 'card_image': 'card image', 'card_name': 'card name'}
    ]
    context = {
        'cards': cards_data,
        'drops': genre_data(),
    }
    return render(request, 'profile.html', context)

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    # Fetch comments ordered by creation time in descending order

    items_per_page = 5
    all_comments = Comment.objects.filter(movieID=movie).order_by('-commentID')

    paginator = Paginator(all_comments, items_per_page)
    page = request.GET.get('page')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            Comment.objects.create(username=request.user, movieID=movie, content=content)
            return HttpResponseRedirect(request.path_info)  # Redirect to the same page after form submission
    else:
        form = CommentForm()

    try:
        comments_page = paginator.page(page)
    except PageNotAnInteger:
        comments_page = paginator.page(1)
    except EmptyPage:
        comments_page = paginator.page(paginator.num_pages)
    content = {
        'movielist':[(int(movie_id) + int(i)) for i in range(3)],
        'movie': movie,
        'comments': comments_page,
        'form': form,
        'username': request.user.username,
        'drops': genre_data(),
    }
    return render(request, 'movie_detail.html', content)

def home(request):
    all_movies = Movie.objects.order_by('-movieID')
    movies_per_page = 6
    page = request.GET.get('page', 1)
    paginator = Paginator(all_movies, movies_per_page)

    try:
        # Get the current page's movie data
        paginated_cards = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_cards = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        paginated_cards = paginator.page(paginator.num_pages)

    context = {
        'author': request.user.is_authenticated,
        'username': request.user.username,
        'paginated_cards': paginated_cards,
        'current_page': int(page),
        'pages': range(1, paginator.num_pages + 1),
        'drops': genre_data(),  # Assuming genre_data() is a function that returns data for drops
    }

    return render(request, 'home.html', context)

def add_movie(request):
    images = [os.path.join("thumbnails", f"{i}.jpg").replace("\\", "/") for i in range(1, 6)]
    
    genres = [genre for genre in Genre.objects.all()]
    
    image_cycle = cycle(images)
    
    genre_cycle = cycle(genres)
    for i in range(30):
        movie_data = {
            "title": f"Phim {i}",
            "description": f"Your Movie Description {i}",
            "releaseDate": '2024-01-05',
            'duration': timedelta(minutes=90),
            "thumbnail": next(image_cycle),
            "genreID": next(genre_cycle),
        }
        print(movie_data)
        movie = Movie.objects.create(**movie_data)
        
    return redirect('home')

def delete_movie(request):
    delete = Movie.objects.all().delete()
    print(delete)
    return redirect('home')


def add_comments(request):
    users = CustomUser.objects.all()
    movies = Movie.objects.all()
    contents = [f'Hello EveryOne {i}' for i in range(300)]
    
    print(users)
    print(movies)
    print(contents)
    
    username = cycle(users)
    movieID = cycle(movies)
    content = cycle(contents)
    
    for i in range(300):
        comment_data = {
            "username": next(username),
            "movieID": next(movieID),
            "content": next(content),
        }
        print(comment_data)
        comments = Comment.objects.create(**comment_data)
        
    return redirect('home')

def del_comments(request):
    delete = Comment.objects.all().delete()
    print(delete)
    return redirect('home')