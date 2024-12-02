"""
URL configuration for Dgroupproject project.
 
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from purchaseapp.views import (
    CreateCheckoutSessionView,
    ProductTopPageView,
    PurchaseCheck,
    SuccessPage,
    CancelPageView,
)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dgroupapp.urls')),
    path('', include('purchaseapp.urls')),
    path('', include('delivery.urls')),
    path('', include('foods.urls')),
    path('', include('adminmenu.urls')),
    path('dgroupLogin/', include('dgroupLogin.urls', namespace='dgroupLogin')),
    path('', include('dgrouinquiry.urls')),
    path('stripe/', ProductTopPageView.as_view(), name="product-top-page"),
    path('stripe/create-checkout-session/', CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    path('stripe/purchasecheck', PurchaseCheck, name='purchasecheck'),
    path('stripe/success/', SuccessPage, name='success'),
    path('stripe/cancel/', CancelPageView.as_view(), name="cancel"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="pw_reset.html"), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name="pw_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="pw_reset_form.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="pw_reset_done.html"), name='password_reset_complete'),
]


# urlpatternsにmediaフォルダのURLパターンを追加
urlpatterns += static(
    # MEDIA_URL = 'media/'
    settings.MEDIA_URL,
    # MEDIA_ROOTにリダイレクト
    document_root=settings.MEDIA_ROOT
)