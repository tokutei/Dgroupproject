from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from foods.models import Food, Category
from dgroupLogin.models import CustomUser 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from foods.models import Food 
from dgroupLogin.forms import ProfileEditForm
from purchaseapp.models import CartPost, BuyJudge
from .forms import AddressEditForm
from django.core.paginator import Paginator
from django.contrib.auth.hashers import check_password
from django import forms
from django.urls import reverse



class IndexView(ListView):
    model = Food
    template_name = 'index.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        # 先に検索条件でフィルタリング
        queryset = Food.objects.all()

        self.search_query = self.request.GET.get('name', None)
        if self.search_query:
            queryset = queryset.filter(name__icontains=self.search_query)

        # フィルタリング後のデータをそのまま返す
        return queryset.order_by('-inputed_at')  # ページネーションのためスライスはしない

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Paginatorを使用してページネーション
        paginator = Paginator(context['object_list'], 8)  # 1ページあたり8件
        page_number = self.request.GET.get('page')  # URLからページ番号を取得
        page_obj = paginator.get_page(page_number)  # ページネーションされたオブジェクト

        context['object_list'] = page_obj  # ページネーションされたデータ
        context['search_query'] = self.search_query
        context['result_count'] = context['object_list'].paginator.count  # 結果数を表示
        context['categorys'] = Category.objects.all()
        context['recommended_items'] = Food.objects.order_by('shelf_life')[:4]

        # 在庫数の処理（既存コード）
        food_list = [i.stripe_product_id for i in Food.objects.all()]
        minus = []
        target = []
        judge = BuyJudge.objects.all()
        for i in judge:
            if i.stripe_product_id in food_list:
                foodsstock = Food.objects.get(stripe_product_id=i.stripe_product_id)
                stock = foodsstock.stock - i.stock
                if stock < 0:
                    stock = 0
                minus.append([i.stripe_product_id, stock])
                target.append(i.stripe_product_id)
        
        context['minus'] = minus
        context['target'] = target

        return context

    def get_template_names(self):
        if self.request.GET.get('name'):
            return ['search.html']
        return ['index.html']

class LoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('dgroupapp:index')  # アプリ名を含める
        return render(request, self.template_name, {'form': form})


class LogoutView(TemplateView):
    template_name = 'logout.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        logout(request)
        return redirect('dgroupapp:index')  # ログアウト後にリダイレクトするURL


class SuperuserOnlyView(UserPassesTestMixin, TemplateView):
    template_name = 'system_menu.html'

    def test_func(self):
        return self.request.user.is_superuser


# 利用規約
class TeamsView(TemplateView):
    template_name = 'teams.html'


class PrivacyView(TemplateView):
    template_name = 'privacy.html'


@login_required
def switch_account(request):
    class PasswordForm(forms.Form):
        password = forms.CharField(widget=forms.PasswordInput, label='Password')

    if request.method == 'POST':
        # ユーザーIDとパスワードを取得
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(id=user_id)

            # ログイン中のユーザーと選択したユーザーのメールアドレスが一致するかを確認
            if user.email == request.user.email:
                # 入力されたパスワードがユーザーのパスワードと一致するか確認
                if check_password(password, user.password):
                    login(request, user)  # パスワードが一致すれば切り替え
                    return redirect('dgroupapp:index')  # インデックスページへリダイレクト
                else:
                    # パスワードが間違っている場合、元のページに戻す
                    messages.error(request, "パスワードが間違っています。")
                    return redirect(reverse('dgroupapp:switch_account'))  # 元のページに戻る
            else:
                messages.error(request, "このアカウントは切り替えられません。")
                return redirect(reverse('dgroupapp:switch_account'))  # 元のページに戻る

        except CustomUser.DoesNotExist:
            messages.error(request, "指定されたユーザーが見つかりません。")
            return redirect(reverse('dgroupapp:switch_account'))  # 元のページに戻る

    else:
        # 自分と同じメールアドレスを持つユーザーのみ表示
        users = CustomUser.objects.filter(email=request.user.email)
        password_form = PasswordForm()
        return render(request, 'switch_account.html', {'users': users, 'password_form': password_form})
@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})


@login_required
def edit_address(request):
    if request.method == 'POST':
        form = AddressEditForm(request.POST)
        
        if form.is_valid():
            # フォームがバリデーションを通過した場合、ユーザーの住所を更新
            new_address = form.cleaned_data['address']
            new_postal_code = form.cleaned_data['postal_code']
            
            request.user.address = new_address
            request.user.postal_code = new_postal_code
            request.user.save()

            return redirect('dgroupapp:address_update_complete')
        else:
            # フォームが無効な場合、エラーメッセージを表示
            return render(request, 'edit_address.html', {'form': form})
    
    # GETリクエストの場合、フォームを空で表示
    form = AddressEditForm(initial={
        'address': request.user.address,
        'postal_code': request.user.postal_code
    })
    return render(request, 'edit_address.html', {'form': form})

@login_required
def address_update_complete(request):
    return render(request, 'address_update_complete.html')


def category_view(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Food.objects.filter(category=category)

    # 在庫数の処理
    food_list = [i.stripe_product_id for i in products]
    minus = []
    target = []
    judge = BuyJudge.objects.all()
    for i in judge:
        if i.stripe_product_id in food_list:
            foodsstock = Food.objects.get(stripe_product_id=i.stripe_product_id)
            stock = foodsstock.stock - i.stock
            if stock < 0:
                stock = 0
            minus.append([i.stripe_product_id, stock])
            target.append(i.stripe_product_id)

    # Paginatorで商品を8件ずつ分割
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()  # 全カテゴリ情報を取得
    return render(request, 'category_view.html', {
        'category': category,
        'products': page_obj,  # ページネーションされた商品を渡す
        'categorys': categories,  # カテゴリ情報をテンプレートに渡す
        'minus': minus,  # 在庫数の減少リストを渡す
        'target': target,  # 在庫数が変更された商品のリストを渡す
    })

class NewArrivalsView(ListView):
    model = Food
    template_name = 'new_arrivals.html'
    context_object_name = 'new_arrivals'

    def get_queryset(self):
        # 新着商品を新着順で取得
        return Food.objects.order_by('-inputed_at')  # 新着順で並べ替え

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 商品リストを取得
        product_list = Food.objects.order_by('-inputed_at')  # 新着順で並べ替え
        
        # Paginatorを使ってページネーション
        paginator = Paginator(product_list, 8)  # 1ページあたり8件を表示
        
        # 現在のページを取得
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        food_list = []
        foods = Food.objects.all()
        for i in foods:
            food_list.append(i.stripe_product_id)
        minus = []
        target = []
        judge = BuyJudge.objects.all()
        for i in judge:
            if i.stripe_product_id in food_list:
                foodsstock = Food.objects.get(stripe_product_id=i.stripe_product_id)
                stock = foodsstock.stock - i.stock
                if stock < 0:
                    stock = 0
                minus.append([i.stripe_product_id, stock])
                target.append(i.stripe_product_id)
        context['minus'] = minus
        context['target'] = target

        context['new_arrivals'] = page_obj  # ページネーションされた商品
        context['categorys'] = Category.objects.all()  # カテゴリ情報も追加
        return context
    
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dgroupapp:profile')  # プロフィールページにリダイレクト
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})


class AboutView(TemplateView):
    template_name = 'about.html'