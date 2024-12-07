from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    """A view to Return the Index Page"""
    return render(request, 'products/index.html')