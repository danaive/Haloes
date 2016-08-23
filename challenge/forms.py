# -*- coding: utf-8 -*-
from django import forms


class ChallengeForm(forms.Form):
    pk = forms.IntegerField()


class SubmitForm(forms.Form):
    pk = forms.IntegerField()
    flag = forms.CharField()


class SwitchForm(forms.Form):
    pk = forms.IntegerField()
    state = forms.BooleanField()


class ZipForm(forms.Form):
    source = forms.FileField()
