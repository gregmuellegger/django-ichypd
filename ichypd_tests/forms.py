from django import forms
from ichypd_tests.models import PersonalDetails


class PersonalDetailsForm(forms.ModelForm):
    age = forms.IntegerField(min_value=13, max_value=99)

    class Meta:
        model = PersonalDetails
        exclude = ('created',)
