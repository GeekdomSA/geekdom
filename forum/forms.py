from django.forms import *
from forum.models import *
from django.contrib.admin import widgets

class ForumForm(ModelForm):
  class Meta:
    model = Forum
    exclude = (
      'deleted_forum', 
      'slug', 
      'added_on',  
      'added_by', 
      'last_modified_on', 
      'last_modified_by'
    )

class ReplyForm(ModelForm): 
  class Meta:
    model = Reply
    exclude = (
      'thread', 
      'user'
    )


class ThreadForm(ModelForm): 
  class Meta:
    model = Thread
    exclude = (
      'forum',
      'user',
      'locked',
    )


class EventForm(ModelForm):
  starts_at = DateTimeField(widget=widgets.AdminSplitDateTime)
  ends_at = DateTimeField(widget=widgets.AdminSplitDateTime)

  class Meta:
    model = Event
    exclude = ('attendees','hosts')


class AdminEventForm(ModelForm):
  starts_at = DateTimeField(widget=widgets.AdminSplitDateTime)
  ends_at = DateTimeField(widget=widgets.AdminSplitDateTime)

  class Meta:
    model = Event
    exclude = ('attendees','hosts')

class ForumMailForm(Form):
  subject = CharField(max_length=100)
  message = CharField(widget=forms.Textarea)


class ForumForm(ModelForm):
  class Meta:
    model = Forum
    exclude = ('locked', 'members', 'owners')


class UserMailForm(Form):
  message = CharField(widget=forms.Textarea)



