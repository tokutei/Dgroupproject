from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from foods.models import Food
from dgroupLogin.models import CustomUser  # CustomUserをインポート
from django.contrib.auth.decorators import login_required


class IndexView(ListView):
    model = Food
    template_name = 'index.html'
    context_object_name = 'object_list'  # コンテキストの名前を指定

    def get_queryset(self):
        # デフォルトで全商品を表示
        queryset = Food.objects.order_by('-inputed_at')

        # 検索フォームから商品名を受け取ってフィルタリング
        name = self.request.GET.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)  # 商品名に部分一致するものを検索

        return queryset


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
