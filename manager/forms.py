from django.forms import *
from manager.models import *
from django.contrib.admin import widgets




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
            'has_elevator_fob'
        )


class AdminUserProfileForm(ModelForm):

  membership_starts_on = DateField(help_text="Format: YYYY-MM-DD", widget=widgets.AdminDateWidget, required=False)
  membership_ends_on = DateField(help_text="Format: YYYY-MM-DD", widget=widgets.AdminDateWidget, required=False)

  class Meta:
    model = UserProfile
    exclude = ('user')
    
