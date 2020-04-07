"""movies_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from movies_lib.views import handle_movies, handle_comments, filter_by_movie, top_movies
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),  # admin pass=demo123
    path('', RedirectView.as_view(url='movies/')),
    path('movies/', handle_movies),
    path('comments/', handle_comments),
    path('comments/<int:movie_id>', filter_by_movie),
    path('top/', top_movies),
]
