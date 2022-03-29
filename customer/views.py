import math
from wsgiref.util import request_uri
from django.shortcuts import render, get_object_or_404
import customer
from customer.models import Customer, Orders
from restaurant.models import FoodItem, Restaurant
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
    order_list  = Orders.objects.filter(customer=customer)
    context = {'order_list': order_list, 'customer': customer, 'train_list': Train.objects.all(), 'food_list': FoodItem.objects.all()}
    return render(request, 'customer/dashboard.html', context)

def fetch_station(request):
    station = Train.objects.get(id=request.GET['train_id']).stations.split(' ')
    station_list, id_list = [],[]
    for i in station:
        id_list.append(i)
        station_list.append(Station.objects.get(id=i).name)

    restaurant_list = []
    

    for id in id_list:
        res_list = Restaurant.objects.filter(station=id)

        for res in  res_list:
            if res.id is not None:
                restaurant_list.append([res.id, res.name])
    

    return JsonResponse({'station_list': station_list, 'id_list': id_list, 'restaurant_list': restaurant_list})

def fetch_food(request):
    restaurant = Restaurant.objects.get(id=request.GET['restaurant_id'])
    food_list = FoodItem.objects.filter(restaurant=restaurant)

    foods = []

    for food in food_list:
        foods.append([food.id, food.name, food.price])

    return JsonResponse({'food_list': foods})

def get_time(request):

    def haversine(lat1, lon1, lat2, lon2):
        # distance between latitudes
        # and longitudes
        dLat = (lat2 - lat1) * math.pi / 180.0
        dLon = (lon2 - lon1) * math.pi / 180.0
    
        # convert to radians
        lat1 = (lat1) * math.pi / 180.0
        lat2 = (lat2) * math.pi / 180.0
    
        # apply formulae
        a = (pow(math.sin(dLat / 2), 2) +
            pow(math.sin(dLon / 2), 2) *
                math.cos(lat1) * math.cos(lat2));
        rad = 6371
        c = 2 * math.asin(math.sqrt(a))
        return rad * c

    restaurant_station = Restaurant.objects.get(id=request.GET['restaurant_id']).station
    food = FoodItem.objects.get(id=request.GET['food_id'])
    train_station = []
    temp = Train.objects.get(id=request.GET['train_id']).stations.split(' ')
    for i in temp:
        train_station.append(Station.objects.get(id=i))
    current_station = Station.objects.get(id=request.GET['current_station_id'])

    speed = 100

    current_station_index = train_station.index(current_station)
    restaurant_station_index = train_station.index(restaurant_station)
    if current_station_index > restaurant_station_index:
        return JsonResponse({'time': 'Delivery Not Possible'})
    elif current_station_index == restaurant_station_index:
        return JsonResponse({'time': '00 hr : 15 min : 00 sec' })
    else:
        distance = 0
        while current_station_index != restaurant_station_index:
            distance += haversine(current_station.lat, current_station.lng, train_station[current_station_index + 1].lat, train_station[current_station_index + 1].lng)
            current_station_index += 1
        time = distance / speed
        hr = int(time)
        min = int((time - hr) * 60)
        sec = int(((time - hr) * 60 - min) * 60)

        return JsonResponse({'time': str(hr) + " hr : " + str(min) + " min : " + str(sec) + " sec"})


def place_order(request,customer_id):
    order = Orders(customer = Customer.objects.get(id=customer_id), restaurant = Restaurant.objects.get(id=request.POST['restaurant']), food_item = request.POST['food'])
    order.save()

    return HttpResponseRedirect('../dashboard/' + str(customer_id))

def change_status(request,order_id):
    order = Orders.objects.get(id=order_id)
    order.status += 1
    order.save()
    return HttpResponseRedirect('../dashboard/' + str(order.customer.id))