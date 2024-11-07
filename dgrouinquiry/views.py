from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # フォームデータをセッションに保存（確認用）
            request.session['contact_form_data'] = form.cleaned_data
            return redirect('dgrouinquiry:contact_confirm')  # 確認ページにリダイレクト
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def contact_confirm_view(request):
    # セッションからフォームデータを取得
    form_data = request.session.get('contact_form_data', None)
    
    if not form_data:
        return redirect('contact')  # データが無ければフォーム画面にリダイレクト

    if request.method == 'POST':
        # 確認後、データをデータベースに保存
        form = ContactForm(form_data)
        if form.is_valid():
            form.save()
            del request.session['contact_form_data']  # セッションデータを削除
            messages.success(request, 'お問い合わせいただきありがとうございます。')
            return redirect('dgrouinquiry:contact')  # 成功後にフォーム画面にリダイレクト
    else:
        form = ContactForm(form_data)

    return render(request, 'contact_confirm.html', {'form': form, 'form_data': form_data})
