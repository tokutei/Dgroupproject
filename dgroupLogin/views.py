from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserForm
from .models import CustomUser
from django.views.generic import TemplateView


# 利用規約とプライバシーポリシーの確認ページ
class TermsAndPrivacyView(TemplateView):
    template_name = 'terms_and_privacy.html'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        # チェックボックスの確認
        agreed_to_terms = request.POST.get('agreed_to_terms', False)
        agreed_to_privacy_policy = request.POST.get('agreed_to_privacy_policy', False)

        # 両方に同意している場合、ユーザー情報入力ページにリダイレクト
        if agreed_to_terms and agreed_to_privacy_policy:
            return redirect('dgroupLogin:user_profile')
        else:
            # どちらかに同意していない場合、エラーメッセージを表示
            messages.error(request, "利用規約とプライバシーポリシーに両方同意する必要があります。")

        # POST後に再度同じテンプレートを表示
        return self.render_to_response(self.get_context_data())


# 利用規約ページ
def terms_of_service_view(request):
    if request.method == 'POST':
        # 同意のチェックを削除して、同意しなくても次のページに進む
        return redirect('dgroupLogin:terms_and_privacy')  

    return render(request, 'termsofservice.html')


# プライバシーポリシー確認ページ
def privacy_confirmation_view(request):
    if request.method == 'POST':
        # プライバシーポリシーに同意するかどうかの確認を削除し、次のステップに進む
        return redirect('dgroupLogin:terms_and_privacy')  

    return render(request, 'privacyconfirmation.html')


# ユーザー情報入力
def user_profile_view(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            # ユーザー情報をセッションに保存
            request.session['user_form_data'] = form.cleaned_data  # フォームのデータをセッションに保存
            return redirect('dgroupLogin:confirmation')  # 確認ページにリダイレクト
    else:
        form = CustomUserForm()

    return render(request, 'user_profile.html', {'form': form})


# 確認画面
def confirmation_view(request):
    # セッションからフォームデータを取得
    user_form_data = request.session.get('user_form_data', None)

    if not user_form_data:
        # セッションにデータがない場合、ユーザー情報入力ページに戻る
        return redirect('dgroupLogin:user_profile')

    if request.method == 'POST':
        # 「確定」ボタンが押された場合、データを保存
        user_form_data.pop('confirm_password', None)  # 'confirm_password' を削除

        user_profile = CustomUser(**user_form_data)
        user_profile.set_password(user_form_data['password'])  # パスワードをハッシュ化
        user_profile.save()  # ユーザー情報をデータベースに保存

        # 登録が完了した場合、登録完了画面にリダイレクト
        messages.success(request, "登録が完了しました。")
        return redirect('dgroupLogin:singnup_success')  # 登録完了画面へのリダイレクト

    return render(request, 'confirmation.html', {
        'user_profile': user_form_data,
    })


# 登録完了画面
def singnup_success_view(request):
    # 最新のユーザー情報を取得
    user_profile = CustomUser.objects.latest('id')

    return render(request, 'singnup_success.html', {
        'user_profile': user_profile,
    })
