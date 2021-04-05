from django import forms
from django.contrib.auth.models import User
from rango.models import UserProfile, Meme

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password',)

class MemeForm(forms.ModelForm):
	title = forms.CharField(max_length=128,
							help_text="Please enter the title of the meme.")
	image = forms.ImageField()
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)

	class Meta:
		model = Meme
		exclude = ('category', )
