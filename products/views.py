from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

# Create your views here.

def index(request):
    """A view to Return the Index Page"""
    return render(request, 'products/index.html')

# Uses Django Generic list view
class ProductList(generic.ListView):
    template_name = "products/product_list.html"
    paginate_by = 12