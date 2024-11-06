from django.contrib import admin
# modelsからCategory、FoodInput、Allergyクラスをインポート
from .models import Category, FoodInput
from .models import Allergy

# 管理サイトにCategory、FoodInput、Allergyを登録する
admin.site.register(Category)
admin.site.register(FoodInput)
admin.site.register(Allergy)
