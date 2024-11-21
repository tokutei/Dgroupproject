from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # 電話番号
    nickname = models.CharField(max_length=30, blank=True, null=True)  # ニックネーム（日本語あり）
    address = models.CharField(max_length=255, blank=True, null=True)  # 住所

    # 必須フィールドを定義（`phone_number` と `nickname` を追加する場合）
    REQUIRED_FIELDS = ['phone_number', 'nickname']  # ここで必須のフィールドを追加
