from django.forms import *
from manager.models import *
from django.contrib.admin import widgets
# from bootstrap.forms import BootstrapForm, Fieldset

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", 'first_name', 'last_name']

# form for non-admin users to edit their own profile
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = (
            'user', 
            'notes', 
            "membership_starts_on", 
            'membership_ends_on', 
            'membership_type', 
            'has_parking_pass', 
            'has_office_key', 
            'has_elevator_fob',
            'privacy'
        )


class AdminUserProfileForm(ModelForm):
  class Meta:
    model = UserProfile
    exclude = ('user', 'privacy')
    
