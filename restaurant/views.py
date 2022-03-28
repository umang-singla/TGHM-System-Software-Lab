from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from matplotlib.style import context
from manager.models import Station
import restaurant
from .models import Restaurant
from customer.models import Orders

# Create your views here. 

def dashboard(request,restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    context = {'restaurant': restaurant}
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
    # if obj
