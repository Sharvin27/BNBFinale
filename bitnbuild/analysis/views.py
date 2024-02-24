from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
def season(request):
    return render(request, 'pages/season.html')\
    
def crops(request):
    return render(request, 'pages/crops.html')

def fertilizer(request):
    return render(request, 'pages/fertilizer.html')

def seed(request):
    return render(request, 'pages/seed.html')

def profit(request):
    return render(request, 'pages/profit.html')

def utilized(request):
    return render(request, 'pages/utilized.html')