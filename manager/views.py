# from forum.models import *
from manager.forms import *
# from forum.forms import *
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, Http404, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import logout, authenticate, login


import datetime
from django.core.mail import send_mail

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




# view account overview
@login_required
def my_account(request):
  return render_to_response(
    'manager/view_member.html',
    {
      'title': request.user.get_full_name(),
      'user' : request.user,
    }, 
    context_instance=RequestContext(request))





# edit my account
@login_required
def edit_my_account(request):
  if request.method == "POST":
    uform = UserForm(request.POST, request.FILES, instance=request.user)
    try:
      pform = UserProfileForm(request.POST, request.FILES, instance=request.user.get_profile())
    except:
      pform = UserProfileForm(request.POST, request.FILES)
      pform.instance.user = request.user
      
    if uform.is_valid() and pform.is_valid():
      user = uform.save()
      profile = pform.save(commit = False)
      profile.user = user
      profile.save()
      message = "Profile successfully updated!"
      messages.add_message(request, messages.SUCCESS, message)
      return HttpResponseRedirect('/account/')

  else:
    uform = UserForm(instance = request.user)
    try:
      pform = UserProfileForm(instance=request.user.get_profile())
    except:
      pform = UserProfileForm
  
  return render_to_response(
    'global/modelform.html',
    {
      'title': "Edit your profile",
      'uform' : uform,
      'pform' : pform,
    }, 
    context_instance=RequestContext(request))




###############
# admin views #
###############



@login_required
def all_members(request): 
  if not request.user.is_superuser: return HttpResponseNotFound()

  users = User.objects.filter(is_active = True)
  return render_to_response(
    'manager/list_members.html',
    {
      'title': "All Members",
      'users' : users,
      'tabsection':'allmembers',
    }, 
    context_instance=RequestContext(request))





@login_required
def view_member(request, user_id): 

  user = User.objects.get(id = user_id)

  if request.user.is_superuser and user.get_profile().notes:
    message = "Admin Note: " + user.get_profile().notes
    messages.add_message(request, messages.INFO, message)
      
  return render_to_response(
    'manager/view_member.html',
    {
      'title': user.get_full_name(),
      'user' : user
    }, 
    context_instance=RequestContext(request))





def new_member(request): 
  if request.method == "POST":
    uform = UserForm(request.POST, request.FILES)
    pform = AdminUserProfileForm(request.POST)

    if uform.is_valid() and pform.is_valid():
      user = uform.save()
      profile = pform.save(commit = False)
      profile.user = user
      profile.save()
      message = "User successfully created!"
      messages.add_message(request, messages.SUCCESS, message)
      return HttpResponseRedirect('/manager/members/' + str(user.id))

  else:
    uform = UserForm()
    pform = AdminUserProfileForm()

  return render_to_response(
    'manager/admin_user_form.html',
    {
      'title': "New Member",
      'uform' : uform,
      'pform' : pform,
      'tabsection':'newmember',
    }, 
    context_instance=RequestContext(request))





def edit_member(request, user_id):
  user = User.objects.get(id = user_id)

  if request.method == "POST":
    uform = UserForm(request.POST, request.FILES, instance=user)
    pform = AdminUserProfileForm(request.POST, request.FILES, instance=user.get_profile())

    if uform.is_valid() and pform.is_valid():
      user = uform.save()
      profile = pform.save(commit = False)
      profile.user = user
      profile.save()
      message = "User " + user.get_full_name() + " has been updated."
      messages.add_message(request, messages.SUCCESS, message)
      return HttpResponseRedirect('/manager/members/' + str(user.id))

  else:
    uform = UserForm(instance = user)
    pform = AdminUserProfileForm(instance = user.get_profile())

  return render_to_response(
    'manager/admin_user_form.html',
    {
      'title': "Editing " + user.get_full_name(),
      'uform' : uform,
      'pform' : pform,
    }, 
    context_instance=RequestContext(request))




def email_all_members(request):
  if not request.user.is_superuser: return HttpResponseNotFound()
  
  today = datetime.date.today()
  
  users = User.objects.filter(
    (
      Q(my_profile__membership_starts_on__lte = today)&Q(my_profile__membership_ends_on__gte = today)
    )|(
      Q(my_profile__membership_starts_on__lte = today)&Q(my_profile__membership_ends_on = None)
    )
  )
  
  if request.method == 'POST':
    form = ForumMailForm(request.POST)
    if form.is_valid():
      count = 0
      for user in users:
        subject = "[geekdom] " + request.POST.get('subject')
        message = request.POST.get('message')
        send_mail(subject, message, 'mailroom@geekdom.com', [user.email], fail_silently=False)
        count = count + 1

      message = "Message sent to the " + str(count) + " members."
      messages.add_message(request, messages.SUCCESS, message)
      return HttpResponseRedirect('/manager/members/')

  else:
    form = ForumMailForm()

  return render_to_response(
    'global/modelform.html',
    {
      'title': 'Send a message to all active members',
      'subtitle': "Members with active memberships only",
      'form' : form
    }, 
    context_instance=RequestContext(request))





def logout_page(request):
    logout(request) 
    return HttpResponseRedirect('/')




def public_member_list(request):

    try: name_query = request.GET['name_query']
    except: name_query = ""
    if name_query:
        users = User.objects.filter(Q(first_name__icontains = name_query)|Q(last_name__icontains = name_query)|Q(email__icontains = name_query)).order_by('first_name')
        title = 'Members matching "' + name_query + '"'
        subtitle = "Don't search both names at once... yet."

    try: skill_query = request.GET['skill_query']
    except: skill_query = ""
    if skill_query:
        users = User.objects.filter(Q(my_profile__skills__icontains = skill_query)).order_by('first_name')
        title = 'Members with skill: "' + skill_query + '"'
        subtitle = "Active members only"

    if not (name_query or skill_query):
        users = User.objects.order_by('first_name')
        title = 'All Geekdom Members'
        subtitle = "Active members only"

    newest_members = User.objects.order_by('-date_joined')[:5]

    return render_to_response(
      'manager/public_member_list.html',
      {
        'title': title,
        'subtitle': subtitle,
        'users': users,
        'name_query':name_query,
        'skill_query':skill_query,
        'newest_members':newest_members,
      }, 
      context_instance=RequestContext(request))




@login_required
def members_with_incomplete_profiles(request):
    if not request.user.is_superuser: return HttpResponseNotFound()
    users = User.objects.filter(
        Q(my_profile__skills = "") | 
        Q(my_profile__phone_number = "") | 
        Q(my_profile__address = "") |
        Q(my_profile__available_for_office_hours = "") |
        Q(my_profile__available_for_workshops = "")
    )

    return render_to_response(
      'manager/list_members.html',
      {
        'title': "Incomplete profiles",
        'subtitle': str(users.count()) + " profiles have missing information.",
        'users': users,
        'tabsection':'membersincompleteprofiles',
      }, 
      context_instance=RequestContext(request))

    




@login_required
def members_who_are_missing_stuff(request):
    if not request.user.is_superuser: return HttpResponseNotFound()
    users = User.objects.filter(
        (
            # community members
            Q(my_profile__membership_type = 1) & 
            Q(my_profile__has_elevator_fob = 0)
        )|(
            # dedicated
            Q(my_profile__membership_type = 2) & 
            Q(my_profile__has_parking_pass = 0) & 
            Q(my_profile__has_elevator_fob = 0) & 
            Q(my_profile__has_office_key = 0)
        )|(
            # student
            Q(my_profile__membership_type = 3) & 
            Q(my_profile__has_elevator_fob = 0)
        )|(
            # business
            Q(my_profile__membership_type = 4) & 
            Q(my_profile__has_parking_pass = 0) & 
            Q(my_profile__has_elevator_fob = 0) & 
            Q(my_profile__has_office_key = 0)
        )|(
            # startup
            Q(my_profile__membership_type = 5) & 
            Q(my_profile__has_elevator_fob = 0) & 
            Q(my_profile__has_parking_pass = 0) & 
            Q(my_profile__has_office_key = 0)
        )
    )

    return render_to_response(
      'manager/list_members.html',
      {
        'title': "Members missing stuff",
        'subtitle': str(users.count()) + " members are missing a fob, a key or a parking pass.",
        'users': users,
        'tabsection':'membersmissingstuff',
      }, 
      context_instance=RequestContext(request))





@login_required
def members_missing_office_num(request):
    if not request.user.is_superuser: return HttpResponseNotFound()
    users = User.objects.filter(
        (
            Q(my_profile__membership_type = 2)|
            Q(my_profile__membership_type = 4)|
            Q(my_profile__membership_type = 5)
        ) & Q(my_profile__office_num = "")        
    )

    return render_to_response(
      'manager/list_members.html',
      {
        'title': "Members w/blank office",
        'subtitle': str(users.count()) + " office-bound members don't have office letters.",
        'users': users,
        'tabsection':'membersofficenum',
      }, 
      context_instance=RequestContext(request))


@login_required
def member_email_list(request):
    users = User.objects.all()

    return render_to_response(
      'manager/member_email_list.html',
      {
        'title': "All member email list",
        'subtitle': "For sending out mass-emails",
        'users': users,
        'tabsection':'membersemaillist',
      }, 
      context_instance=RequestContext(request))



@login_required
def members_by_room(request):
    users = User.objects.exclude(my_profile__office_num = "").order_by('my_profile__office_num')

    return render_to_response(
      'manager/list_members.html',
      {
        'title': "Members by office #",
        'subtitle': "",
        'users': users,
        'tabsection':'membersbyroom',
      }, 
      context_instance=RequestContext(request))






def kiosk1(request):
  now = datetime.datetime.now()
  users = User.objects.filter(my_profile__checkin__expires_at__gte = now).order_by('first_name')
  all_users = User.objects.filter(is_active = True).order_by('first_name')

  return render_to_response(
    'kiosk/screen1.html',
    { 'users': users, 'all_users':all_users, }, 
    context_instance=RequestContext(request))



def kiosk_user_view(request, user_id):

  user = User.objects.get(id = user_id)
  all_users = User.objects.filter(is_active = True).order_by('first_name')

  return render_to_response(
    'kiosk/memberscreen.html',
    { 'user': user, 'all_users':all_users, }, 
    context_instance=RequestContext(request))



def kiosk_user_checkin(request, user_id):
  user = User.objects.get(id = user_id)
  checkin = Checkin.objects.get_or_create(userprofile = user.my_profile, expires_at = datetime.datetime.now() + datetime.timedelta(hours = 8))
  message = "Thanks for checking in, " + user.first_name + "!"
  messages.add_message(request, messages.SUCCESS, message)
  return HttpResponseRedirect("/kiosk1/")


def kiosk_user_checkout(request, user_id):
  user = User.objects.get(id = user_id)
  now = datetime.datetime.now()
  checkins = Checkin.objects.filter(userprofile = user.my_profile).filter(expires_at__gte = now)
  for checkin in checkins:
    checkin.expires_at = now - datetime.timedelta(hours = 1)
    checkin.save()
  message = "Thanks for checking out, " + user.first_name + "! Drive safe!"
  messages.add_message(request, messages.SUCCESS, message)
  return HttpResponseRedirect("/kiosk1/")
  



from dateutil import parser
import feedparser
def kiosk2(request):
  today = datetime.date.today()
  now = datetime.datetime.now()
  events = Event.objects.filter(ends_at__gte = now).order_by('starts_at')

  twitterfeed = feedparser.parse("http://search.twitter.com/search.atom?q=geekdomsa")
  tweets = []
  for tweet in twitterfeed.entries: tweets.append(tweet)
  for tweet in tweets: tweet.pp = parser.parse(tweet.published).strftime("%m/%d/%y %H:%M:%S")

  return render_to_response(
    'kiosk/screen2.html',
    { 'events': events, 'today': today, 'tweets':tweets }, 
    context_instance=RequestContext(request))

