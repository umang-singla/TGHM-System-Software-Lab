from django.shortcuts import render, get_object_or_404
from customer.models import Customer
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

def login(request):
    return render(request, 'customer/index.html')

def login_customer(request):
    obj = None
    for customer in Customer.objects.all():
        if customer.username == request.POST['username'] and customer.password == request.POST['password']:
            obj = customer
            break
    
    if obj is None:
        return HttpResponse("Invalid username or password")

    return HttpResponse('Logged in successfully')

def register(request):
    return render(request, 'customer/register.html')

def register_customer(request):
    admin = Customer(username= request.POST['username'], password= request.POST['password'])
    admin.save()

    return HttpResponse('Registered successfully')
    

def dashboard(request):
    return render(request, 'customer/dashboard.html')
    