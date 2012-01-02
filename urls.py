from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
def i18n_javascript(request):
  return admin.site.i18n_javascript(request)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from geekdom.forum.views import *
from geekdom.manager.views import *

handler403 = 'manager.views.error_403handler'
handler404 = 'manager.views.error_404handler'
handler500 = 'manager.views.error_500handler'

admin.autodiscover()

urlpatterns = patterns('',

    # homepage
    url(r'^$', homepage),


    ###############
    # forum views #
    ###############

    # view all forums
    url(r'^forums/$', all_forums),

    # create a new forum
    url(r'^forums/new$', new_forum),

    # view forum
    url(r'^forums/(?P<forum_id>[\d]+)/$', view_forum),

    # create thread
    url(r'^forums/(?P<forum_id>[\d]+)/new_thread/$', create_thread),

    # subscribe to forum
    url(r'^forums/(?P<forum_id>[\d]+)/subscribe/$', subscribe_to_forum),

    # unsubscribe from forum
    url(r'^forums/(?P<forum_id>[\d]+)/unsubscribe/$', unsubscribe_from_forum),

    # mail all users of this forum
    url(r'^forums/(?P<forum_id>[\d]+)/mail/$', mail_forum_users),

    # view thread
    url(r'^forums/(?P<forum_id>[\d]+)/(?P<thread_id>[\d]+)/$', view_thread),

    # create reply
    url(r'^forums/(?P<forum_id>[\d]+)/(?P<thread_id>[\d]+)/reply/$', reply_to_thread),



    ###############
    # event views #
    ###############

    # view all upcoming events
    url(r'^events/$', upcoming_events),

    # view a project
    url(r'^events/(?P<event_id>[\d]+)/$', view_event),

    # rsvp for event
    url(r'^events/(?P<event_id>[\d]+)/rsvp/$', rsvp_event),

    # unrsvp for event
    url(r'^events/(?P<event_id>[\d]+)/unrsvp/$', unrsvp_event),

    # events im attending
    url(r'^events/attending/$', events_attending),

    # events from my forums
    url(r'^events/recommended/$', events_recommended),

    # create a new event
    url(r'^events/new/$', new_event),




    ##########################
    # public memberlist views #
    ##########################

    url(r'^members/$', public_member_list),
    url(r'^members/(?P<user_id>[\d]+)/$', view_member),



    #################
    # account views #
    #################

    # view account overview
    url(r'^account/$', my_account),

    # edit my account
    url(r'^account/edit/$', edit_my_account),




    ###############
    # admin views #
    ###############

    # view all bills, oldest newest first
    url(r'^manager/billing/$', all_bills),

    # run billing update manually
    url(r'^manager/billing/run/$', run_billing),

    # create bill
    url(r'^manager/billing/new/$', new_bill),

    # view bill
    url(r'^manager/billing/(?P<bill_id>[\d]+)/$', view_bill),

    # edit bill
    url(r'^manager/billing/(?P<bill_id>[\d]+)/edit/$', edit_bill),

    # mark bill as paid
    url(r'^manager/billing/(?P<bill_id>[\d]+)/mark_as_paid/$', mark_bill_as_paid),

    # mark bill as unpaid
    url(r'^manager/billing/(?P<bill_id>[\d]+)/mark_as_unpaid/$', mark_bill_as_unpaid),

    # list all members
    url(r'^manager/members/$', all_members),

    # view a user profile
    url(r'^manager/members/(?P<user_id>[\d]+)/$', view_member),

    # edit a user profile
    url(r'^manager/members/(?P<user_id>[\d]+)/edit/$', edit_member),

    # create new member
    url(r'^manager/members/new$', new_member),

    # send an email to all ACTIVE members
    url(r'^manager/members/email_all_members$', email_all_members),
    
    

    ###########
    # REPORTS #
    ###########
    
    # members with incomplete profiles
    url(r'^manager/members/incomplete$', members_with_incomplete_profiles),
    url(r'^manager/members/missing_stuff$', members_who_are_missing_stuff),
    url(r'^manager/members/office_num$', members_missing_office_num),
    






    # user login
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),

    # user logout
    url(r'^logout/$', logout_page),



    ######################
    # django admin views #
    ######################

    url(r'^admin/jsi18n', i18n_javascript),
    url(r'^admin/', include(admin.site.urls)),

    # added for django-admin-tools
    url(r'^admin_tools/', include('admin_tools.urls')),


)
