# from asyncio.windows_events import NULL
from django.db import models
from manager.models import Station

class Customer(models.Model):
    username = models.CharField(max_length= 20)
    password = models.CharField(max_length= 20)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, default= None)
    def __str__(self):
        return self.username

class Orders(models.Model):
    food_item = models.CharField(max_length= 30, default= "")
    # restaurant = models.CharField(max_length= 50)
    time = models.DateTimeField()
    customer = models.ForeignKey(Customer, on_delete= models.CASCADE)
    def __str__(self):
        return self.food_item # + ", " + self.restaurant + ", " + str(self.time)