from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'address')  # 一覧表示するフィールド
    search_fields = ('name', 'email')  # 検索可能なフィールド
    list_filter = ('created_at',)  # フィルタリング可能なフィールド


# Contact モデルを管理サイトに登録
admin.site.register(Contact, ContactAdmin)
