# reservation/models.py
from django.db import models
from django.contrib.auth.models import User

class Table(models.Model):
    number = models.IntegerField()
    seats = models.IntegerField()
    shape_choices = [('oval', 'Oval'), ('rectangle', 'Rectangle')]
    shape = models.CharField(max_length=10, choices=shape_choices)
    width = models.FloatField()
    length = models.FloatField()
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
