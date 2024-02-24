from django.shortcuts import render,HttpResponse
from .models import Category
from .forms import ProductForm

def index(request):
    return render(request, 'base.html')


def add_inventory(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('Product added successfully!')
    else:
        form = ProductForm()
    categories = Category.objects.all()
    return render(request, 'inventory/add_inventory.html', {'form': form, 'categories': categories})


def display_inventory(request):
    # Retrieve all categories along with their associated products
    categories = Category.objects.prefetch_related('product_set')

    # Render the template with the categories and associated products
    return render(request, 'inventory/inventory.html', {'categories': categories})