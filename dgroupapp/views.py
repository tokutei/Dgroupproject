from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import FoodInputForm
from .models import FoodInput


class IndexView(ListView):
    template_name = 'index.html'
    queryset = FoodInput.objects.order_by('-inputed_at')


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


# 商品情報入力ページのビュー
class CreateFoodView(CreateView):
    form_class = FoodInputForm
    template_name = "input_food.html"
    success_url = reverse_lazy('dgroupapp:input_done')

    def form_valid(self, form):
        inputdata = form.save(commit=False)
        inputdata.save()
        return super().form_valid(form)


# 入力完了ページのビュー
class InputDoneView(TemplateView):
    template_name = 'input_done.html'


# 利用規約
class TeamsView(TemplateView):
    template_name = 'teams.html'
