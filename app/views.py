from django.shortcuts import render, redirect
from .news_api import resources, api
from django.views import View
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from app.helpers import clean_dict
import requests


# 35db69b8abc947d2b2f0d6d2e78d829c


class Register(View):
	def get(self, request):
		user = request.user
		if not user.is_anonymous:
			return redirect('home')
		return render(request, 'register.html', {'url': self.__class__.__name__.lower(), 'countries': resources.countries})

	@staticmethod
	def post(request):
		info = request.POST.copy()
		if not clean_dict(info)[0]:
			info['status'] = 'failure'
			info['error'] = f'Parameter {clean_dict(info)[1]} has not been fulfilled'
		else:
			try:
				User.objects.get(api_key=info['api_key'])
				info['status'] = 'failure'
				info['error'] = 'API KEY is already registered'
			except User.DoesNotExist:
				res = requests.get('https://newsapi.org/v2/top-headlines?country=arg&apiKey=' + info['api_key']).json()
				if res['status'] != 'error':
					try:
						User.objects.get(name=info['name'])
						info['status'] = 'failure'
						info['error'] = 'Username already taken'
					except User.DoesNotExist:
						user = User.objects.create_user(api_key=info['api_key'], password=info['password'], name=info['name'])
						Profile.objects.create(profile=user)
				else:
					info['status'] = 'failure'
					info['error'] = 'API KEY is not correct'
		return JsonResponse(info)


class Login(View):
	def get(self, request):
		user = request.user
		if not user.is_anonymous:
			return redirect('home')
		return render(request, 'login.html', {'url': self.__class__.__name__.lower()})

	@staticmethod
	def post(request):
		info = request.POST.copy()
		if not clean_dict(info)[0]:
			info['status'] = 'failure'
			info['error'] = f'Parameter {clean_dict(info)[1]} has not been fulfilled'
		else:
			try:
				user = User.objects.get(name=info['name'])
				print(info['password'])
				user = authenticate(username=user.api_key, password=info['password'])
				if user is not None:
					login(request, user)
					if user.profile.country is None:
						info['url'] = 'account'
					else:
						info['url'] = 'home'
				else:
					info['status'] = 'failure'
					info['error'] = 'Wrong password'
			except User.DoesNotExist:
				info['status'] = 'failure'
				info['error'] = 'Username not registered'
		return JsonResponse(info)


class Home(View):
	def get(self, request):
		user = request.user
		news = api.News(user.api_key).get_news('top-headlines', country=user.profile.country)
		# news = pickle.load(open('sample_news', 'rb'))
		# print(type(news))
		return render(request, 'home.html', {'url': self.__class__.__name__.lower(), 'user': user, 'articles': news['articles'], 'categories': resources.categories})


class Category(View):
	def get(self, request, category):
		user = request.user
		category = category
		if category not in resources.categories:
			return redirect('home')
		news = api.News(user.api_key).get_news('top-headlines', country=user.profile.country, category=category)
		# news = pickle.load(open('sample_news', 'rb'))
		return render(request, 'home.html', {'url': self.__class__.__name__.lower(), 'user': user,
		                                     'articles': news['articles'], 'categories': resources.categories,
		                                     'title': category.title()})


class Saved(View):
	def get(self, request):
		user = request.user
		saved_articles = SavedNews.objects.filter(user=user).order_by('-date_saved')
		articles = []
		for article in saved_articles:
			articles.append({'urlToImage': article.image, 'title': article.title, 'author': article.author,
			                 'description': article.description, 'content': article.content, 'url': article.url})
		return render(request, 'saved.html', {'url': self.__class__.__name__.lower(), 'user': user,
		                                      'articles': articles, 'categories': resources.categories})

	@staticmethod
	def post(request):
		user = request.user
		article = eval(request.POST['article'])
		response = dict()
		if request.POST['action'] == 'save':
			SavedNews.objects.get_or_create(user=user, title=article['title'], image=article['urlToImage'],
			                                author=article['author'], description=article['description'],
			                                content=article['content'], url=article['url'])
			response['message'] = 'Saved'
		else:
			SavedNews.objects.get(user=user, title=article['title'], image=article['urlToImage'],
			                      author=article['author'], description=article['description'],
			                      content=article['content'], url=article['url']).delete()
			response['message'] = 'Save'
		return JsonResponse(response)


class Account(View):
	def get(self, request):
		user = request.user
		return render(request, 'account.html', {'url': self.__class__.__name__.lower(), 'user': user,
		                                        'countries': resources.countries})

	@staticmethod
	def post(request):
		user = request.user
		info = request.POST
		if authenticate(username=user.api_key, password=info['password']) is not None:
			user.profile.country = info['country']
			user.profile.save()
		return redirect('account')


class Logout(View):
	@staticmethod
	def get(request):
		logout(request)
		return redirect('login')


def redirect_to_news(request):
	return render(request, 'main.html')
