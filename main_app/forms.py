from django import forms
from .models import users

class user_form(forms.ModelForm):
	class Meta:
		model=users
		fields=('username','password','address','city','state','pin_code','lat_longitude')
		widgets={
		'username':forms.TextInput(attrs={'placeholder':'enter your username'}),
		'password':forms.PasswordInput(attrs={'placeholder':'Password'}),
		'address':forms.TextInput(attrs={'placeholder':'address'}),
		'city':forms.TextInput(attrs={'placeholder':'city','id':'city_field'}),
		'state':forms.TextInput(attrs={'placeholder':'state','id':'state_field'}),
		'pin_code':forms.TextInput(attrs={'placeholder':'Pin code'}),
		'lat_longitude':forms.TextInput(attrs={'type':'hidden','id':'geolocation'})
		}





