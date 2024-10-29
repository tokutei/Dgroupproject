from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "member.html"  # アプリ名なし

    def form_valid(self, form):
        user_data = form.cleaned_data
        self.request.session['user_data'] = user_data  # セッションにデータを保存
        return redirect('dgroupLogin:signup_confirm')  # 確認画面にリダイレクト


class SignUpConfirmView(TemplateView):
    template_name = "signup_confirm.html"  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_data'] = self.request.session.get('user_data')
        return context

    def post(self, request, *args, **kwargs):
        user_data = request.session.get('user_data')
        if user_data:
            # ユーザーを作成
            form = CustomUserCreationForm(data=user_data)
            if form.is_valid():
                form.save()  # データベースに保存
                del request.session['user_data']  # セッションからデータを削除
                return redirect('dgroupLogin:signup_success')  # 成功画面にリダイレクト
        return redirect('dgroupLogin:signup')  # データがない場合は登録画面に戻る


class SignUpSuccessView(TemplateView):
    template_name = "singnup_success.html"  # 登録完了画面のテンプレート名
