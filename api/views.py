import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from geekdom.api.models import UserApiKey

@login_required
def generate_key(request):
	'''
		This view handles the generating of an API key for the user
	'''
	if request.method == "GET":
		try:
			k = UserApiKey.objects.get(user=request.user)
		except:
			k = UserApiKey.objects.generate_key(request.user)

		if k.api_key != None:
			return HttpResponse(k.api_key)
		else:
			return HttpResponse("Error generating key")

@csrf_exempt
def checkin(request):
	'''
		Checks a user in to geekdom
		URL: /api/users/checkin/
		Method: POST
		ARGS:	user_id 	-	The user's ID as is in the geekdom database 
				api_key 	-	Issued API key
	'''
	if request.method == "POST":
		key = request.POST["api_key"]
		user_id = request.POST["user_id"]

		try:
			k = UserApiKey.objects.get(api_key=key)
		except:
			return HttpResponse("Invalid API Key: " + str(key))

		try:
			u = User.objects.get(id=user_id)
		except:
			return HttpResponse("Invalid username: " + str(user_id))
		
		# Check user in
		u.get_profile().check_in(method=5)
		return HttpResponse("User checked in")
		
	else:
		return HttpResponse("Need to use POST for this one.")

def get_user_id(request, username):
	'''
		Returns a user profile given a username
		URL: /api/users/get/user_id/<username>/?api_key=API_KEY
		Method: GET
		ARGS:	username	- 	The user's geekdom username
				api_key 	- 	Issued API Key
	'''
	if request.method == "GET":
		try:
			key = request.GET.get('api_key', '')
		except:
			return HttpResponse("No API Key passed")

		try:
			k = UserApiKey.objects.get(api_key=key)
		except:
			return HttpResponse("Invalid API Key: " + key)

		try:
			u = User.objects.get(username=username)
		except:
			return HttpResponse("Invalid username: " + username)

		d = {}
		d["id"] = u.id
		d["username"] = u.username
		d["first_name"] = u.first_name
		d["last_name"] = u.last_name
		d["email"] = u.email
		# You can add more things from the profile as well
		# p = u.get_profile()
		# d["room_number"] = p.room_number
		return HttpResponse(json.dumps(d))