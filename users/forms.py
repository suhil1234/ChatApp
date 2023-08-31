from typing import Any
from django.contrib.auth import forms
from django.contrib.auth.models import User
from django import forms as form
from users.models import profile

class UserCreateForm(forms.UserCreationForm):
    email=form.EmailField(required=True)

    class Meta:
        model =User
        fields= ['username','email','password1','password2']
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(UserCreateForm,self).__init__(*args, **kwargs)

        for fieldname in ['username','email','password1','password2']:
            self.fields[fieldname].help_text=None

class UserUpdateForm(form.ModelForm):

    class Meta:
        model = User
        fields = ['username','email']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(UserUpdateForm,self).__init__(*args, **kwargs)

        for fieldname in ['username','email']:
            self.fields[fieldname].help_text=None

class ProfileUpdateForm(form.ModelForm):
    
    class Meta :
        model = profile
        fields = ['image']
