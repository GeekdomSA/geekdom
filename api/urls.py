from django.conf.urls.defaults import patterns, include, url

from geekdom.api.views import *

urlpatterns = patterns('',
    
    # Some management functionality
    url(r'^manage/generate_key/$', generate_key),

    # User action APIs
    url(r'^users/checkin/$', checkin),
    # url(r'^checkout/(?P<user_id>\d)/$', checkout),

    # User information APIs
    url(r'^users/get/user_id/(?P<username>\w+)/$', get_user_id)
    # Examples:
    # url(r'^info/get/username/(?P<user_id>\d)/$', foo)
    # url(r'^info/get/all/(?P<user_id>\d)/$', foo)
)