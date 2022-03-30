from telnetlib import STATUS
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Admin, Station, Train
from customer.models import Orders
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# Create your views here.

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def login(request):
    return render(request, 'manager/index.html')

def login_admin(request):
    obj = None
    for admin in Admin.objects.all():
        if admin.username == request.POST['username'] and admin.password == request.POST['password']:
            obj = admin
            break
    
    if obj is None:
        messages.error(request, 'Invalid username or password!')
        return HttpResponseRedirect('../login')

    return HttpResponseRedirect('../dashboard')

def register(request):
    return render(request, 'manager/register.html')

def register_admin(request):
    if request.POST['username'] != "" and request.POST['password'] == request.POST['re_password']:
        admin = Admin(username= request.POST['username'], password= request.POST['password'])
        admin.save()

        return HttpResponseRedirect('../dashboard')
    else :
        messages.error(request, 'Invalid username or passwords do not match!')
        return HttpResponseRedirect('../register')

def dashboard(request):
    context = {'station_list': Station.objects.all(), 'train_list': Train.objects.all()}
    return render(request, 'manager/dashboard.html',context)

def add_station(request):
    # return HttpResponse(request.POST['station'] + ' added successfully')
    if isfloat(request.POST['lat']) and isfloat(request.POST['lon']) and request.POST['station'] != "" and request.POST['lat']!= "" and request.POST['lon']!= "": 
        if -90 < float(request.POST['lat']) < 90 and -180 < float(request.POST['lon']) < 180:
            station = Station(name= request.POST['station'], lat= request.POST['lat'], lng= request.POST['lon'])
            station.save()
            return HttpResponseRedirect('../dashboard', status= 200)
        else :
            messages.error(request, 'Latitude or Longitude out of range!')
            return HttpResponseRedirect('../dashboard', status= 302)
    else:
        messages.error(request, 'Invalid input!')
        return HttpResponseRedirect('../dashboard')

def edit_train(request,train_id):

    if request.method == 'POST':
        train = get_object_or_404(Train, id=train_id)
        train.name = request.POST['train']
        train.stations = str(request.POST['start'])
        for i in range(0, len(request.POST)-4):
            train.stations += ' ' + str(request.POST[ 'r' + str(i+1)])
        train.stations += ' ' + str(request.POST['end'])
        train.save()

        return HttpResponseRedirect('../dashboard')

    train_name = Train.objects.get(id=train_id).name
    station_list = Train.objects.get(id=train_id).stations.split(" ")
    stations = []
    for station in station_list:
        stations.append(Station.objects.get(id=station))
    context = {'train_name': train_name, 'stations': stations,'station_list': Station.objects.all(), 'train_id': train_id}
    return HttpResponse(render(request, 'manager/edit_train.html', context))
    pass

def add_train(request):

    train = request.POST['train']
    start = request.POST['start']
    end = request.POST['end']
    station_list = str(request.POST['start'])
    for i in range(0, len(request.POST)-4):
        station_list += ' ' + str(request.POST[ 'r' + str(i+1)])
    station_list += ' ' + str(request.POST['end'])

    train = Train(name= train, stations= station_list)
    train.save()

    return HttpResponseRedirect('../dashboard')
    
def change_station_status(request):
    station = get_object_or_404(Station, id=request.GET['station_id'])
    station.visible = not station.visible
    station.save()

    return HttpResponseRedirect('../dashboard')

def statistics(request):
    # function to plot the statistics of the train
    train = get_object_or_404(Train, id=request.GET['train_id'])
    station_list = train.stations.split(" ")
    stations = []

    for station in station_list:
        stations.append(Station.objects.get(id=station))

    deliv_cnt = 0
    undeliv_cnt = 0

    for order in Orders.objects.all():
        if order.status > 1:
            for station in stations:
                if station == order.restaurant.station:
                    deliv_cnt += 1
        else:
            for station in stations:
                if station == order.restaurant.station:
                    undeliv_cnt += 1

    context = {'delivered': deliv_cnt, 'undelivered': undeliv_cnt}
    
    return JsonResponse(context)
