from django.shortcuts import render, redirect
from .forms import PhoneNumberForm, CustomUserForm
from .models import CustomUser
from django.urls import path
from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import redirect


class TermsAndPrivacyView(TemplateView):
    template_name = 'terms_and_privacy.html'  # 使用するテンプレート

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # コンテキストにメッセージを追加することもできます（必要に応じて）
        return context

    def post(self, request, *args, **kwargs):
        # チェックボックスの確認
        agreed_to_terms = request.POST.get('agreed_to_terms', False)
        agreed_to_privacy_policy = request.POST.get('agreed_to_privacy_policy', False)

        # 両方に同意している場合、ユーザー情報入力ページにリダイレクト
        if agreed_to_terms and agreed_to_privacy_policy:
            return redirect('dgroupLogin:phone_number')  # 'user_profile'はユーザー情報入力ページのURL名
        else:
            # どちらかに同意していない場合、エラーメッセージを表示
            messages.error(request, "利用規約とプライバシーポリシーに両方同意する必要があります。")

        # POST後に再度同じテンプレートを表示
        return self.render_to_response(self.get_context_data())


# 電話番号入力
def phone_number_view(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            request.session['phone_number'] = phone_number  # セッションに電話番号を保存
            return redirect('dgroupLogin:user_profile')
    else:
        form = PhoneNumberForm()

    return render(request, 'phone_number.html', {'form': form})


# ユーザー情報入力
def user_profile_view(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            # 電話番号をセッションから取得
            user_profile.phone_number = request.session.get('phone_number')
            user_profile.save()  # ユーザー情報をデータベースに保存
            return redirect('dgroupLogin:confirmation')
    else:
        form = CustomUserForm()

    return render(request, 'user_profile.html', {'form': form})


# 確認画面
def confirmation_view(request):
    # セッションから電話番号を取得
    phone_number = request.session.get('phone_number')
    # 最新のユーザー情報を取得
    user_profile = CustomUser.objects.latest('id')

    if request.method == 'POST':
        # 登録が完了した場合、登録完了画面にリダイレクト
        messages.success(request, "登録が完了しました。")
        return redirect('dgroupLogin:confirmation')  # 登録完了画面へのリダイレクト

    return render(request, 'confirmation.html', {
        'user_profile': user_profile,
        'phone_number': phone_number,
    })
