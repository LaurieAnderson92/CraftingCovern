from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models.functions import Lower
from django.utils.timezone import now
from django.views.generic import CreateView
from django.http import HttpResponse
from django.db.models import Q

from .models import Product, Category
from .forms import ProductForm
from users.models import Profile

# Create your views here.

def index(request):
    """A view to Return the Index Page"""
    return render(request, 'products/index.html')

# Uses Django Generic list view
def product_list(request):

    products = Product.objects.filter(deleted_on=None)
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
                products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                return redirect(reverse('product_all'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'query': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(
    request,
    'products/product_list.html',
    context,
    )

def product_detail(request, id):
    """A View to return the detail page for a product"""

    auth_user_id = request.user.pk

    queryset_product = Product.objects.all()
    product = get_object_or_404(queryset_product, id=id)

    try: 
        profile = Profile.objects.get(auth_user_id=auth_user_id)
        return render(
            request,
            'products/product_detail.html',
            {
                "product": product,
                "profile": profile
            },
        )
    except:
        return render(
            request,
            'products/product_detail.html',
            {
                "product": product,
            },
        )

def product_new(request):
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect(reverse('product_all'))
    else:
        form = ProductForm()

    template = 'products/product_add.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

def product_edit(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid:
            form.save()
            return redirect('product_detail', id)
    else:
        form = ProductForm(instance=product)
        
    template = 'products/product_edit.html'
    context = {
    'form': form,
    "product": product,
    }

    return render(request, template, context)

def product_delete(request, id):
    product = get_object_or_404(Product, pk=id)

    product.deleted_on = now()
    product.save()
    return redirect(reverse('product_all'))
    