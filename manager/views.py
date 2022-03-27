from tracemalloc import start
from unicodedata import name
from django.shortcuts import render, get_object_or_404
from .models import Admin, Station, Train
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

def login(request):
    return render(request, 'manager/index.html')

def login_admin(request):
    obj = None
    for admin in Admin.objects.all():
        if admin.username == request.POST['username'] and admin.password == request.POST['password']:
            obj = admin
            break
    
    if obj is None:
        return HttpResponse("Invalid username or password")

    return HttpResponse('Logged in successfully')

def register(request):
    return render(request, 'manager/register.html')

def register_admin(request):
    admin = Admin(username= request.POST['username'], password= request.POST['password'])
    admin.save()

    return HttpResponseRedirect('../dashboard')

def dashboard(request):
    context = {'station_list': Station.objects.all(), 'train_list': Train.objects.all()}
    return render(request, 'manager/dashboard.html',context)

def add_station(request):
    # return HttpResponse(request.POST['station'] + ' added successfully')
    station = Station(name= request.POST['station'], lat= request.POST['lat'], lng= request.POST['lon'])
    station.save()

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