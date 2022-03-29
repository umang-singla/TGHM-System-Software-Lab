from unicodedata import name
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from matplotlib.style import context
from manager.models import Station
import restaurant
from .models import FoodItem, Restaurant
from customer.models import Orders

# Create your views here. 

def dashboard(request,restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    food_list = FoodItem.objects.filter(restaurant_id=restaurant_id)
    order_list = Orders.objects.filter(restaurant_id=restaurant_id)
    context = {'restaurant': restaurant,'food_list': food_list, 'order_list': order_list}
    return render(request, 'restaurant/dashboard.html',context)

def login(request):
    return render(request, 'restaurant/index.html')

def login_restaurant(request):
    obj = None
    for restaurant in Restaurant.objects.all():
        if restaurant.username == request.POST['username'] and restaurant.password == request.POST['password']:
            obj = restaurant
            break
    if obj is None:
        return render(request, 'restaurant/login.html', {'error': 'Invalid username or password!'})
    
    return HttpResponseRedirect('../dashboard/' + str(obj.id))

def register(request):
    context = {'station_list': Station.objects.all()}
    return render(request, 'restaurant/register.html',context)

def register_restaurant(request):
    obj = Restaurant(username=request.POST['username'], password=request.POST['password'], name=request.POST['name'], station=Station.objects.get(id=request.POST['station']), mobile=request.POST['mobile'])
    obj.save()
    return HttpResponseRedirect('../login')

def add_food(request,restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    food = FoodItem(name=request.POST['food_name'], price=request.POST['food_price'], restaurant=restaurant)
    food.save()
    return HttpResponseRedirect('../dashboard/' + str(restaurant.id))

def change_status(request,order_id):
    order = Orders.objects.get(id=order_id)
    order.status += 1
    order.save()
    return HttpResponseRedirect('../dashboard/' + str(order.restaurant.id))
