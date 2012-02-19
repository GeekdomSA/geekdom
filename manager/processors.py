from django.template import Context
from manager.models import BackgroundImage
from django.contrib.auth.models import User

def flickr_background(request):
  try:
    background_image = BackgroundImage.objects.order_by('?')[0].url
  except:
    background_image = []
  
  return {'background_image' : background_image }


def all_users(request):
	all_users = User.objects.filter(is_active = True).order_by('first_name')
	return {'all_users':all_users}


def check_for_checkin_cookie(request):

	if request.user.is_authenticated():
		if not request.user.userprofile.is_checked_in():
			try: 
				test = request.COOKIES['asked_for_checkin']
				return {'needs_to_check_in': False}
			except:
				return {'needs_to_check_in': True}
	else:
		return {'needs_to_check_in': False}
