from django.shortcuts import render

# Create your views here.


def add_patient(request):
    return render(request, 'add_patient.html')
