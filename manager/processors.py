from django.template import Context
from django.contrib.auth.models import User
from manager.models import *

# def flickr_background(request):
#   try:
#     background_image = BackgroundImage.objects.order_by('?')[0].url
#   except:
#     background_image = []
  
#   return {'background_image' : background_image }


def all_users(request):
	all_users = User.objects.filter(is_active = True).order_by('first_name')
	return { 'all_users' : all_users }


def check_for_checkin_cookie(request):

	needs_to_check_in = False

	if request.user.is_authenticated():
		if not request.user.my_profile.is_checked_in():
			try: 
				test = request.COOKIES['asked_for_checkin']
			except:
				needs_to_check_in = True
	
	return { "needs_to_check_in" : needs_to_check_in }