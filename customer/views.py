from wsgiref.util import request_uri
from django.shortcuts import render, get_object_or_404
from customer.models import Customer, Orders
from manager.models import Station, Train
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

import json
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

    return HttpResponseRedirect('../dashboard/' + str(obj.id))

def register(request):
    return render(request, 'customer/register.html')

def register_customer(request):
    if request.POST['password'] == request.POST['re_password']: 
        customer = Customer(username= request.POST['username'], password= request.POST['password'], phone_number = request.POST['phone_number'])

        if Customer.objects.filter(username=customer.username, password = customer.password).exists():
            return HttpResponseRedirect('../dashboard/' + str(Customer.objects.filter(username=customer.username, password = customer.password)[0].id))
        
        customer.save()
        return HttpResponseRedirect('../dashboard/' + str(customer.id))
    else: 
        return render(request, 'customer/register.html', {'error': 'Passwords do not match'})

def dashboard(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    context = {'customer': customer, 'train_list': Train.objects.all()}
    return render(request, 'customer/dashboard.html', context)

def fetch_station(request):
    station = Train.objects.get(id=request.GET['train_id']).stations.split(' ')
    station_list, id_list = [],[]
    for i in station:
        id_list.append(i)
        station_list.append(Station.objects.get(id=i).name)
    

    return JsonResponse({'station_list': station_list, 'id_list': id_list})

def place_order(request):
    pass