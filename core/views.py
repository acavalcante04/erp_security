from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Mantenha as outras imports se houver

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')