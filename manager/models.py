from django.db import models

class Admin(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    def __str__(self):
        return self.username 

class Station(models.Model):
    name = models.CharField(max_length=50)
    lat = models.FloatField()
    lng = models.FloatField()
    visible = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Train(models.Model):
    name = models.CharField(max_length=50)
    stations = models.CharField(max_length=200)
    def __str__(self):
        return self.name