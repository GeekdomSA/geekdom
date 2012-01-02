from forum.models import *
from manager.forms import *
from forum.forms import *
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
      'title': request.user.userprofile.cname(),
      'user' : request.user,
    }, 
    context_instance=RequestContext(request))





# edit my account
@login_required
def edit_my_account(request):
  if request.method == "POST":
    uform = UserForm(request.POST, request.FILES, instance=request.user)
    try:
      pform = UserProfileForm(request.POST, instance=request.user.userprofile)
    except:
      pform = UserProfileForm(request.POST)
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
      pform = UserProfileForm(instance=request.user.userprofile)
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

# view all bills, oldest newest first
@login_required
def all_bills(request): 
  if not request.user.is_superuser: return HttpResponseNotFound()

  # bills = Bill.objects.order_by('paid', 'date_created')
  bills = Bill.objects.order_by('-id')
  return render_to_response(
    'manager/all_bills.html',
    {
      'title': "All Bills",
      'bills' : bills
    }, 
    context_instance=RequestContext(request))




# run billing update manually
@login_required
def run_billing(request):
  
  if not request.user.is_superuser: return HttpResponseNotFound()
  
  today = datetime.date.today()
  userprofiles = UserProfile.objects.filter(Q(membership_starts_on__lte = today)|Q(membership_ends_on__gte = today))
  
  count = 0
  
  for userprofile in userprofiles:
    
    if not userprofile.membership_type.price == 0:
    
      bill = Bill()
      bill.user = userprofile.user
      bill.collected_for = "Membership Dues"
      bill.amount = userprofile.membership_type.price
      bill.save()
    
      count = count + 1

      if userprofile.membership_type.duration == "mo": timedelta = datetime.timedelta(days=30)
      if userprofile.membership_type.duration == "dy": timedelta = datetime.timedelta(days=1)
      if userprofile.membership_type.duration == "wk": timedelta = datetime.timedelta(days=14)
      if userprofile.membership_type.duration == "qu": timedelta = datetime.timedelta(days=90)
      if userprofile.membership_type.duration == "ba": timedelta = datetime.timedelta(days=182)
      if userprofile.membership_type.duration == "yr": timedelta = datetime.timedelta(days=365)

      userprofile.next_billing_date = userprofile.next_billing_date + timedelta
      userprofile.save()
    
      subject = "Invoice #" + str(bill.id) + " - Geekdom Billing"

      message = """Hey """ + bill.user.userprofile.cname() + """!

        A new invoice has been generated.

        You owe: """ + str(bill.amount) + """ for """ + bill.collected_for + """

        Your total account balance is now: """ + str(bill.user.userprofile.account_balance()) + """

        Please swing by at your earliest convenience to take care of this. Thanks!

        """
    
      send_mail(subject, message, 'billing@geekdom.com', [bill.user.email], fail_silently=False)
    
  if count > 0:
    message = "Billing has been run successfully. " + str(count) + " new bills generated."
    messages.add_message(request, messages.SUCCESS, message)

  else:
    message = "Billing has been run successfully, but no new bills were generated."
    messages.add_message(request, messages.WARNING, message)
    
  return HttpResponseRedirect('/manager/billing/')






# create bill
@login_required
def new_bill(request): return





# view bill
@login_required
def view_bill(request, bill_id):
  if not request.user.is_superuser: return HttpResponseNotFound()

  bill = Bill.objects.get(id = bill_id)
  return render_to_response(
    'manager/view_bill.html',
    {
      'title': "Bill #" + str(bill.id),
      'bill' : bill
    }, 
    context_instance=RequestContext(request))





# edit bill
@login_required
def edit_bill(request, bill_id): return





# mark bill as paid
@login_required
def mark_bill_as_paid(request, bill_id):
  if not request.user.is_superuser: return HttpResponseNotFound()
  bill = Bill.objects.get(id = bill_id)
  bill.paid = True
  bill.save()
  message = "Bill #" + str(bill.id) + " has been marked as paid."
  messages.add_message(request, messages.SUCCESS, message)
  return HttpResponseRedirect("/manager/billing/")





# mark bill as unpaid
@login_required
def mark_bill_as_unpaid(request, bill_id):
  if not request.user.is_superuser: return HttpResponseNotFound()
  bill = Bill.objects.get(id = bill_id)
  bill.paid = False
  bill.save()
  message = "Bill #" + str(bill.id) + " has been marked as unpaid."
  messages.add_message(request, messages.WARNING, message)
  return HttpResponseRedirect("/manager/billing/")





@login_required
def all_members(request): 
  if not request.user.is_superuser: return HttpResponseNotFound()

  # bills = Bill.objects.order_by('paid', 'date_created')
  users = User.objects.all()
  return render_to_response(
    'manager/list_members.html',
    {
      'title': "All Members",
      'users' : users
    }, 
    context_instance=RequestContext(request))





@login_required
def view_member(request, user_id): 
  if not request.user.is_superuser: return HttpResponseNotFound()
  
  user = User.objects.get(id = user_id)

  if request.user.is_superuser and user.userprofile.notes:
    message = "Admin Note: " + user.userprofile.notes
    messages.add_message(request, messages.WARNING, message)
      
  return render_to_response(
    'manager/view_member.html',
    {
      'title': user.userprofile.cname(),
      'user' : user
    }, 
    context_instance=RequestContext(request))





def new_member(request): 
  if request.method == "POST":
    uform = UserForm(request.POST, request.FILES)
    pform = UserProfileForm(request.POST)

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
    pform = UserProfileForm()

  return render_to_response(
    'global/modelform.html',
    {
      'title': "Create a new user",
      'uform' : uform,
      'pform' : pform,
    }, 
    context_instance=RequestContext(request))





def edit_member(request, user_id):
  user = User.objects.get(id = user_id)

  if request.method == "POST":
    uform = UserForm(request.POST, request.FILES, instance=user)
    pform = AdminUserProfileForm(request.POST, request.FILES, instance=user.userprofile)

    if uform.is_valid() and pform.is_valid():
      user = uform.save()
      profile = pform.save(commit = False)
      profile.user = user
      profile.save()
      message = "User " + user.userprofile.cname() + " has been updated."
      messages.add_message(request, messages.SUCCESS, message)
      return HttpResponseRedirect('/manager/members/' + str(user.id))

  else:
    uform = UserForm(instance = user)
    pform = AdminUserProfileForm(instance = user.userprofile)

  return render_to_response(
    'global/modelform.html',
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
      Q(userprofile__membership_starts_on__lte = today)&Q(userprofile__membership_ends_on__gte = today)
    )|(
      Q(userprofile__membership_starts_on__lte = today)&Q(userprofile__membership_ends_on = None)
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
        users = User.objects.all()
        users = User.objects.filter(Q(first_name__icontains = name_query)|Q(last_name__icontains = name_query))
        
        title = 'Members matching "' + name_query + '"'
        subtitle = "Active members only"

    try: skill_query = request.GET['skill_query']
    except: skill_query = ""

    if not name_query or skill_query:
        users = User.objects.all()
        title = 'All Geekdom Members'
        subtitle = "Active members only"

    return render_to_response(
      'manager/public_member_list.html',
      {
        'title': title,
        'subtitle': subtitle,
        'users': users,
        'name_query':name_query,
        'skill_query':skill_query,
      }, 
      context_instance=RequestContext(request))




@login_required
def members_with_incomplete_profiles(request):
    if not request.user.is_superuser: return HttpResponseNotFound()
    users = User.objects.filter(
        Q(userprofile__skills = "") | 
        Q(userprofile__phone_number = "") | 
        Q(userprofile__address = "") |
        Q(userprofile__available_for_office_hours = "") |
        Q(userprofile__available_for_workshops = "")
    )

    return render_to_response(
      'manager/list_members.html',
      {
        'title': "Incomplete profiles",
        'subtitle': "Something is missing! Find it!",
        'users': users,
      }, 
      context_instance=RequestContext(request))

    




@login_required
def members_who_are_missing_stuff(request):
    if not request.user.is_superuser: return HttpResponseNotFound()
    users = User.objects.filter(
        (
            # community members
            Q(userprofile__membership_type = 1) & 
            Q(userprofile__has_elevator_fob = 0)
        )|(
            # dedicated
            Q(userprofile__membership_type = 2) & 
            Q(userprofile__has_parking_pass = 0) & 
            Q(userprofile__has_elevator_fob = 0) & 
            Q(userprofile__has_office_key = 0)
        )|(
            # student
            Q(userprofile__membership_type = 3) & 
            Q(userprofile__has_elevator_fob = 0)
        )|(
            # business
            Q(userprofile__membership_type = 4) & 
            Q(userprofile__has_parking_pass = 0) & 
            Q(userprofile__has_elevator_fob = 0) & 
            Q(userprofile__has_office_key = 0)
        )|(
            # startup
            Q(userprofile__membership_type = 5) & 
            Q(userprofile__has_elevator_fob = 0) & 
            Q(userprofile__has_parking_pass = 0) & 
            Q(userprofile__has_office_key = 0)
        )
    )

    return render_to_response(
      'manager/list_members.html',
      {
        'title': "Members missing stuff",
        'subtitle': "They need something from you, give it to them.",
        'users': users,
      }, 
      context_instance=RequestContext(request))





@login_required
def members_missing_office_num(request):
    if not request.user.is_superuser: return HttpResponseNotFound()
    users = User.objects.filter(
        (
            Q(userprofile__membership_type = 2)|
            Q(userprofile__membership_type = 4)|
            Q(userprofile__membership_type = 5)
        ) & Q(userprofile__office_num = "")        
    )

    return render_to_response(
      'manager/list_members.html',
      {
        'title': "Members w/blank office",
        'subtitle': "Where could they be?",
        'users': users,
      }, 
      context_instance=RequestContext(request))
