from unicodedata import name
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from matplotlib.style import context
from manager.models import Station
import restaurant
from .models import FoodItem, Restaurant
from customer.models import Orders

# Create your views here. 

# function to display the dashboard of the restaurant
def dashboard(request,restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    food_list = FoodItem.objects.filter(restaurant_id=restaurant_id)
    order_list = Orders.objects.filter(restaurant_id=restaurant_id)
    context = {'restaurant': restaurant,'food_list': food_list, 'order_list': order_list}
    return render(request, 'restaurant/dashboard.html',context)

# functions to login
def login(request):
    return render(request, 'restaurant/index.html')

def login_restaurant(request):
    obj = None
    for restaurant in Restaurant.objects.all():
        if restaurant.username == request.POST['username'] and restaurant.password == request.POST['password'] and request.POST['username']!= "" and request.POST['password'] != "":
            obj = restaurant
            break
    if obj is None:
        messages.error(request, 'Invalid username or password!')
        return HttpResponseRedirect('../login/')
    
    return HttpResponseRedirect('../dashboard/' + str(obj.id))

# functions to register
def register(request):
    context = {'station_list': Station.objects.all()}
    return render(request, 'restaurant/register.html',context)

def register_restaurant(request):
    if request.POST['username']!= "" and request.POST['password'] == request.POST['re_password'] and request.POST['password']!= "" and request.POST['mobile']!= "": 
        obj = Restaurant(username=request.POST['username'], password=request.POST['password'], name=request.POST['name'], station= Station.objects.get(id=request.POST['station']))

        if Restaurant.objects.filter(username = obj.username, password = obj.password, mobile = obj.mobile).exists():
            return HttpResponseRedirect('../dashboard/' + str(Restaurant.objects.get(username = obj.username, password = obj.password, mobile = obj.mobile).id))
        obj.save()
            
        return HttpResponseRedirect('../dashboard/' + str(obj.id))
    else :
        messages.error(request, 'Error! Please fill all the fields correctly!')
        return HttpResponseRedirect('../register', status = 302)

# function to add a food item to the restaurant
def add_food(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    if request.POST['food_name']!= "" and request.POST['food_price'].isnumeric() and  float(request.POST['food_price'])>= 0:
        food = FoodItem(name=request.POST['food_name'], price=request.POST['food_price'], restaurant=restaurant)
        food.save()
        return HttpResponseRedirect('../dashboard/' + str(restaurant.id))
    
    else :
        messages.error(request, 'Error! Please fill all the fields correctly!')
        return HttpResponseRedirect('../dashboard/' + str(restaurant.id), status = 302)

def change_status(request,order_id):
    order = Orders.objects.get(id=order_id)
    order.status += 1
    order.save()
    return HttpResponseRedirect('../dashboard/' + str(order.restaurant.id))
