from django.shortcuts import render

def system_menu(request):
    return render(request, 'system_menu.html')


def order_list(request):
    return render(request, 'order_list.html')

def index(request):
    return render(request, 'index')


