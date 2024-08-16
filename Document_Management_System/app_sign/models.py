from django.db import models

# Create your models here.
# 登陆界面数据库中的元素
class UserProfile(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.phone_number