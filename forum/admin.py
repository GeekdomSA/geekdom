from django.contrib import admin
from forum.models import *

admin.site.register(ForumType)
admin.site.register(Forum)
admin.site.register(Thread)
admin.site.register(Reply)
admin.site.register(Event)