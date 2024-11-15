from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product


# 商品登録ページ
def product_register(request):
    print("bbb")
    print(request)
    if request.method == 'POST':
        print(request.POST)
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # フォームデータをセッションに保存して確認ページに送る
            request.session['form_data'] = form.cleaned_data
            print("セッションに保存されたデータ:", request.session['form_data'])
            return redirect('Convenience:product_confirm')  # 確認ページにリダイレクト
    else:
       
        form = ProductForm()
    return render(request, 'register.html', {'form': form})


# 確認ページ
def product_confirm(request):
    form_data = request.session.get('form_data', None)  # セッションからデータを取得

    if not form_data:
        print("データは来てないよ～")
        return redirect('Convenience:product_register')  # データがなければ登録ページにリダイレクト

    # 最終確認ページの表示
    if request.method == 'POST':
        # 確認ページで「登録」をクリックした場合に保存
        product = Product(
            name=form_data['name'],
            quantity=form_data['quantity'],
            expiration_date=form_data['expiration_date'],
            allergies=', '.join(form_data['allergies']),
            image=form_data['image']
        )
        product.save()  # データベースに保存

        # セッションのデータをクリア
        del request.session['form_data']

        return redirect('Convenience:product_list')  # 商品一覧ページにリダイレクト

    return render(request, 'product_confirm.html', {'form_data': form_data})


# 商品一覧ページ
def product_list(request):
    products = Product.objects.all()
    return render(request, 'Convenience.html', {'products': products})
