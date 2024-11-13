from django.contrib import admin
# modelsからCategory、FoodInput、Allergyクラスをインポート
from .models import Category, Food, Allergy

# # 管理サイトにCategory、FoodInput、Allergyを登録する
admin.site.register(Category)
admin.site.register(Food)
admin.site.register(Allergy)
