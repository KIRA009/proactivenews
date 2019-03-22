from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
import uuid


class UserManager(BaseUserManager):
	def create_user(self, api_key, password, **extra_details):
		"""
		Creates and saves a User with the given contact, password, name, gender, location_id
		"""

		extra_details['is_superuser'] = False
		extra_details['is_staff'] = False

		user = self.model(api_key=api_key, **extra_details)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, api_key, password, **extra_details):
		"""
		Creates and saves a user with the given email, password
		"""

		extra_details['is_superuser'] = True

		user = self.model(api_key=api_key, **extra_details)
		user.set_password(password)
		user.save(using=self._db)
		return user


class User(AbstractBaseUser, PermissionsMixin):
	name = models.CharField(max_length=255, default=None, unique=False, null=True)
	api_key = models.CharField(unique=True, null=False, max_length=255)
	is_staff = models.BooleanField(default=False)
	USERNAME_FIELD = 'api_key'
	REQUIRED_FIELDS = ['name']

	objects = UserManager()


class Profile(models.Model):
	unique_id = models.UUIDField(primary_key=True, editable=False, auto_created=True, default=uuid.uuid4)
	profile = models.OneToOneField(User, to_field='api_key', on_delete=models.CASCADE)
	country = models.TextField(default=None, null=True)

	objects = models.Manager()


class SavedNews(models.Model):
	user = models.ForeignKey(User, to_field='api_key', on_delete=models.CASCADE, null=True)
	title = models.TextField(null=True)
	image = models.URLField(null=True)
	author = models.CharField(max_length=256, null=True)
	description = models.TextField(null=True)
	content = models.TextField(null=True)
	url = models.URLField(null=True)
	date_saved = models.DateTimeField(auto_now_add=True)
