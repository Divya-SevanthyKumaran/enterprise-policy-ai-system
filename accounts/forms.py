from django import forms
from accounts.models import UserProfile

class RegisterForm(forms.Form):
        username = forms.CharField(max_length=50)
        password = forms.CharField(widget=forms.PasswordInput)
        email = forms.EmailField()
        department = forms.ChoiceField(choices=[('HR','HR'),('IT','IT'),('F','finance')])
        date_of_birth = forms.DateField()
        gender = forms.ChoiceField(choices=[('M','Male'),('F', 'Female'),('O', 'Other')], required=False)
        
        
class LoginForm(forms.Form):
        username = forms.CharField(max_length=50)
        password = forms.CharField(widget=forms.PasswordInput)
        
class UpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        
        