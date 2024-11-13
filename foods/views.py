from django.shortcuts import render
from django.views.generic import TemplateView, DeleteView, CreateView
from django.urls import reverse_lazy
from .forms import FoodInputForm


# 商品情報入力ページのビュー
class CreateFoodView(CreateView):
    form_class = FoodInputForm
    template_name = "food_input.html"
    success_url = reverse_lazy('foods:input_done')

    def form_valid(self, form):
        inputdata = form.save(commit=False)
        allergy = form.cleaned_data.get("allergy")
        if allergy:
            inputdata.allergy = '、'.join(allergy)
        inputdata.save()
        return super().form_valid(form)


# 入力完了ページのビュー
class InputDoneView(TemplateView):
    template_name = 'input_done.html'
