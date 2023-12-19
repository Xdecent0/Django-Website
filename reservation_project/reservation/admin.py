# reservation/admin.py
from django.contrib import admin
from .models import Table, Reservation
from .models import Category, Dish

admin.site.register(Table)
admin.site.register(Reservation)
admin.site.register(Category)
admin.site.register(Dish)