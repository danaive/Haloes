from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def test(request):
    return render(request, 'users.jade', {'username': 'danlei'})