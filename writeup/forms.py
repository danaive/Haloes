# -*- coding: utf-8 -*-
from django import forms


class ImageForm(forms.Form):
    img = forms.ImageField()


class SourceForm(forms.Form):
    title = forms.CharField()


class WriteupForm(forms.Form):
    title = forms.CharField()
    challenge = forms.IntegerField()
    content = forms.CharField()