import random, string

from django.contrib.auth.models import User
from django.db import models

def key_generator(size=32, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

class UserApiKeyManager(models.Manager):
	def generate_key(self, user):
			'''
				Generates a random, UNQUE API key for the user object and saves it
			'''
			# Generate the key
			key = key_generator()

			# Keep generating keys until the key is unique
			while UserApiKey.objects.filter(api_key__exact=key).count() != 0:
				key = key_generator

			# Set and save
			k = UserApiKey(user=user)
			k.api_key = key
			k.save()

			return k

class UserApiKey(models.Model):
	'''
		This model stores a Geekdom API key for the user
	'''
	user = models.OneToOneField(User, unique=True, verbose_name=('user'))
	api_key = models.CharField(max_length=256, null=True, blank=True)

	objects = UserApiKeyManager()