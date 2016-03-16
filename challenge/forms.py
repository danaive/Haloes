from django import forms

class DropForm(forms.Form):
    pk = forms.IntegerField()


class SubmitForm(forms.Form):
    pk = forms.IntegerField()
    flag = forms.CharField()


class SwitchForm(forms.Form):
    pk = forms.IntegerField()
    state = forms.BooleanField()
