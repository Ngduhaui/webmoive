# urls.py in your "myapp" app

from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('movie_detail/<str:movie_id>/', views.movie_detail, name='movie_detail'),
    path('findmovie/', views.findmovie, name='findmovie'),
    path('addmovie/', views.add_movie, name='addmovie'),
    path('deletemovie/', views.delete_movie, name='deletemovie'),
    path('addcomments/', views.add_comments, name='addcomments'),
    path('delcomments/', views.del_comments, name='delcomments')
]
