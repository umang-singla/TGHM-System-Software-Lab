# from asyncio.windows_events import NULL
from django.db import models
from manager.models import Station
from restaurant.models import Restaurant

class Customer(models.Model):
    username = models.CharField(max_length= 20)
    password = models.CharField(max_length= 20)
    phone_number = models.CharField(max_length= 10, default = 0)
    def __str__(self):
        return self.username

class Orders(models.Model):
    food_item = models.CharField(max_length= 30, default= "")
    restaurant = models.ForeignKey(Restaurant, on_delete= models.CASCADE, default=None)
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE, default=None)
    time = models.DateTimeField()
    price = models.FloatField(default= 0)
    
    def __str__(self):
        return self.food_item # + ", " + self.restaurant + ", " + str(self.time)