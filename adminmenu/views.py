from django.shortcuts import render, get_object_or_404
from .models import Contact


def system_menu(request):
    return render(request, 'system_menu.html')


def order_list(request):
    return render(request, 'order_list.html')


def index(request):
    return render(request, 'index')


def contact_list(request):
    # Contactモデルから全てのデータを取得
    contacts = Contact.objects.all()
    return render(request, 'contact_list.html', {'contacts': contacts})


def contact_detail(request, contact_id):
    # 特定のContactオブジェクトを取得
    contact = get_object_or_404(Contact, id=contact_id)
    return render(request, 'contact_detail.html', {'contact': contact})