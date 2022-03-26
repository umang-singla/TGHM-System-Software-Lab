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
    station_list = Station.objects.all()
    context = {'station_list': station_list}
    return render(request, 'manager/dashboard.html',context)

def add_station(request):
    # return HttpResponse(request.POST['station'] + ' added successfully')
    station = Station(name= request.POST['station'], lat= request.POST['lat'], lng= request.POST['lon'])
    station.save()

    return HttpResponseRedirect('../dashboard')

def add_train(request):
    train = Train()
    train.name = request.POST['train_name']
    train.stations = request.POST['stations']
    train.save()

    return HttpResponseRedirect('../dashboard')
    
def change_station_status(request):
    station = get_object_or_404(Station, id=request.GET['station_id'])
    station.visible = not station.visible
    station.save()

    return HttpResponseRedirect('../dashboard')