from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required as lr
from django.contrib.auth.models import User

from aniCategory.models import Anime_Bookmarks

#Model // form imports 
from aniCategory.forms import UserForm,UserLoginForm

#global imports
import json
import os
import re
#3rd party imports
import requests
from pprint import pprint

# Create your views here.

def index(request):
    
    return render(request,'aniCategory/index.html',{})

def user_login(request): 
    context_dict = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username , password = password ) 
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                context_dict['user_stats'] = 'Account is Disabled'
        else: 
            context_dict['user_stats'] = 'Incorrect Username or Password' 
    user_login_form = UserLoginForm()

    context_dict['login_form'] = user_login_form 

    return render(request, 'aniCategory/login.html', context_dict )
                    
        
    
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    context_dict = {}
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        re_password = request.POST['re_password']
        if re_password == request.POST['password']:
            if user_form.is_valid(): 
                #set password to hashed
                user = user_form.save(commit = True)
                user.set_password(user.password)
                user.save()
                registered = True
                context_dict['stats'] = registered
            else: 
                print(user_form.errors)
        else: 
            print(user_form.add_error('re_password','Password does not match!'))
            context_dict['password'] = 'Password did not match!'
    else:
        user_form = UserForm()
    
    context_dict['stats'] = registered
    context_dict['form'] = user_form 
    return render(request,'aniCategory/register.html',context_dict)


def anime_search(request):
    endpoint = r'https://api.jikan.moe/v3'
    context_dict = {}
    if request.method == 'GET':
        query = request.GET['query']
        if query:
            response = requests.get(endpoint + '/search/anime?q={}&page=1'.format(query))
            response.raise_for_status()
            json_data = json.loads(response.text)
            context_dict['results'] = json_data['results'] 
          
        else:
            pass
    else:
        pass

    return render(request,'aniCategory/search_results.html',context_dict)


def show_archive(request):
    context_dict = {}
    endpoint = r'https://api.jikan.moe/v3/season/'
    if request.method == 'GET': 
        season = request.GET['season']
        year = request.GET['year']
        if season and year:
            response = requests.get(endpoint + str(year) + '/' + season)
            response.raise_for_status()
            json_data = json.loads(response.text)
            context_dict['results'] = json_data['anime']
        else:
            pass
    else: 
        pass

    return render(request,'aniCategory/search_results.html',context_dict)
            

def show_recommended(request): 
    context_dict  = {}
    endpoint = r'https://api.jikan.moe/v3/anime/1/'
    if request.method == 'GET': 
        request_type = request.GET['session_request']
        response = requests.get(endpoint + request_type)
        response.raise_for_status()

        if response.status_code == requests.codes.ok: 
            json_response = json.loads(response.text)
            if request_type == 'recommendations': 
                context_dict['results'] = json_response['recommendations']
            else: 
                context_dict['results'] = json_response['articles']
        else:
            pass
    else:
        pass

    return render(request, 'aniCategory/search_results.html', context_dict)


# to be added after..
def show_anime_info(request): 
    context_dict  = {}
    endpoint = r'https://api.jikan.moe/v3/anime/'
    
    if request.method == 'GET': 
        mal_id = request.GET.get('mal_id')
        if mal_id: 
            try:
                response = requests.get(endpoint + '/' + mal_id )
                response.raise_for_status()
                json_data = json_loads(response.text)
                pprint(json_data)

            except Exception as err:
                print(err)
        else:
            context_dict['data'] = None
    
    return render(request,'aniCategory/search_anime.html',context_dict)

#Streaming anime API part
def get_key():
    with open('id.key') as key_obj:
        key = key_obj.read()
    return key

#Bookmark views
#Title rename
def re_title(title = None): 
    reg_title_obj = re.compile(r'episode \d+?', re.I)
    res_title = reg_title_obj.sub(r'',title)
    return res_title

#Show bookmarks
def show_bookmarks(user = None):
    bookmarks = Anime_Bookmarks.objects.filter(user = user)
    return bookmarks
#Get Bookmarks
def get_bookmarks(user = None):
    bookmarks_list = []
    bookmarks = Anime_Bookmarks.objects.filter(user = user)
    for anime in bookmarks:
        bookmarks_list.append(anime.anime_title)

    print(bookmarks_list)
    
    return bookmarks_list

def add_bookmark(request): 

    if request.method == 'GET': 
        anime_name = request.GET.get('anime_name',None)
        re_anime_title = re_title(anime_name)
        print(re_anime_title)
        anime_cover = request.GET.get('anime_cover',None)
        anime_vid_id = request.GET.get('anime_video_id',None)
        user_id = request.GET.get('user_id',None)

        if request.user.id == int(user_id):
            bookmark,stats = Anime_Bookmarks.objects.get_or_create(anime_title = anime_name, \
            clean_title = re_anime_title,
            anime_cover = anime_cover,
            anime_vid_id = anime_vid_id,
            user = request.user
            )
            if stats == True: 
                bookmark.save()
                status = 'True'
                print('Added')

            elif stats == False:
                bookmark.delete()
                status = 'False'
                print('Deleted')

            else: 
                pass
                print('passed')

        else: 
            raise Exception('Invalid')

    return HttpResponse(status)

def stream_anime_search(request): 

    endpoint = r'https://simpleanime.p.rapidapi.com/anime/search/'

    key = get_key()

    if request.method == 'GET':
        query = request.GET.get('search_anime', None)
        context_dict = {}
        if key:    
            headers = {
                'x-rapidapi-key': key,
                 'x-rapidapi-host': "simpleanime.p.rapidapi.com"
            }
        else: 
            print('Key not found ')

        if not query == None: 
            response = requests.get(endpoint + query , headers = headers )
            response.raise_for_status()
            json_data = json.loads(response.text)
            context_dict['animes'] = json_data['data']
            pprint(context_dict['animes'])
            
        else:
            pass
    
    return render(request,'aniCategory/stream_anime_by_search.html', context_dict)

def stream_anime_latest(request):
    context_dict = {}
    endpoint = r'https://simpleanime.p.rapidapi.com/anime/list/recent' 
    key = get_key()

    if request.user.is_authenticated:
        context_dict['bookmarks'] = get_bookmarks(request.user)
    else:
        context_dict['bookmarks'] = None

    print(context_dict['bookmarks'])

    if request.method == 'GET': 
        if key: 
            headers = {
               'x-rapidapi-key': key, 
               'x-rapidapi-host' :  "simpleanime.p.rapidapi.com"
            }

            response = requests.get(endpoint, headers = headers)
            response.raise_for_status()
            json_data = json.loads(response.text)

            context_dict['animes'] = json_data['data']
        else:
            print('Key not found')
    
    return render(request, 'aniCategory/stream_anime_search.html',context_dict)


def stream_anime_by_id(request):
    endpoint = r'https://simpleanime.p.rapidapi.com/anime/info/videos/'
    context_dict = {}
    
    key = get_key()
    
    if request.method == 'POST':
        vid_id = request.POST.get('watch')
        if vid_id:
            if key:
                headers = {
                    'x-rapidapi-key': key, 
                    'x-rapidapi-host' :  "simpleanime.p.rapidapi.com"
                }

                response = requests.get(endpoint + vid_id, headers = headers)
                response.raise_for_status()

                json_data = json.loads(response.text)
                context_dict['data'] = json_data['data'][0]
                context_dict['episodes'] = json_data['episode']
                pprint(json_data)

            else:
                print('Key not found')
        else:
            print('Failed to get Video id ')
    
    return render(request,'aniCategory/stream_anime.html',context_dict)

def stream_anime_by_link(request,video_id):
    endpoint = r'https://simpleanime.p.rapidapi.com/anime/info/videos/'
    context_dict = {}
    key = get_key()
    if key: 
        headers = {
            'x-rapidapi-key': key, 
            'x-rapidapi-host' :  "simpleanime.p.rapidapi.com"    
        }
    else:
        headers = None
        print('Key not found')

    if video_id: 
        try:
            response = requests.get(endpoint + video_id , headers = headers)
            response.raise_for_status()
            json_data = json.loads(response.text)
            pprint(json_data)
            context_dict['data'] = json_data['data'][0]
            context_dict['episodes'] = json_data['episode']

        except Exception as err:
            print(err)
    else:
        pass

    return render(request,'aniCategory/stream_anime.html', context_dict)