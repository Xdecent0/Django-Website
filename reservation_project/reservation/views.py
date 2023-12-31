from django.contrib.auth.forms import UserCreationForm
from django.db.models import OuterRef, Subquery
from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Table, Reservation
from django.contrib.auth import logout
from datetime import datetime
from .forms import ReservationForm
from django.views.generic import ListView
from .forms import DateForm
from django.views import View
from django.contrib import messages
from .models import Category, Dish
from django.http import HttpResponseBadRequest
from django.db.models import OuterRef, Subquery
from django.urls import reverse

class MenuView(View):
    template_name = 'reservation/menu.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        dishes = Dish.objects.all()
        context = {'categories': categories, 'dishes': dishes}
        return render(request, self.template_name, context)

def home(request):
    return render(request, 'reservation/base.html')

class TableListView(View):
    template_name = 'reservation/table_list.html'

    def get(self, request, *args, **kwargs):
        form = DateForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = DateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']

            available_tables = Table.objects.filter(
                last_reservation_date__lt=date
            )

            return render(request, self.template_name, {'tables': available_tables, 'date': date, 'form': form})

        return render(request, self.template_name, {'form': form})

class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reservation/about.html')


def select_table(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            available_tables = Table.get_available_tables(date)
            return render(request, 'reservation/table_list.html', {'tables': available_tables, 'date': date, 'form': form})
    else:
        form = DateForm()

    tables = Table.objects.all()
    return render(request, 'reservation/select_table.html', {'form': form, 'tables': tables})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('table_list')
    else:
        form = UserCreationForm()
    return render(request, 'reservation/register.html', {'form': form})

@login_required
def reserve_table(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    date = request.POST.get('date')

    existing_reservation = Reservation.objects.filter(user=request.user, table=table, date=date).exists()
    if existing_reservation:
        error_message = "This table is already reserved."
        form = DateForm()
        tables = Table.objects.all()
        url = reverse('select_table')
        return render(request, 'reservation/select_table.html', {'reservation_error': error_message, 'redirect_url': url})

    if date:
        reservation = Reservation.objects.create(user=request.user, table=table, date=date)
        table.last_reservation_date = datetime.strptime(date, '%Y-%m-%d').date()
        table.save()
        return redirect('user_confirm')

    return redirect('select_table')


@login_required
def user_profile(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservation/user_profile.html', {'reservations': reservations})


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def user_confirm(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservation/user_confirm.html', {'reservations': reservations})

