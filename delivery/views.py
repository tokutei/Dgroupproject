from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils import timezone
from purchaseapp.models import OrderPost, OrderAitemPost


def order_list(request):
    order_id = request.GET.get('order_id')
    sort_by = request.GET.get('sort_by', 'ordernumber')  # デフォルトで注文番号でソート

    # 並び替え可能なフィールド名をリストで指定
    valid_sort_fields = ['ordernumber', 'aitemname', 'delivery_method', 'shipped_date']  # 必要なフィールドを追加

    # sort_by が有効なフィールド名でなければデフォルトの 'ordernumber' に設定
    if sort_by not in valid_sort_fields:
        sort_by = 'ordernumber'

    # 注文番号でフィルタリングする場合
    if order_id:
        orders = OrderPost.objects.filter(ordernumber=order_id).order_by(sort_by)
    else:
        orders = OrderPost.objects.all().order_by(sort_by)
    
    # アイテム情報を注文番号で関連付けて取得
    order_items = OrderAitemPost.objects.filter(ordernumber__in=[order.ordernumber for order in orders])
        
    # ページネーションの設定
    paginator = Paginator(orders, 5)  # 1ページに5件表示
    page_number = request.GET.get('page')  # 現在のページ番号を取得
    page_obj = paginator.get_page(page_number)  # ページオブジェクトを取得

    return render(request, 'order_list.html', {
        'orders': page_obj,
        'order_items': order_items,
        'sort_by': sort_by,
    })


# 配送処理
def ship_order(request, order_id):
    order = get_object_or_404(OrderPost, id=order_id)
    if not order.shipped:
        order.shipped = True
        order.shipped_date = timezone.now()  # 配送日時を現在時刻に設定
        order.save()
        return redirect('delivery:order_list')  # 注文一覧にリダイレクト
    return HttpResponse("配送処理に失敗しました。", status=400)


# 取り消し処理
def cancel_order(request, order_id):
    order = get_object_or_404(OrderPost, id=order_id)
    if order.shipped:
        order.shipped = False
        order.shipped_date = None  # 配送日時を解除
        order.save()
        return redirect('delivery:order_list')  # 注文一覧にリダイレクト
    return HttpResponse("配送がまだ完了していないため、キャンセルできません。", status=400)
