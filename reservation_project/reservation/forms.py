# reservation/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation, Table
from datetime import date
from django.forms import ValidationError
from django.core.validators import MinValueValidator

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ReservationForm(forms.Form):
    seats = forms.IntegerField(label='Number of seats')
    shape = forms.ChoiceField(
        label='Shape',
        choices=[('any', 'Any shape'), ('oval', 'Oval'), ('rectangle', 'Rectangle')],
        initial='any',
        widget=forms.Select(),
    )
    date = forms.DateField(label='Date', widget=forms.TextInput(attrs={'type': 'date'}))

class DateForm(forms.Form):
    date = forms.DateField(
        label='Choose a Date',
        widget=forms.TextInput(attrs={'type': 'date'}),
    )

    def clean_date(self):
        selected_date = self.cleaned_data['date']

        if selected_date < date.today():
            raise ValidationError('Please select a date from today onwards.')

        return selected_date