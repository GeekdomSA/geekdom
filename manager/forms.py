from django.forms import *
from manager.models import *
from django.contrib.admin import widgets
# from bootstrap.forms import BootstrapForm, Fieldset
from userena.forms import EditProfileForm
from userena.utils import get_profile_model

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
    


class HackedProfileForm(EditProfileForm):
    class Meta:
        model = get_profile_model()
        exclude = ['user', 'notes', 
            "membership_starts_on", 
            'membership_ends_on', 
            'membership_type', 
            'has_parking_pass', 
            'has_office_key', 
            'has_elevator_fob',
            'privacy',]

    # def save(self):
    # """
    # Override the save method to save the first and last name to the user
    # field.

    # """

    # user_profile = super(SignupFormExtra, self).save(commit=False)

    # user_profile.address = self.cleaned_data['address']
    # user_profile.contact = self.cleaned_data['contact']
    # user_profile.business = self.cleaned_data['business']

    # user_profile.save()

    # return user_profile