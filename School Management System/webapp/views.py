from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'webapp/index.html')


def aboutus(request):
    return render(request, 'webapp/about.html')
    


def contactUs(request):
    return render(request, 'webapp/contact.html')


def facilities(request):
    return render(request, 'webapp/facilities.html')


def gallery(request):
    return render(request, 'webapp/gallery.html')

def pre_primary(request):
    return render(request, 'webapp/pre-primary.html')


def primmary(request):
    return render(request, 'webapp/primary.html')


def high_school(request):
    return render(request, 'webapp/high-school.html')