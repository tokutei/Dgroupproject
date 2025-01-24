# dgroupinquiry/models.py
from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    postal_code = models.CharField(max_length=7) 
    address = models.CharField(max_length=255)  
    created_at = models.DateTimeField(auto_now_add=True)  # 送信日時を自動で記録

    def __str__(self):
        return self.name
