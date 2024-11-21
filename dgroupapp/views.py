from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from foods.models import Food, Category
from dgroupLogin.models import CustomUser  # CustomUserをインポート
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from foods.models import Allergy, Food 
from django.core.paginator import Paginator

class IndexView(ListView):
    model = Food
    template_name = 'index.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = Food.objects.order_by('-inputed_at')[:8]
        self.search_query = self.request.GET.get('name', None)
        if self.search_query:
            queryset = queryset.filter(name__icontains=self.search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.search_query
        context['result_count'] = context['object_list'].count()
        context['categorys'] = Category.objects.all()  # カテゴリ情報を追加
         # 賞味期限が遠い順に商品4件を取得
        context['recommended_items'] = Food.objects.order_by('shelf_life')[:4]  # 賞味期限が遠い順に4つ取
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
    if request.method == 'POST':
        # ユーザーIDでアカウントを切り替え
        user_id = request.POST.get('user_id')
        try:
            user = CustomUser.objects.get(id=user_id)  # CustomUserを使って検索
            login(request, user)  # 新しいユーザーでログイン
            return redirect('dgroupapp:index')  # インデックスページにリダイレクト
        except CustomUser.DoesNotExist:
            return redirect('dgroupapp:login')  # ユーザーが見つからなかった場合はログインページに戻る
    else:
        # superuserの場合、全ユーザーを表示
        if request.user.is_superuser:
            users = CustomUser.objects.filter(is_superuser=True)  # Superuserは全ユーザーを表示
        else:
            # 普通のユーザーの場合、自分のアカウントと同じ役割のユーザーのみ表示
            users = CustomUser.objects.filter(is_superuser=False)  # 普通のユーザーのみ表示

        return render(request, 'switch_account.html', {'users': users})

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def edit_address(request):
    if request.method == 'POST':
        # フォームから新しい住所を取得
        new_address = request.POST.get('address')

        # ユーザーの住所を更新
        request.user.address = new_address
        request.user.save()

        return redirect('dgroupapp:address_update_complete')
    
    # GETリクエストの場合は、現在の住所を表示
    return render(request, 'edit_address.html')

@login_required
def address_update_complete(request):
    return render(request, 'address_update_complete.html')


def category_view(request, category_id):
    # 指定したカテゴリに関連する商品を取得
    category = Category.objects.get(id=category_id)
    products = Food.objects.filter(category=category)  # カテゴリに関連する商品を取得

    return render(request, 'category_view.html', {
        'category': category,
        'products': products,
    })


def allergy_view(request):
    # 全てのアレルギーを取得
    allergies = Allergy.objects.all()

    # 初期表示として、全ての食品を取得
    foods = Food.objects.all()

    # アレルギーが選択されている場合、選択されたアレルギーを含む食品をフィルタリング
    selected_allergy = request.GET.get('allergy', None)
    if selected_allergy:
        # 'selected_allergy'に基づいてアレルギー項目が含まれていない食品をフィルタリング
        foods = foods.exclude(allergy__icontains=selected_allergy)

    # フィルタリング後の食品とアレルギー一覧をテンプレートに渡す
    return render(request, 'allergy_view.html', {
        'allergies': allergies,  # アレルギーのリストを渡す
        'foods': foods,          # フィルタリング後の食品リストを渡す
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
        
        context['new_arrivals'] = page_obj  # ページネーションされた商品
        context['categorys'] = Category.objects.all()  # カテゴリ情報も追加
        return context
    