from manager.forms import *
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, Http404, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.template.defaultfilters import date as django_date_filter
from django.views.decorators.csrf import csrf_exempt

from manager.admin_views import *

import datetime

# handle 403 error
def error_403handler(request):
  return render_to_response('global/generic.html',{
      'title': "Hey! 403!",
      'subtitle': "You don't have permission to do that.",
    },context_instance=RequestContext(request))

# handle 404 error
def error_404handler(request):
  return render_to_response('global/generic.html',{
      'title': "404! Oh no!",
      'subtitle': "How embarassing! We can't seem to find that thing.",
    },context_instance=RequestContext(request))

# handle 500 error
def error_500handler(request):
  return render_to_response('global/generic.html',{
      'title': "Oops, 500?",
      'subtitle': "Something may or may not have broken somewhere.",
    },context_instance=RequestContext(request))




# user homepage
# if kiosk=True is passed, use kiosk template
def homepage(request, kiosk=False):
  now = datetime.datetime.now()
  users = User.objects.filter(my_profile__checkin__expires_at__gte = now).order_by('first_name').distinct()
  all_users = User.objects.filter(is_active = True).order_by('first_name')

  return render_to_response(
    'kiosk/homepage.html',
    { 
      'users': users, 
      'all_users':all_users, 
      'kiosk':kiosk,
      'title':'Currently here: <em>' + str(users.count()) + ' Members</em>'
    }, 
    context_instance=RequestContext(request))



def user_checkin(request):
  if request.user.my_profile.check_in(method = "desktop"):
    message = "Thanks for checking in, " + request.user.first_name + "! Welcome to Geekdom."
    messages.add_message(request, messages.SUCCESS, message)
  else:
    message = "You were already checked in, but thanks anyway!"
    messages.add_message(request, messages.SUCCESS, message)  
  return HttpResponseRedirect("/")




def user_checkout(request):
  if request.user.my_profile.check_out():
      message = "Thanks for checking out, " + request.user.first_name + "! Come back soon!"
      messages.add_message(request, messages.SUCCESS, message)
  else:
    message = "That was weird, you probably weren't checked in!"
    messages.add_message(request, messages.ERROR, message)

  return HttpResponseRedirect("/")



from dateutil import parser
import feedparser
def all_events(request, kiosk=False):
  today = datetime.date.today()
  now = datetime.datetime.now()

  twitterfeed = feedparser.parse("http://search.twitter.com/search.atom?q=geekdom")
  tweets = []
  for tweet in twitterfeed.entries: tweets.append(tweet)
  for tweet in tweets: tweet.pp = parser.parse(tweet.published).strftime("%m/%d/%y %H:%M:%S")

  if request.user.is_superuser:
    events = Event.objects.filter(ends_at__gte = now).order_by('starts_at')
  else:
    events = Event.objects.filter(ends_at__gte = now).order_by('starts_at').filter(private_event = False)

  return render_to_response(
    'kiosk/all_events.html',
    { 
      'events': events, 
      'today': today, 
      'tweets':tweets, 
      'kiosk':kiosk, 
      'title': 'Upcoming events at <em>Geekdom</em>',
    }, 
    context_instance=RequestContext(request))




def search(request, kiosk=False):
  try: query = request.GET['query']
  except: query = ""

  users_unsorted = User.objects.filter(
    Q(first_name__icontains = query) | 
    Q(last_name__icontains = query) | 
    Q(my_profile__skills__icontains = query) |
    Q(my_profile__company_name__icontains = query)
  )

  users = []

  for user in users_unsorted:
    if user.my_profile.is_checked_in():
      users.insert(0, user)
    else:
      users.append(user)


  return render_to_response(
      'kiosk/homepage.html',
      {
          'title': "Search: " + query,
          'subtitle': str(len(users)) + " members found.",
          'users' : users,
          'kiosk': kiosk,
      }, 
      context_instance=RequestContext(request)
  )


def logout_user(request):
  message = "See you later, " + request.user.first_name + "!"
  messages.add_message(request, messages.SUCCESS, message)
  logout(request)
  response = HttpResponseRedirect("/")
  response.delete_cookie('asked_for_checkin')
  return response




def view_event(request, event_id):
  now = datetime.datetime.now()

  event = Event.objects.get(id=event_id)
  events = Event.objects.filter(ends_at__gte = now).order_by('starts_at').exclude(id = event.id)

  return render_to_response(
      'kiosk/event_detail.html',
      {
          'title': event.name,
          'subtitle': 
            django_date_filter(event.starts_at, 'l, F jS') + 
            " from " + django_date_filter(event.starts_at, ("P")) + 
            " until " + django_date_filter(event.ends_at, ("P")),
          'event' : event,
          'events':events,
      }, 
      context_instance=RequestContext(request)
  )


def kiosk_user_view(request, user_id):

  user = User.objects.get(id = user_id)

  return render_to_response(
      'userena/profile_detail.html',
      {
          'profile' : user.my_profile,
          'kiosk': True,
      }, 
      context_instance=RequestContext(request)
  )
  

@csrf_exempt
def flomio_toggle_check_in(request):
    ''' Toggles the check-in status for the given user (via tag UUID) '''
    
    tag_uuid = request.POST.get('tag_uuid')

    try:
      user = User.objects.get(my_profile__flomio_tag_uuid=tag_uuid)
      user.my_profile.toggle_check_in(check_in_method=3)

      response = HttpResponse()
      response.status_code = 200
      return response

    except:
      return HttpResponseNotFound()


