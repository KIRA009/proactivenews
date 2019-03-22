from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

cache_time = 60 * 60

urlpatterns = [
	path('', redirect_to_news, name='index'),
	path('register/', Register.as_view(), name='register'),
	path('login/', Login.as_view(), name='login'),
	path('home/', login_required(Home.as_view()), name='home'),
	path('category/<str:category>/', cache_page(cache_time)(login_required(Category.as_view())), name='category'),
	path('saved/', login_required(Saved.as_view()), name='saved'),
	path('account/', login_required(Account.as_view()), name='account'),
	path('logout/', login_required(Logout.as_view()), name='logout'),
]
