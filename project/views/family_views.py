from django.shortcuts import render, redirect

def family(request):
    return render(request, 'project/family.html')
