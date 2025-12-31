from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Produto

@login_required
def produto_list(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque/produto_list.html', {'produtos': produtos})