from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product  # Productモデルをインポート


# 商品登録ページ
def product_register(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)  # モデルを保存する前に処理
            allergies_selected = form.cleaned_data['allergies']
            # アレルギーをカンマ区切りの文字列として保存
            product.allergies = ', '.join(allergies_selected)
            product.save()  # データベースに保存
            return redirect('product_list')  # 商品一覧ページにリダイレクト
    else:
        form = ProductForm()

    return render(request, 'register.html', {'form': form})


# 商品一覧ページ
def product_list(request):
    products = Product.objects.all()  # すべての商品を取得
    return render(request, 'product_list.html', {'products': products})
