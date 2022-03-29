# from asyncio.windows_events import NULL
from datetime import datetime
from django.db import models
from manager.models import Station
from restaurant.models import Restaurant, FoodItem

class Customer(models.Model):
    username = models.CharField(max_length= 20)
    password = models.CharField(max_length= 20)
    phone_number = models.CharField(max_length= 10, default = 0)
    def __str__(self):
        return self.username

class Orders(models.Model):
    food_item = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete= models.CASCADE, default=None)
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE, default=None)
    time = models.DateTimeField(default= datetime.now())
    status = models.IntegerField(default=0)
    
    def __str__(self):
        return FoodItem.objects.get(id = self.food_item).name + ", " + self.restaurant.name + ", " + str(self.time)