import requests
from .resources import base_url


class News:
	"""
	top-headlines
	country, category, q


	"""
	def __init__(self, api_key):
		self.api_key = api_key

	def get_news(self, news_type, **kwargs):
		url = base_url.replace('{type}', news_type).replace('{api_key}', self.api_key)
		url = News.add_to_url(url, **kwargs)
		return News.make_request(url)

	@staticmethod
	def add_to_url(url, **kwargs):
		url = url
		for item in kwargs:
			url += f'&{item}={kwargs[item]}'
		return url

	@staticmethod
	def make_request(url):
		return requests.get(url).json()
