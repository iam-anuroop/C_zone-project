from django import forms
# from django.contrib.auth.forms import UserCreationForm
from .models import UserDetails

class  UserRegistrationForm(forms.ModelForm):
    confirmpassword = forms.CharField(widget=forms.PasswordInput())


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].help_text=None
        # self.fields['password'].widget.attrs.update({'type':"password"})

    class Meta:
        model = UserDetails
        fields = ('fullname', 'username', 'email', 'phone', 'password')



    


