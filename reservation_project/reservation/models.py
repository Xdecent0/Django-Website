# reservation/models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Table(models.Model):
    number = models.IntegerField()
    seats = models.IntegerField()
    shape_choices = [('oval', 'Oval'), ('rectangle', 'Rectangle')]
    shape = models.CharField(max_length=10, choices=shape_choices)
    width = models.FloatField()
    length = models.FloatField()
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()
    last_reservation_date = models.DateField(null=True, blank=True)

    def is_reserved(self, date):
        return self.last_reservation_date and self.last_reservation_date >= date


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=255)
    weight = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
