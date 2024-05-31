from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def register(request):
    return render(request, 'registration/register.html')

def login_view(request):
    return render(request, 'registration/login.html')

@login_required
def challenge_create(request):
    return render(request, 'challenges/challenge_create.html')

@login_required
def challenge_list(request):
    return render(request, 'challenges/challenge_list.html')

@login_required
def challenge_detail(request):
    return render(request, 'challenges/challenge_detail.html')