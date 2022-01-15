from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def HomeView(req):
    return render(req, "base.html")
