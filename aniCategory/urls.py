from django.urls import path

#2nd party imports
from aniCategory import views


urlpatterns = [
    path('',views.index, name = 'index'),
    path('search/',views.anime_search, name = 'anime_search'),
    path('archive/',views.show_archive , name = 'show_archive'),
    path('recommended/',views.show_recommended , name ='show_recommeded'),
]
