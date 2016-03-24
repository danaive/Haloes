# -*- coding: utf-8 -*-
from django import forms

class RegForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    salt = forms.CharField(max_length=50)


class ImageForm(forms.Form):
    img = forms.ImageField()


class UpdateForm(forms.Form):
    major = forms.CharField(max_length=50, required=False)
    school = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=False)
    blog = forms.URLField(required=False)
    motto = forms.CharField(max_length=30, required=False)


class FollowForm(forms.Form):
    username = forms.CharField(max_length=50)
