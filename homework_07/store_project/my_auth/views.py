from django.shortcuts import render
from .models import StoreUser
from django.views.generic import CreateView
from .forms import StoreUserCreateForm

class StoreUserCreateView(CreateView):
    model = StoreUser
    success_url = '/'
    form_class = StoreUserCreateForm
    
