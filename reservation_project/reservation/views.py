from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Table, Reservation
from django.contrib.auth import logout
from .forms import ReservationForm
from django.views.generic import ListView
from .forms import DateForm

def home(request):
    return render(request, 'reservation/base.html')

class TableListView(ListView):
    model = Table
    template_name = 'reservation/table_list.html'

def select_table(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            tables = Table.objects.all()
            return render(request, 'reservation/table_list.html', {'tables': tables, 'date': date})
    else:
        form = DateForm()

    return render(request, 'reservation/select_table.html', {'form': form})

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
    table = Table.objects.get(pk=table_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']

            if not Reservation.objects.filter(table=table, date=date).exists():
                Reservation.objects.create(user=request.user, table=table, date=date)
                return redirect('profile')
            else:
                form.add_error('date', 'Table is already reserved for the selected date.')
    else:
        form = ReservationForm()

    return render(request, 'reservation/reserve_table.html', {'table': table, 'form': form})

@login_required
def user_profile(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'accounts/user_profile.html', {'reservations': reservations})

def logout_view(request):
    logout(request)
    return redirect('home')
