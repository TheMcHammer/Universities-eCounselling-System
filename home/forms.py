from django.contrib.auth.models import User, Group
from .models import UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            #'group'
        ]

    def save(self, commit = True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        #user.group = self.cleaned_data['group']

        if commit:
            user.save()

        return user

class UserProfileForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            #'university',
            'password',
            #'group'
        )

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            #'university',
            'password',
            #'group'
        )
