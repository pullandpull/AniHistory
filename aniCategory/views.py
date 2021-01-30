from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse 
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required as lr


#Model // form imports 
from aniCategory.forms import UserForm,UserLoginForm

#global imports
import json
import os
#3rd party imports
import requests
from pprint import pprint

# Create your views here.

def index(request):
    
    return render(request,'aniCategory/index.html',{})

def user_login(request): 
    context_dict = {}
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else: 
                context_dict['stats'] = 'Account is Disabled'
        else:
            context_dict['stats'] = 'Incorrect Username or Password'
    else: 
        context_dict['user_login_form'] = UserLoginForm()
    
    return render(request,'aniCategory/login.html',context_dict)
    
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    context_dict = {}
    register_stat = False 
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        
        if user_form.is_valid(): 
            user = user_form.save(commit = True)
            user.set_password(user.password)
            user.save()
            register_stat = True
            return HttpResponseRedirect(reverse('index'))
        else: 
            print(user_form.errors)
    else: 
        user_form = UserForm()

    context_dict['user_form'] = user_form
    context_dict['register_stat'] = register_stat

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
            pprint(json_data)
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
            pprint(json_response)
            if request_type == 'recommendations': 
                context_dict['results'] = json_response['recommendations']
            else: 
                context_dict['results'] = json_response['articles']
        else:
            pass
    else:
        pass

    return render(request, 'aniCategory/search_results.html', context_dict)
    '''
    response = requests.get(endpoint + query)
    response.raise_for_status()
    
    json_data = json.loads(response.text)
    pprint(json_data['archive'][:10])
    context_dict['archives'] = json_data['achive'][:11]  
    return render(request,'aniCategory/search_results.html',context_dict)
    '''
