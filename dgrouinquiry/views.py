from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages
from purchaseapp.models import OrderPost, OrderAitemPost


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # フォームデータをセッションに保存（確認用）
            request.session['contact_form_data'] = form.cleaned_data
            return redirect('dgrouinquiry:contact_confirm')  # 確認ページにリダイレクト
        else:
            # フォームが無効な場合、エラーメッセージを表示して再表示
            messages.error(request, "入力されていない項目があります。もう一度確認してください。")
            return render(request, 'contact.html', {'form': form})
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def contact_confirm_view(request):
    # セッションからフォームデータを取得
    form_data = request.session.get('contact_form_data', None)
    
    if not form_data:
        return redirect('dgrouinquiry:contact')  # データが無ければフォーム画面にリダイレクト

    form = ContactForm(form_data)

    if request.method == 'POST':
        # 確認後、データをデータベースに保存
        if form.is_valid():
            form.save()
            del request.session['contact_form_data']  # セッションデータを削除
            messages.success(request, 'お問い合わせいただきありがとうございます。')
            return redirect('dgroupapp:index')  # 成功後にフォーム画面にリダイレクト
        else:
            # フォームが無効な場合、エラーを表示
            return render(request, 'contact_confirm.html', {'form': form, 'form_data': form_data, 'errors': form.errors})

    return render(request, 'contact_confirm.html', {'form': form, 'form_data': form_data})


def order_history(request):
    if request.user.is_authenticated:
        orders = OrderPost.objects.filter(user=request.user)
        order_details = []
        for order in orders:
            items = OrderAitemPost.objects.filter(ordernumber=order.ordernumber)
            order_details.append({
                'order': order,
                'items': items
            })

        if order_details:
            return render(request, 'order_history.html', {
                'order_details': order_details
            })
        else:
            return render(request, 'order_history.html', {
                'message': '注文履歴はありません。'
            })
    else:
        return redirect('dgroupapp:login')