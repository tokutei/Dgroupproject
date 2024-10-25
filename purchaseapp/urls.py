from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'purchaseapp'

urlpatterns = [
    path('cart/<int:user>', views.CartView.as_view(), name='cart'),
    path('cart/<int:pk>/delete', views.PurchaseDeleteView.as_view(), name='purchase_delete'),
    path('cart/purchase/<int:user>', views.PurchaseView.as_view(), name='purchase'),
    path('cart/<int:pk>/detail', views.DetailView.as_view(), name='detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
