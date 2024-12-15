"""craftingcovern URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from .views import ProductCreateView

urlpatterns = [
    path('', views.index, name='home'),
    path('product/', views.product_list, name='products_all'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('product/new/', ProductCreateView.as_view(), name='products_create'),
]
