# -*- coding: utf-8 -*-
from django import forms


class ImageForm(forms.Form):
    img = forms.ImageField()


class OriginForm(forms.Form):
    title = forms.CharField()


class WriteupForm(forms.Form):
    title = forms.CharField()
    challenge = forms.IntegerField()
    content = forms.CharField()


class CommentForm(forms.Form):
    writeup = forms.IntegerField()
    reply = forms.IntegerField()
    content = forms.CharField()
