from django.shortcuts import render,HttpResponse,redirect
from .models import Category
from .forms import ProductForm

def index(request):
    send_expiration_via_sms()
    return render(request, 'base.html')


def add_inventory(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(display_inventory)
    else:
        form = ProductForm()
    categories = Category.objects.all()
    return render(request, 'inventory/add_inventory.html', {'form': form, 'categories': categories})


def display_inventory(request):
    # Retrieve all categories along with their associated products
    categories = Category.objects.prefetch_related('product_set')

    # Render the template with the categories and associated products
    return render(request, 'inventory/inventory.html', {'categories': categories})

from twilio.rest import Client


def send_expiration_via_sms():
    account_sid = 'ACbf6cee76099df8fffbf3b1956c747fcd'
    auth_token = '727f773bf34138354ce81640b466ce32'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='whatsapp:+14155238886',
                                    body=f'Hello, Aryan \nProduct Name : Banana\nExpiration Date:4days Later, 27th Feb 2024\nProduct Name : Banana\nExpiration Date:4days Later, 27th Feb 2024\nPlease refill the stock',

    to='whatsapp:+919653484071'
    )

    print(message.sid)
