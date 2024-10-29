from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import FoodInputForm


class IndexView(TemplateView):
    template_name = 'index.html'


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
