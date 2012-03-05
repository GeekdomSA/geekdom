# admin_views
from manager.forms import *
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, Http404, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required
def all_members(request): 
  if not request.user.is_superuser: return HttpResponseNotForbidden()

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
  if not request.user.is_superuser: return HttpResponseNotForbidden()

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


@login_required
def new_member(request): 
  if not request.user.is_superuser: return HttpResponseNotForbidden()

  if request.method == "POST":
    uform = UserForm(request.POST, request.FILES)
    pform = AdminUserProfileForm(request.POST)

    if uform.is_valid() and pform.is_valid():
      user = uform.save()
      profile = pform.save(commit = False)
      profile.user = user
      profile.save()

      # add member to mailchimp list
      list = mailchimp.utils.get_connection().get_list_by_id("8bd90b528f")
      list.subscribe(profile.user.email, {'EMAIL':profile.user.email})

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


@login_required
def edit_member(request, user_id):
  if not request.user.is_superuser: return HttpResponseNotForbidden()
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
def member_email_list(request, mt_id = False):
  if not request.user.is_superuser: return HttpResponseNotForbidden()
  if mt_id:
    mt = MembershipType.objects.get(id = mt_id)
    users = User.objects.filter(my_profile__membership_type__id = mt_id)
    title = mt.name + " email list"
    subtitle = "For sending out mass-emails to " + mt.name + "s!"
    tabsection = 'membersemaillist-' + str(mt_id)
  else:  
    users = User.objects.all()
    title = "All member email list"
    subtitle = "For sending out mass-emails to everybody!"
    tabsection = 'membersemaillist'

  return render_to_response(
    'manager/member_email_list.html',
    {
      'title': title,
      'subtitle': subtitle,
      'users': users,
      'tabsection':tabsection,
    }, 
    context_instance=RequestContext(request))


@login_required
def members_by_room(request):
  if not request.user.is_superuser: return HttpResponseNotForbidden()
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


def general_member_stats(request):
  if not request.user.is_superuser: return HttpResponseNotForbidden()
  total_members = User.objects.all()
  mts = MembershipType.objects.all()
  total_revenue = 0
  for mt in mts: total_revenue = total_revenue + mt.total_revenue()

  return render_to_response(
    'manager/general_member_report.html',
    { 
      'title': "Total Members: " + str(total_members.count()),
      'mts': mts,
      'total_revenue': total_revenue,
      'tabsection':'membersgeneralstats' 
    }, 
    context_instance=RequestContext(request))






  


