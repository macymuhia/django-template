from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return redirect('dashboard')


def dashboard(request):
    return render(request, 'base.html')
