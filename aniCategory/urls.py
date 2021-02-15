from django.urls import path

#2nd party imports
from aniCategory import views


urlpatterns = [
    path('',views.index, name = 'index'),
    #anime related stuffs
    path('search/',views.anime_search, name = 'anime_search'),
    path('archive/',views.show_archive , name = 'show_archive'),
    path('recommended/',views.show_recommended , name ='show_recommeded'),
    #account related stuffs
    path('register/',views.register, name = 'register'),
    path('login/',views.user_login, name = 'login'), 
    path('logout/',views.user_logout, name = 'logout'), 
    #streaming anime related stuffs
    path('stream/anime/', views.stream_anime_by_id, name = 'stream_anime_by_id'), 
    path('stream/anime/search/',views.stream_anime_search, name = 'stream_anime_search'),
    path('stream/anime/latest/', views.stream_anime_latest, name = 'stream_anime_latest'),
    path('stream/anime/bookmark/',views.add_bookmark, name = 'add_bookmark'),
    path('stream/anime/id/<path:video_id>/',views.stream_anime_by_link, name = 'stream_anime_by_link'),

    path('account/anime/bookmarks/', views.get_anime_bookmarks, name = 'my_bookmarks'),
    path('account/anime/bookmarks/search/',views.find_by_name, name = 'find_by_anime'),
]
