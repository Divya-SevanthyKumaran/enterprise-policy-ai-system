from django import forms
from documents.models import PolicyDocument

class PolicyForm(forms.ModelForm):
    class Meta:
        model = PolicyDocument
        fields = '__all__'