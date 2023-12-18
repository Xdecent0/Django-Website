# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import View
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:user_profile')
    template_name = 'signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return response

class UserProfileView(View):
    template_name = 'user_profile.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = UserChangeForm(instance=request.user)
            return render(request, self.template_name, context={'user': request.user, 'form': form})
        else:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
        return render(request, self.template_name, context={'user': request.user, 'form': form})
