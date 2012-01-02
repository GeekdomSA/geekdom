import datetime
from haystack.indexes import *
from haystack import site
from manager.models import UserProfile

class UserProfileIndex(SearchIndex):
    fullname = CharField(document=True, use_template=True)
    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return UserProfile.objects.all()

site.register(UserProfile, UserProfileIndex)