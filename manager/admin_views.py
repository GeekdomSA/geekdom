# admin_views
from manager.forms import *
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, Http404, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from userena.models import UserenaSignup

import datetime
import mailchimp

@login_required
def all_members(request): 
  if not request.user.is_superuser: return HttpResponseForbidden()

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
  if not request.user.is_superuser: return HttpResponseForbidden()

  user = User.objects.get(id = user_id)

  return render_to_response(
    'manager/view_member.html',
    {
      'title': user.get_full_name(),
      'user' : user
    }, 
    context_instance=RequestContext(request))


@login_required
def new_member(request): 
  if not request.user.is_superuser: return HttpResponseForbidden()

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

      user.userena_signup = UserenaSignup(user_id = user.id, email_unconfirmed=user.email)

      message = "User successfully created!"
      messages.add_message(request, messages.SUCCESS, message)
      return HttpResponseRedirect('/accounts/' + user.username)

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
  if not request.user.is_superuser: return HttpResponseForbidden()
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
      return HttpResponseRedirect('/accounts/' + user.username)

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
def member_email_list(request, mt_id = False):
  if not request.user.is_superuser: return HttpResponseForbidden()
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
  if not request.user.is_superuser: return HttpResponseForbidden()
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
  if not request.user.is_superuser: return HttpResponseForbidden()
  total_members = User.objects.filter(is_active = True).all()
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



def tabular_member_report(request):
  if not request.user.is_superuser: return HttpResponseForbidden()

  members = User.objects.filter(is_active=True)
  today = datetime.date.today()

  return render_to_response(
    'manager/user_skill_tabular_report.html',
    { 
      'members': members, 'today':today,
    }, 
    context_instance=RequestContext(request))



def tabular_member_report_member_types(request):
  if not request.user.is_superuser: return HttpResponseForbidden()

  members = User.objects.filter(is_active=True)
  today = datetime.date.today()

  return render_to_response(
    'manager/user_type_tabular_report.html',
    { 
      'members': members, 'today':today,
    }, 
    context_instance=RequestContext(request))





  


