# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # フォームデータをデータベースに保存
            messages.success(request, 'お問い合わせいただきありがとうございます。')  # メッセージを設定
            return redirect('/contact/')  # 絶対パスでリダイレクト
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
