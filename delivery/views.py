from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Order

def order_list(request):
    order_id = request.GET.get('order_id')
    sort_by = request.GET.get('sort_by', '')  # デフォルトで注文番号でソート

    if sort_by == '':
        sort_by = 'id'

    if order_id:
        orders = Order.objects.filter(order_number=order_id).order_by(sort_by)
    else:
        orders = Order.objects.all().order_by(sort_by)

    return render(request, 'order_list.html', {'orders': orders, 'sort_by': sort_by})

def ship_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.shipped = True
        order.shipped_date = timezone.now()
        order.save()
        return redirect('delivery:order_list')

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.shipped = False
        order.shipped_date = None
        order.save()
        return redirect('delivery:order_list')




