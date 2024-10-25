from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DeleteView, DetailView
from .models import CartPost, OrderPost, OrderAitemPost
from django.urls import reverse_lazy
from urllib.parse import urlencode, urljoin


class CartView(ListView):
    template_name = 'cart.html'
    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = CartPost.objects.filter(user=user_id)
        return user_list


class PurchaseDeleteView(DeleteView):
    model = CartPost
    template_name = 'delete.html'
    def get_success_url(self):
        return reverse_lazy('purchaseapp:cart', kwargs={'user': self.request.user.id})
    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)


class PurchaseView(ListView):
    template_name = 'purchase.html'
    def get_queryset(self):
        user_id = self.kwargs['user']
        user_list = CartPost.objects.filter(user=user_id)
        return user_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_list = self.get_queryset()
        totalprice = sum(item.price for item in user_list)
        context['totalprice'] = totalprice
        return context


class DetailView(DetailView):
    template_name = 'detail.html'
    model = CartPost
