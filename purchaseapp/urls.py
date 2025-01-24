from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'purchaseapp'

urlpatterns = [
    path('cart/<int:user>', views.CartView.as_view(), name='cart'),
    path('cart/<int:pk>/delete', views.PurchaseDeleteView.as_view(), name='purchase_delete'),
    path('cart/deletesuccess/<str:stripe_product_id>', views.DeleteSuccess, name="deletesuccess"),
    path('cart/purchase/<int:user>', views.PurchaseView.as_view(), name='purchase'),
    path('cart/<int:pk>/detail', views.DetailView.as_view(), name='detail'),
    path('buy/<int:pk>', views.BuyView.as_view(), name='buy'),
    path('buy/buysuccess/<str:stripe_product_id>', views.BuySuccess, name='buysuccess'),
    path('cart/over/<int:pk>', views.OverView.as_view(), name='over'),
    path('cart/overback', views.Overback, name='overback'),
    path('cart/overdelete/<str:stripe_product_id>', views.OverDelete, name='overdelete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
