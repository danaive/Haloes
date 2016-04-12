# -*- coding: utf-8 -*-
from django import forms


class SubmitForm(forms.Form):
    pk = forms.IntegerField()
    contest = forms.IntegerField()
    flag = forms.CharField()