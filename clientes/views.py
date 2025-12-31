from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cliente

@login_required
def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/cliente_list.html', {'clientes': clientes})