from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import Product

# Create your views here.

def index(request):
    """A view to Return the Index Page"""
    return render(request, 'products/index.html')

# Uses Django Generic list view
class ProductList(generic.ListView):
    model = Product
    template_name = "products/product_list.html"
    paginate_by = 12

def product_detail(request, id):
    """A View to return the detail page for a product"""

    queryset = Product
    product = get_object_or_404(queryset, id=id)

    return render(
        request,
        'products/product_detail.html',
        {"product": product},
    )