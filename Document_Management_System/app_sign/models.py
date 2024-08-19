from django.db import models
from django.utils import timezone
import mimetypes
import os


# Create your models here.
# 登陆界面数据库中的元素
class UserProfile(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.phone_number

    # C:\Users\28740\AppData\Local\Microsoft\WindowsApps\python3.10.exe


class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    name = models.CharField(max_length=255)
    attributes = models.CharField(max_length=255, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    size = models.PositiveIntegerField()  # 以字节为单位存储大小

    def save(self, *args, **kwargs):
        # 自动识别文件类型
        if not self.attributes:
            mime_type, _ = mimetypes.guess_type(self.file.name)
            self.attributes = mime_type or 'Unknown'

        # 自动设置文件大小
        if self.file and not self.size:
            self.size = self.file.size

        # 自动设置文件名（如果没有提供）
        if not self.name:
            self.name = os.path.basename(self.file.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class FileModel(models.Model):
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    upload_date = models.DateTimeField(default=timezone.now)
    attributes = models.CharField(max_length=255, blank=True, null=True)  # 自动生成的属性字段

    def save(self, *args, **kwargs):
        if not self.attributes:  # 如果属性为空，自动设置
            mime_type, _ = mimetypes.guess_type(self.name)
            self.attributes = mime_type or 'Unknown'
        self.upload_date = timezone.now()  # 更新上传时间
        super().save(*args, **kwargs)


