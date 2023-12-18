# reservations/models.py
from django.db import models
from django.contrib.auth.models import User

# reservations/models.py
class Table(models.Model):
    number = models.IntegerField(unique=True)
    seats = models.IntegerField()
    shape = models.CharField(max_length=20, choices=[('rectangle', 'Прямоугольный'), ('oval', 'Овальный')])
    coordinates_horizontal = models.FloatField()
    coordinates_vertical = models.FloatField()
    width_percentage = models.FloatField()
    length_percentage = models.FloatField()

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()

